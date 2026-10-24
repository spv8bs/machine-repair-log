from django.urls import path
from repairs import views

app_name = 'repairs'

urlpatterns = [
    path('', views.RepairListView.as_view(), name='list'),
    path('select-machine/', views.RepairSelectMachineView.as_view(), name='select_machine'),
    path('create/', views.RepairCreateView.as_view(), name='create'),
    path('<int:pk>/', views.RepairDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.RepairEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.RepairDeleteView.as_view(), name='delete'),
    path('<int:repair_pk>/actions/add/', views.RepairActionCreateView.as_view(), name='action_create'),
]
