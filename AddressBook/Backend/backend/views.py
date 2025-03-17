from http.client import responses
from wsgiref.util import request_uri
import pandas as pd
import openpyxl
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .models import Contact ,ContactNumbers
from .serializers import ContactSerializer, ContactListSerializer, ContactNumberSerializer, ContactXLSXSerializer, ContactXLSXUploadSerializer

class ContactAPI(APIView):

    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ContactListAPI(APIView):

    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactListSerializer(contacts, many=True)
        return Response(serializer.data)

    def get(self, request):
        queryset = Contact.objects.all()
        first_name = request.query_params.get('first_name', None)
        last_name = request.query_params.get('last_name', None)
        email = request.query_params.get('email', None)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if email:
            queryset = queryset.filter(email__icontains=email)

        serializer = ContactListSerializer(queryset, many=True)
        return Response(serializer.data)

class ContactNumberAPI(APIView):
    def get(self, request, id):
        if id:
            try:
                contact_number = ContactNumbers.objects.get(id=id)
                serializer = ContactNumberSerializer(contact_number)
                return Response(serializer.data)
            except ContactNumbers.DoesNotExist:
                return Response({"error": "contact not found"})

    def put(self, request, id):
            contact_number = ContactNumbers.objects.get(id=id)
            serializer = ContactNumberSerializer(contact_number, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

class ContactDetailsAPI(APIView):
    def get(self, request, id):
        if id:
            try:
                contacts = Contact.objects.get(id=id)
                serializer = ContactListSerializer(contacts)
                return Response(serializer.data)
            except Contact.DoesNotExist:
                return Response({"error": "contact not found"})

    def put(self, request, id):
            contacts = Contact.objects.get(id=id)
            serializer = ContactListSerializer(contacts, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

    def delete(self, request, id):
        try:
            contacts = Contact.objects.get(id=id)
            contacts.delete()
            return Response({'message': 'contact deleted'})
        except Contact.DoesNotExist:
            return Response({"message": "contact not found"})

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