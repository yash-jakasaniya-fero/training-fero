from django.urls import path, include
from job.views import job_list1 , job_detail1, JobListAPIView1 , JobDetailAPIView1 ,job_list2, job_detail2, JobListAPIView2 , JobDetailAPIView2, JobFilteredListView


urlpatterns = [

    path('v1/jobs1/', job_list1, name='job-list'),
    path('v1/jobs1/<int:pk>/', job_detail1, name='job-list'),

    path('v1/jobs11/', JobListAPIView1.as_view(), name='job-list-class'),
    path('v1/jobs11/<int:pk>/', JobDetailAPIView1.as_view(), name='job-list-class'),

    path('v1/jobs2/', job_list2, name='job-list'),
    path('v1/jobs2/<int:pk>/', job_detail2, name='job-list'),

    path('v1/jobs22/', JobListAPIView2.as_view(), name='job-list-class'),
    path('v1/jobs22/<int:pk>/', JobDetailAPIView2.as_view(), name='job-list-class'),

    path('v2/jobs/', JobFilteredListView.as_view(), name='job-list-filtered'),

]
