from django.urls import path, include
from rest_framework import routers

from .views.views import (
    PublicAPI, SecretAPI
)
from .views.filesystem import (
    BlankFileSystemAPI, RecordsFSAPI,
    RecordsAPI, RecordFoldersAPI,
    MoveBetweenAPI, MoveInsideAPI,
)
from .views.content import (
    RecordContentAPI, BlankDataAPI, NoteAPI, ImageAPI, ImagesAPI
)


urlpatterns = []

test_urls = [
    path(  # get test public content
        route='public/',
        view=PublicAPI.as_view(),
        name='get_test_public_content'
    ),
    path(  # get test secret content
        route='secret/',
        view=SecretAPI.as_view(),
        name='get_test_secret_content'
    ),
]
urlpatterns += test_urls

file_system_urls = [
    path(  # create test filesystem content
        route='set-test/',
        view=BlankFileSystemAPI.as_view(),
        name='create_test_fs_content'
    ),
    path(  # get all records and folders
        route='',
        view=RecordsFSAPI.as_view(),
        name='get_fs_content'
    ),
    path(  # post record
        route='records/',
        view=RecordsAPI.as_view(),
        name='create_record'
    ),
    path(  # patch/delete record
        route='records/<int:record_id>/',
        view=RecordsAPI.as_view(),
        name='change_record'
    ),
    path(  # post folders
        route='folders/',
        view=RecordFoldersAPI.as_view(),
        name='create_folder'
    ),
    path(  # patch/delete folders
        route='folders/<int:folder_id>/',
        view=RecordFoldersAPI.as_view(),
        name='change_folder'
    ),

    # move event
    path(  # put object in the new folder
        route='move/inside/',
        view=MoveInsideAPI.as_view(),
        name='move_inside'
    ),
    path(  # change objects order
        route='move/between/',
        view=MoveBetweenAPI.as_view(),
        name='move_between'
    ),
]
urlpatterns += [path("file-system/", include(file_system_urls))]

records_urls = [
    path(  # create test messages
        route='set-content/',
        view=BlankDataAPI.as_view(),
        name='create_test_record_content'
    ),
    path(  # get details and messages
        route='<int:record_id>/',
        view=RecordContentAPI.as_view(),
        name='get_all_content'
    ),
    path(  # post note
        route='<int:record_id>/notes/',
        view=NoteAPI.as_view(),
        name='create_note'
    ),
    path(  # get/patch/delete note
        route='<int:record_id>/notes/<int:note_id>/',
        view=NoteAPI.as_view(),
        name='get_note'
    ),
    path(  # post image
        route='<int:record_id>/images/',
        view=ImageAPI.as_view(),
        name='create_image'
    ),
    path(  # get/delete image
        route='<int:record_id>/images/<int:image_id>/',
        view=ImageAPI.as_view(),
        name='get_image'
    ),
    path(  # post images group
        route='<int:record_id>/images-group/',
        view=ImagesAPI.as_view(),
        name='create_image_group'
    ),
    path(  # get/delete images group
        route='<int:record_id>/images-group/<int:msg_id>/',
        view=ImagesAPI.as_view(),
        name='get_image_group'
    ),
]
urlpatterns += [path("records/", include(records_urls))]


# === Router URLs ===
test_router = routers.DefaultRouter()  # test file upload

urlpatterns += [path("", include(test_router.urls))]
