from multiprocessing.resource_tracker import register

from django.urls import path, include

from rest_framework.routers import DefaultRouter
from home.views import PeopleViewSet, index, person, login, PersonAPI ,RegisterAPI, LoginAPI


router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('register/',RegisterAPI.as_view()),
    path('login/',LoginAPI.as_view()),
    path('index/',index),
    path('person/', person),
    path('login/',login),
    path('persons/', PersonAPI.as_view())
]
