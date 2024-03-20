
from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name=""),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('user-logout', views.user_logout, name="user-logout"),

#CRUD
    path('dashboard', views.dashboard, name="dashboard"),

    path('dashboard2', views.dashboard2, name="dashboard2"),

    path('create-record', views.create_record, name="create-record"),

    path('update-record/<int:pk>', views.update_record, name='update-record'),

    path('record/<int:pk>', views.singular_record, name="record"),

    path('delete-record/<int:pk>', views.delete_record, name="delete-record"),

    path('upload', views.upload, name="upload"),
    
    path('download', views.download, name="download"),

    path('creer/', views.creer_fichier, name='creer_fichier'),

    path('telecharger/<int:fichier_id>/', views.telecharger_fichier, name='telecharger_fichier'),

    path('telecharger_fichier_direct/<int:fichier_id>/', views.telecharger_fichier_direct, name='telecharger_fichier_direct'),

    path('download-file/', views.download_file, name='download_file'),

    path('download-file2/', views.download_file2, name='download_file2'),

    path('traitement_fin/<str:file>', views.traitement_fin, name='traitement_fin'),


    path('upload_file', views.upload_file, name="upload_file"),

    path('table', views.table, name="table"),

    path('views_table', views.views_table, name="views_table"),
    
    path('redevance/<int:pk>', views.singular_redevance, name="redevance"),

    path('update-redevance/<int:pk>', views.update_redevance, name='update-redevance'),

    path('accordion', views.accordion, name="accordion"),

]