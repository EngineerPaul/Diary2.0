from django.urls import path

from .views.views import (
    PublickAPI, SecretAPI,
)
from .views.filesystem import (
    BlankFileSystemAPI, RecordsFSAPI,
    RecordsAPI, RecordFoldersAPI
)
from .views.content import (
    RecordContentAPI, BlankDataAPI, NoteAPI, ImageAPI, ImagesAPI
)



urlpatterns = [
    path('publick', PublickAPI.as_view()),
    path('secret', SecretAPI.as_view()),

    # file-system
    path('file-system/set-test', BlankFileSystemAPI.as_view()),
    path('file-system', RecordsFSAPI.as_view()),
    path('file-system/records/<int:record_id>/', RecordsAPI.as_view()),
    path('file-system/records', RecordsAPI.as_view()),
    path('file-system/folders/<int:folder_id>/', RecordFoldersAPI.as_view()),
    path('file-system/folders', RecordFoldersAPI.as_view()),

    # content
    path('records/<int:record_id>/', RecordContentAPI.as_view()),
    path('records/set-content', BlankDataAPI.as_view()),
    path('records/<int:record_id>/notes/<int:note_id>/', NoteAPI.as_view()),
    path('records/<int:record_id>/notes/', NoteAPI.as_view()),
    path('records/<int:record_id>/images/<int:image_id>/', ImageAPI.as_view()),
    path('records/<int:record_id>/images/', ImageAPI.as_view()),
    path('records/<int:record_id>/images-group/<int:msg_id>/', ImagesAPI.as_view()),
    path('records/<int:record_id>/images-group/', ImagesAPI.as_view()),


]
