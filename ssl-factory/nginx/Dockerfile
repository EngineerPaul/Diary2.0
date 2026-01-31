# Временный nginx для SSL Factory
# Минимальная конфигурация только для верификации домена

FROM nginx:1.27-alpine

# Удаляем стандартную конфигурацию nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем временную конфигурацию для SSL верификации
COPY temp-ssl.conf /etc/nginx/conf.d/default.conf

# Создаем директорию для логов
RUN mkdir -p /var/log/nginx

# Порт для HTTP верификации
EXPOSE 80
