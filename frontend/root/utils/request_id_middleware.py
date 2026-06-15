import uuid

from django.utils.deprecation import MiddlewareMixin

from utils.request_context import REQUEST_ID_HEADER, set_request_id


class RequestIdMiddleware(MiddlewareMixin):
    """Middleware для добавления request_id в запрос и ответ"""

    def process_request(self, request):
        request_id = request.META.get('HTTP_X_REQUEST_ID') or str(uuid.uuid4())
        set_request_id(request_id)
        request.request_id = request_id

    def process_response(self, request, response):
        request_id = getattr(request, 'request_id', None)
        if request_id:
            response[REQUEST_ID_HEADER] = request_id
        set_request_id(None)
        return response
