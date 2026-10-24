from django.urls import path
from machines import views

app_name = 'machines'

urlpatterns = [
    path('', views.MachineListView.as_view(), name='list'),
    path('create/', views.MachineCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MachineDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.MachineEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.MachineDeleteView.as_view(), name='delete'),
]