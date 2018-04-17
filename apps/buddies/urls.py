from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),

    url(r'^travels$', views.travels, name='travels'),
    url(r'^travels/add$', views.addPlan),
    url(r'^new/trip$', views.newTripSubmit),

    url(r'^travels/destination/(?P<id>\d+)$', views.tripDisplay, name='trip_display'),
    url(r'^join/new/trip/(?P<id>\d+)$', views.joinTrip, name='joinTrip'),
]
