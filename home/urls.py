from django.urls import path
from .views import create_token, doctor_list, fetch_time_list, fetch_slot_list


urlpatterns = [
    path('', create_token, name='token-booking'),
    path('doctor_list/', doctor_list, name='doctor_list'),
    path('fetch_time_list/', fetch_time_list, name='fetch_time_details'),
    path('fetch_slot_list/', fetch_slot_list, name='fetch_slot_list'),
]