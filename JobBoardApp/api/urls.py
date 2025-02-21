from django.urls import path, include
from job.views import job_list1 , job_detail1, JobListAPIView1 , JobDetailAPIView1 ,job_list2, job_detail2, JobListAPIView2 , JobDetailAPIView2, JobFilteredListView


urlpatterns = [
#UsingJobModelSerializer
#Function-Based Views
    path('v1/md/fun/jobs/', job_list1, name='job-list'),
    path('v1/md/fun/jobs/<int:pk>/', job_detail1, name='job-list'),
#Class-Based Views
    path('v1/md/class/jobs/', JobListAPIView1.as_view(), name='job-list-class'),
    path('v1/md/class/jobs/<int:pk>/', JobDetailAPIView1.as_view(), name='job-list-class'),
#UsingJobSerializer
#Function-Based Views
    path('v1/jb/fun/jobs/', job_list2, name='job-list'),
    path('v1/jb/fun/jobs/<int:pk>/', job_detail2, name='job-list'),
#Class-Based Views
    path('v1/jb/class/jobs/', JobListAPIView2.as_view(), name='job-list-class'),
    path('v1/jb/class/jobs/<int:pk>/', JobDetailAPIView2.as_view(), name='job-list-class'),
#pagination and filters
    path('v2/jobs/', JobFilteredListView.as_view(), name='job-list-filtered'),

]
