 
from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_usr, name="login"),
    path('logout/', views.logout_usr, name="logout"),
    path('signup/', views.signup_usr, name="signup"),
    path('reset-password/', views.reset_password, name="reset-password"),
    #path('app/', views.app, name="app"),
    path('start/', views.start, name="start"),
    path('start-chat/', views.get_or_create_chatroom, name="start-chat"),
    path('overview/', views.overview, name="overview"),
    path('settings/', views.settings, name="settings"),
    path('account/', views.account, name="account"),
    path('help/', views.help, name="help"),
    path('notification/', views.notification, name="notification"),
    path('docs/', views.docs, name="docs"),
    path('notfound/', views.notfound, name="notfound"),
    path('upload/', views.upload_file, name='upload_file'),
    path('first-upload/', views.first_upload, name='first-upload'),
    path('delete_vector/<int:file_id>/', views.delete_vector_db, name='delete_vector_db'),
    path('chat/room/<chatroom_name>', views.app, name="chatroom"),
    path('chat/get-room/<destination_url>', views.get_room, name="get-room"),
    path('chat/edit/<chatroom_name>', views.chatroom_edit, name="chatroom-edit"),
    path('chat/delete/<chatroom_name>', views.chatroom_delete, name="chatroom-delete"),


]
