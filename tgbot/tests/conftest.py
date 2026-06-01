import os

import pytest


@pytest.fixture(autouse=True)
def _set_env_defaults(monkeypatch):
    # Minimal env for config/secrets readers during tests.
    monkeypatch.setenv("ID", "777")
    monkeypatch.setenv("SITELINK", "https://example.test/diary")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("MAX_YEAR", "5")
    monkeypatch.setenv(
        "PROJECT_HOSTS",
        '{"backend":"http://back:8000/","auth_server":"http://authserver:8000/","tg_server":"http://botapi:8000/"}',
    )

    # Token is not used in handler tests, but keep a valid format anyway.
    monkeypatch.setenv("TOKEN", "123456789:test-token")

    # Ensure no other tests leak env into this session.
    yield


class FakeChat:
    def __init__(self, chat_id: int):
        self.id = chat_id


class FakeFromUser:
    def __init__(self, user_id: int, first_name: str = "User", username: str = "usernick"):
        self.id = user_id
        self.first_name = first_name
        self.username = username


class FakeMessage:
    def __init__(self, text: str, chat_id: int = 1001, from_user_id: int = 2002):
        self.text = text
        self.chat = FakeChat(chat_id)
        self.from_user = FakeFromUser(from_user_id)


class FakeCallbackMessage:
    def __init__(self, chat_id: int):
        self.chat = FakeChat(chat_id)


class FakeCallbackQuery:
    def __init__(self, data: str, chat_id: int = 1001):
        self.data = data
        self.message = FakeCallbackMessage(chat_id)


class FakeBot:
    """
    Minimal TeleBot-like surface used by our handlers.
    Stores registered handlers so tests can call them directly.
    """

    def __init__(self):
        self._command_handlers: dict[str, callable] = {}
        self._callback_handlers: list[callable] = []
        self.sent_messages: list[dict] = []
        self.next_step_handlers: list[tuple] = []

    def message_handler(self, commands=None, **_kwargs):
        commands = commands or []

        def decorator(fn):
            for cmd in commands:
                self._command_handlers[cmd] = fn
            return fn

        return decorator

    def callback_query_handler(self, func=None, **_kwargs):
        def decorator(fn):
            self._callback_handlers.append((func, fn))
            return fn

        return decorator

    def register_next_step_handler(self, msg, fn, *args):
        self.next_step_handlers.append((msg, fn, args))

    def send_message(self, chat_id, text, **kwargs):
        self.sent_messages.append({"chat_id": chat_id, "text": text, **kwargs})

    # Convenience helpers for tests
    def call_command(self, command: str, msg: FakeMessage):
        handler = self._command_handlers[command]
        return handler(msg)

    def call_callback(self, callback: FakeCallbackQuery):
        for func, handler in self._callback_handlers:
            if func is None or func(callback):
                return handler(callback)
        raise AssertionError("No callback handler matched")

