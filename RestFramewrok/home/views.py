from functools import partial
from turtle import color

from django.contrib.admin.templatetags.admin_list import pagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sqlalchemy.sql.coercions import expect

from .models import Person
from .serializers import PeopleSerializer, LoginSerializer , RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from django.core.paginator import Paginator
from rest_framework.decorators import action


class LoginAPI(APIView):
    def post(self, request):
        data=request.data
        serializer = LoginSerializer( data = data)

        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        print(serializer.data)
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        print(user)
        if not user:
            return Response({
                'status': False,
                'message': 'invalid credentials'
            }, status.HTTP_400_BAD_REQUEST)



        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return Response({
            'status' : True,
            'message' : 'user login',
            'token' : str(token)
        }, status.HTTP_201_CREATED)



class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response({
            'status' : True,
            'message' : 'user created '
        }, status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT'])
def index(request):
    courses = {
        'courses_name': 'python',
        'learn': ['Django','flask'],
        'course_provider' : 'Fero'
    }

    if request.method == 'GET':
        print('You hit a GET method')
        return Response(courses)
    elif request.method == 'POST':
        print('You hit a POST method')
        return Response(courses)
    elif request.method == 'PUT':
        print('You hit a PUT method')
        return Response(courses)
    else:
        data = request.data
        print(data)
        json_response = {
            'name': 'Scaler',
            'courses': ['python'],
            'method': 'POST'
        }
    return Response(json_response)


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message':'success'})
    return Response(serializer.errors)


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        try:
            print(request.user)
            obj = Person.objects.filter(color__isnull=False)
            page = request.GET.get('page', 1)
            page_size = 1

            paginator = Paginator(obj, page_size)

            serializer = PeopleSerializer(paginator.page(page), many=True)

            return Response(serializer.data)

        except Exception as e:
            return Response({
            'status': False,
            'message': 'invalid paga'
            })

    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'person deleted'})


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        obj = Person.objects.filter(color__isnull = False)
        serializer = PeopleSerializer(obj, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'PUT' :
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'PATCH' :
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data=data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'person deleted'})


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    @action(detail=False, methods=['post'])
    def send_mail_to_person(self, request):
        return Response({
            'status' : True,
            'message' : 'email send succesfully'
        })
