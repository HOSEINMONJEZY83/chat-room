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
    path('report',views.report,name='report')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
   path('<path:invalid_path>',views.invalid_path,name='invalid_path')
]