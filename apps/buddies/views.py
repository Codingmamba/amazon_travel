from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import logout
from datetime import datetime
from time import gmtime, strftime, localtime
from .models import *

# Rendered HTML Templates
def index(request):
    return render(request, 'buddies/index.html')

def travels(request):
    context = {
        "mines": Trip.objects.filter(id=request.session['user_id']).all(),
        "trips": User.objects.get(id=request.session['user_id']).trips.all(),
        'others': Trip.objects.exclude(uploader__id=request.session['user_id']).all()
    }
    return render(request, 'buddies/travels.html', context)

def addPlan(request):
    return render(request, 'buddies/addPlan.html')


def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    print request.POST
    result = User.objects.validate_reg(request.POST)
    if result[0]:

        request.session['user_id'] = result[1].id
        request.session['user_name'] = result[1].name
        return redirect('/travels')
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)

        return redirect('/')


def login(request):
    result = User.objects.validate_log(request.POST)
    if result[0]:

        request.session['user_id'] = result[1].id
        print "THE ID:", request.session['user_id']
        request.session['user_name'] = result[1].name
        print "THE NAME:", request.session['user_name']
        return redirect('/travels')
    else:

        for error in result[1]:
            messages.add_message(request, messages.INFO, error)

        return redirect('/')

# Form Validation
def newTripSubmit(request):
    destination = request.POST['destination']
    description = request.POST['description']
    datefrom = request.POST['datefrom']
    dateto = request.POST['dateto']
    print destination
    print description
    print datefrom
    print dateto
    print strftime("%Y-%m-%d", gmtime())

    if len(destination) <= 0:
        messages.warning(request, 'Please enter in an Destination')
        return redirect('/travels/add')

    elif len(description) <= 0:
        messages.warning(request, 'Please enter in an Description')
        return redirect('/travels/add')

    elif len(datefrom) <= 0:
        messages.warning(request, 'Please enter a Start Date')
        return redirect('/travels/add')

    elif len(dateto) <= 0:
        messages.warning(request, 'Please enter an End Date')
        return redirect('/travels/add')

    elif strftime("%Y-%m-%d", gmtime()) > datefrom:
        messages.warning(request, 'Travel Dates must be in the future')
        return redirect('/travels/add')
    elif datefrom > dateto:
        messages.warning(request, 'Travel Date To should not be before the Travel Date From')
        return redirect('/travels/add')
    else:
        Trip.objects.create(destination=destination, description=description, travel_from=datefrom, travel_to=dateto, uploader_id=request.session['user_id'])

        return redirect('/travels')


# Displaying results from the trip when they are selected
def tripDisplay(request, id):
    context = {
        "dest": Trip.objects.get(id = id),
        'users': Trip.objects.get(id=id).users.all()
    }
    return render(request, 'buddies/trip_display.html', context)


# When the users selectes 'Join'
def joinTrip(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    trip.users.add(user)
    return redirect('/travels')
