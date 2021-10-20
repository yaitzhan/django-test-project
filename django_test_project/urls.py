"""django_test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from account import views
from storage import views as storage_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('transactions/', views.TransactionView.as_view(), name='transactions'),
    path('usersaccounts/', views.UserAccountsView.as_view(), name='usersaccounts-list'),

    path('', storage_views.HomeView.as_view(), name='home'),
    path('fileupload/', storage_views.FileUploadView.as_view(), name='file-upload'),
    path('filedownload/<int:file_id>/', storage_views.FileDownloadView.as_view(), name='file-download')
]
