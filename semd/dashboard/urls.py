from django.urls import path
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('month/<int:q_month>/', views.index, name='index_by_month'),
    path('month/<int:q_month>/year/<int:q_year>/', views.index, name='index_by_month_year'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('delete_all_semd/', views.delete_all_semd, name='delete_all_semd'),
]