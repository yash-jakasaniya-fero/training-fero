import pandas as pd
import openpyxl
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import ContactXLSXSerializer, ContactXLSXUploadSerializer #,ContactListEditSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Contact, ContactNumbers
from .serializers import ContactUpdateSerializer, ContactCreateSerializer, ContactListSerializer, ContactNumberSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return ContactUpdateSerializer
        return ContactCreateSerializer


class ContactNumberViewSet(viewsets.ModelViewSet):
    queryset = ContactNumbers.objects.all()
    serializer_class = ContactNumberSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        contact_id = self.request.query_params.get('contact_id', None)
        if contact_id:
            queryset = queryset.filter(contact_id=contact_id)
        return queryset

class ContactDetailsViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

# class ContactXLSXExportView(APIView):
#     def get(self, request, *args, **kwargs):
#         contact_numbers = ContactNumbers.objects.all()
#         serializer = ContactXLSXSerializer(contact_numbers, many=True)
#         # return Response(serializer.data)
#
#         workbook = openpyxl.Workbook()
#         sheet = workbook.active
#         sheet.title = "Contacts"
#
#         headers = ["ID", "First Name", "Last Name", "Email", "Contact Type", "Contact Number"]
#         sheet.append(headers)
#
#         for contact in serializer.data:
#             sheet.append([
#                 contact["id"],
#                 contact["first_name"],
#                 contact["last_name"],
#                 contact["email"],
#                 contact["contact_type"],
#                 contact["contact_number"]
#             ])
#
#         response = HttpResponse(content_type="application/ms-excel")
#         response["Content-Disposition"] = 'attachment; filename="contacts.xlsx"'
#         workbook.save(response)
#         return response

class ContactXLSXExportView(APIView):
    def get(self, request, *args, **kwargs):
        contact_numbers = ContactNumbers.objects.all()
        serializer = ContactXLSXSerializer(contact_numbers, many=True)

        df = pd.DataFrame(serializer.data)

        df = df.rename(columns={
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "contact_type": "Contact Type",
            "contact_number": "Contact Number"
        })

        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="contacts.xlsx"'

        with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Contacts")

        return response


class ContactXLSXImportView(APIView):

    def post(self, request, *args, **kwargs):
        payload = request.data
        try:
            serializer = ContactXLSXUploadSerializer(data=payload, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Contacts imported successfully"})
            else:
                return Response(serializer.errors)
        except Exception as e:
            return Response({"error": str(e)})