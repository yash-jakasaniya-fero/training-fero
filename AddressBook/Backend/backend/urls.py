from django.urls import path
from .views import ContactViewSet, ContactNumberViewSet, ContactDetailsViewSet, ContactXLSXExportView, ContactXLSXImportView

urlpatterns = [
    path('contacts/', ContactViewSet.as_view({'get': 'list', 'post': 'create'}), name='contact-list-create'),
    path('contacts/<int:pk>/', ContactViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy','patch': 'partial_update'}), name='contact-detail'),

    path('contact-numbers/', ContactNumberViewSet.as_view({'get': 'list', 'post': 'create'}),name='contact-number-list-create'),
    path('contact-numbers/<int:pk>/', ContactNumberViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),name='contact-number-detail'),

    path('contact-details/', ContactDetailsViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}), name='contact-detail-list-create'),
    path('contact-details/<int:pk>/',ContactDetailsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),name='contact-detail-detail'),

    path('contacts/download/', ContactXLSXExportView.as_view(), name='contact_xlsx_download'),
    path('contacts/import/', ContactXLSXImportView.as_view(), name='contact_xlsx_import'),
]
