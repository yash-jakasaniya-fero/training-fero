from django.urls import path
from .views import ContactAPI, ContactListAPI, ContactDetailsAPI, ContactNumberAPI, ContactXLSXExportView, ContactXLSXImportView

urlpatterns = [
    path('contacts/', ContactAPI.as_view(), name='contact-view'),
    path('contacts/list/', ContactListAPI.as_view(), name='contact-list'),
    path('contacts/<int:id>/', ContactDetailsAPI.as_view(), name='contact-list'),
    path('contact_numbers/<int:id>/',ContactNumberAPI.as_view(), name='contact_number-view_update'),
    path('contacts/download/', ContactXLSXExportView.as_view(), name='contact_xlsx_download'),
    path('contacts/import/',ContactXLSXImportView.as_view(), name='contact_xlsx_import')
]