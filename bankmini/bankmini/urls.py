from django.contrib import admin
from django.urls import path
from siswa.views import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(IndexView.as_view(), login_url='login/'), name='index'),
    path('dashboard/', login_required(DashboardView.as_view(), login_url='../login/'), name='dashboard'),
    path('transfer/', login_required(TransferView.as_view(), login_url='../login/'), name='transfer'),
    path('profile/', login_required(ProfileView.as_view(), login_url='../login/'), name='profile'),
    path('privacy/', login_required(PrivacyView.as_view(), login_url='../login.'), name='privacy'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)
