from django.urls import path, include
from rest_framework import routers

from .views.views import (
    PublicAPI, SecretAPI, TestDateAPI, TestTGAPI, TestFromTGAPI,
    TestAPI,
)
from .views.FSRecordViews import (
    BlankFileSystemAPI, RecordsFSAPI,
    RecordsAPI, RecordFoldersAPI,
)
from .views.FSNoticeViews import (
    BlankFileSystemAPI2, NoticesFSAPI,
    NoticesAPI, NoticeFoldersAPI,
    DisplayPeriodicDate,
)
from .views.FSMoveViews import (
    MoveBetweenAPI, MoveInsideAPI,
)
from .views.content import (
    RecordContentAPI, BlankDataAPI, NoteAPI, ImageAPI, ImagesAPI,
    NoticeImageAPI, NoticesImageAPI
)
from .views.common import FirstSetUp
from .views.TGServer import (
    CreateNoticeAPI, NoticeShiftAPI, UserInfoAPI
)


urlpatterns = []

# ===== Test API =====
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
    path(  # post test periodic date
        route='periodic-date/',
        view=TestDateAPI.as_view(),
        name='get_test_periodic_date'
    ),
    path(  # get/post test tg server
        route='tg-test/',
        view=TestTGAPI.as_view(),
        name='test_tg_server'
    ),
    path(  # get/post test tg server
        route='from-fastapi/',
        view=TestFromTGAPI.as_view(),
        name='from_fastapi'
    ),
    path(  # get test any function
        route='any-test/',
        view=TestAPI.as_view(),
        name='any_test'
    ),
]
urlpatterns += [path("tests/", include(test_urls))]

test_router = routers.DefaultRouter()  # test file upload

urlpatterns += [path("", include(test_router.urls))]

# ===== Common API =====
auth_requests_urls = [
    path(  # create root directories (post from the auth server)
        route='create-roots/',
        view=FirstSetUp.as_view(),
        name='create_roots'
    ),
]
urlpatterns += [path("auth/", include(auth_requests_urls))]

# ===== File system API =====
file_system_record_urls = [
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
]
urlpatterns += [path("file-system/record-content/", include(file_system_record_urls))]

file_system_notice_urls = [
    path(  # create test filesystem content
        route='set-test/',
        view=BlankFileSystemAPI2.as_view(),
        name='create_test_fs_notice_content'
    ),
    path(  # get all notices and folders
        route='',
        view=NoticesFSAPI.as_view(),
        name='get_fs_notice_content'
    ),
    path(  # post notice
        route='notices/',
        view=NoticesAPI.as_view(),
        name='create_notice'
    ),
    path(  # patch/delete notice
        route='notices/<int:notice_id>/',
        view=NoticesAPI.as_view(),
        name='change_notice'
    ),
    path(  # post folders
        route='folders/',
        view=NoticeFoldersAPI.as_view(),
        name='create_notice_folder'
    ),
    path(  # patch/delete folders
        route='folders/<int:folder_id>/',
        view=NoticeFoldersAPI.as_view(),
        name='change_notice_folder'
    ),
    path(  # post - getting nextdate into a form
        route='get-nextdate/',
        view=DisplayPeriodicDate.as_view(),
        name='get_nextdate'
    )
]
urlpatterns += [path("file-system/notice-content/", include(file_system_notice_urls))]

file_system_move_urls = [
    path(  # put object in the new folder
        route='inside/',
        view=MoveInsideAPI.as_view(),
        name='move_inside'
    ),
    path(  # change objects order
        route='between/',
        view=MoveBetweenAPI.as_view(),
        name='move_between'
    ),
]
urlpatterns += [path("file-system/move/", include(file_system_move_urls))]

# ===== Content (record/notice) API =====
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

# ===== Notice API =====
notice_urls = [
    path(  # get/delete notice image
        route='<int:notice_id>/images/<int:image_id>/',
        view=NoticeImageAPI.as_view(),
        name='create_notice_image'
    ),
    path(  # get/post/delete notice images
        route='<int:notice_id>/images/',
        view=NoticesImageAPI.as_view(),
        name='create_notice_image'
    ),
]
urlpatterns += [path("notices/", include(notice_urls))]

# ===== TG Server API =====
tg_server_urls = [
    path(  # post new notice
        route='new-notice/',
        view=CreateNoticeAPI.as_view(),
        name='create_notice'
    ),
    path(  # post shift notice
        route='notice-shift/',
        view=NoticeShiftAPI.as_view(),
        name='shift_notice'
    ),
    path(  # save user info ???
        route='save-user-info/',
        view=UserInfoAPI.as_view(),
        name='save_user_info'
    ),
]
urlpatterns += [path("tg-server/", include(tg_server_urls))]
