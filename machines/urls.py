from django.urls import path
from machines import views

app_name = 'machines'

urlpatterns = [
    path('', views.MachineListView.as_view(), name='list'),
    path('create/', views.MachineCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MachineDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.MachineEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.MachineDeleteView.as_view(), name='delete'),
    path('<int:pk>/components/create/', views.ComponentCreateView.as_view(), name='component_create'),
    path('components/<int:pk>/edit/', views.ComponentEditView.as_view(), name='component_edit'),
    path('components/<int:pk>/', views.ComponentDetailView.as_view(), name='component_detail'),
    path('components/<int:pk>/delete/', views.ComponentDeleteView.as_view(), name='component_delete'),
]