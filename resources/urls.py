from resources import views
from django.urls import path

app_name = 'resources'

urlpatterns = [
    path('technicians/', views.TechnicianListView.as_view(), name='technician_list'),
    path('technicians/create/', views.TechnicianCreateView.as_view(), name='technician_create'),
    path('technicians/<int:pk>/', views.TechnicianDetailView.as_view(), name='technician_details'),
    path('technicians/<int:pk>/edit/', views.TechnicianEditView.as_view(), name='technician_edit'),
    path('technicians/<int:pk>/delete/', views.TechnicianDeleteView.as_view(), name='technician_delete'),

    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_details'),
    path('suppliers/<int:pk>/edit/', views.SupplierEditView.as_view(), name='supplier_edit'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),

    path('parts/', views.PartListView.as_view(), name='part_list'),
    path('parts/create/', views.PartCreateView.as_view(), name='part_create'),
    path('parts/<int:pk>/', views.PartDetailView.as_view(), name='part_details'),
    path('parts/<int:pk>/edit/', views.PartEditView.as_view(), name='part_edit'),
    path('parts/<int:pk>/delete/', views.PartDeleteView.as_view(), name='part_delete'),
]