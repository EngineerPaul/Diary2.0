import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import NoticeFolder, RecordFolder
from main.permissions import ServiceTokenPermission

logger = logging.getLogger(__name__)


class FirstSetUp(APIView):
    """Creating root directories after registration"""

    permission_classes = [ServiceTokenPermission]

    def post(self, request):

        user_id = request.data.get('user_id')

        if not user_id:
            msg = 'Error: user_id not found'
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        RecordFolder.objects.create(
            user_id=user_id,
            title='root',
            parent_id=None
        )
        NoticeFolder.objects.create(
            user_id=user_id,
            title='root',
            parent_id=None
        )
        logger.info('Root folders created', extra={'extra_fields': {'user_id': user_id}})

        msg = 'Корневые папки созданы'
        return Response(msg, status=status.HTTP_201_CREATED)
