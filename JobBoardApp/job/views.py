from django.shortcuts import render
from .models import Job
from rest_framework import status , generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import JobModelSerializer , JobSerializer
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.


#UsingJobModelSerializer
#Function-Based Views
@api_view(['GET', 'POST'])
def job_list1(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        serializer = JobModelSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def job_detail1(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobModelSerializer(job)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = JobModelSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Class-Based Views

class JobListAPIView1(APIView):
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobModelSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDetailAPIView1(APIView):
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        job = self.get_object(pk)
        serializer = JobModelSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk)
        serializer = JobModelSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#UsingJobSerializer

# #Function-Based Views
@api_view(['GET', 'POST'])
def job_list2(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def job_detail2(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Class-Based Views
class JobListAPIView2(APIView):
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDetailAPIView2(APIView):
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        job = self.get_object(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Pagination
class JobPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'


#Filters
class JobFilteredListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'company_name', 'location']
    search_fields = ['title']
    pagination_class = JobPagination