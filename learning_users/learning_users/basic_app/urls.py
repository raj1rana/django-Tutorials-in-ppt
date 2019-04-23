from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static



# add the template URLS here

app_name = 'basic_app'

# URL PATHS
urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/',views.user_login,name='user_login'),
]
static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
