from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from main.permissions import CustomPermission
from main.serializers import UploadTestSerializer
from main.models import UploadedTest


class PublickAPI(APIView):
    # authentication_classes = []

    def get(self, request):
        return Response(
            data={
                'success': True,
                'data': 'publick data',
                'user_id': request.user_info['id'],
                'username': request.user_info['username'],
                'role': request.user_info['role'],
                'is_auth': request.user_info['is_auth'],
            }
        )


class SecretAPI(APIView):
    permission_classes = [CustomPermission]

    def get(self, request):
        return Response(
            data={
                'success': True,
                'data': 'secret data',
                'user_id': request.user_info['id'],
                'username': request.user_info['username'],
                'role': request.user_info['role'],
                'is_auth': request.user_info['is_auth'],
            }
        )


class UploadTestViewSet(ModelViewSet):
    """Создание и удаление картинок.
    P.S. получение (путей) через методы контента.
    Здесь метод get отключен (но будет работать при включении)"""
    model = UploadedTest
    queryset = UploadedTest.objects.all()
    serializer_class = UploadTestSerializer
    # permission_classes = [CustomPermission]
    http_method_names = ['post', 'delete']

    def get_queryset(self):
        # user_id = self.request.user_info['id']
        user_id = 1  # для работы без токена
        return self.model.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        """Создание картинок по списку"""

        # user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        files = request.FILES.getlist('files')

        if not files:
            return Response("Error: files not found",
                            status=status.HTTP_400_BAD_REQUEST)

        data_list = []
        for file in files:
            data = {
                'title': file.name,
                'file': file,
                'user_id': user_id
            }
            data_list.append(data)

        serializer = self.get_serializer(data=data_list, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # print(serializer.errors)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Удаление картинки по id"""
        instance = self.get_object()

        # Удаление файла из файловой системы
        if instance.file:
            instance.file.delete(save=False)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
