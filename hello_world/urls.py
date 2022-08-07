from django.urls import include, re_path
from hello_world import views

# SET THE NAMESPACE!
app_name = 'hello_world'

urlpatterns=[
    re_path(r'^register/$',views.register,name='register'),
    re_path(r'^user_login/$',views.user_login,name='user_login'),
    re_path(r'^dashboard/$',views.dashboard,name='dashboard'),
]