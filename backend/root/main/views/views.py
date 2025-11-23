from rest_framework.views import APIView
from rest_framework.response import Response

from main.permissions import CustomPermission


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
