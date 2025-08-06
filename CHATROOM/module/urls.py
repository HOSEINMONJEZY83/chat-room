from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('about-us',views.aboutus,name='aboutus'),
    path('account',views.account,name='account'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('changeinformation',views.changeinformation,name='changeinformation'),
    path('chatroom',views.chatroom,name='chatroom'),
    path('sendmessage',views.sendmessage,name='sendmessage'),
    path('',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('signup',views.signup,name='signup'),
    path('report',views.report,name='report'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('api/users/', views.user_list_create, name='user_list_create'),
    path('api/users/<int:user_id>/', views.user_detail_update, name='user_detail_update'),
    path('api/report_message_api', views.report_message_api, name='report_message_api'),
    path('api/messages/', views.message_api, name='message_list_create'),
    path('api/messages/<int:message_id>/', views.message_detail, name='message_detail')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
   path('<path:invalid_path>',views.invalid_path,name='invalid_path')
]