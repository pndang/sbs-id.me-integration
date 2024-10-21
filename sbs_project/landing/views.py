from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from .forms import UserInfoForm
from .data_storage import StoreData
import requests
import jwt 
import csv
import os
import json

import pandas as pd
import pytz
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Create your views here.

client_id = settings.IDME_CLIENT_ID
client_secret = settings.IDME_CLIENT_SECRET
redirect_uri = settings.IDME_REDIRECT_URI

def idme_callback(request):

    """
    Handle callback from ID.me, extract the auth code, and get user info.

    """

    authCode = request.GET.get('code')
    if authCode:

        print(f'Authorization code: {authCode}\n')

        tokenPayloadURL = "https://api.id.me/oauth/token"
        # "https://api.id.me/oauth/token"
        # "https://api.idmelabs.com/oauth/token"

        payload = {
            'code': authCode,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        # exchange auth code for token payload
        response = requests.post(tokenPayloadURL, data=payload)

        if response.status_code == 200:
            tokenPayload = response.json()
            print(f'Token payload: {tokenPayload}\n')

            idToken = tokenPayload['id_token']
            if idToken:
                decodedIDToken = jwt.decode(idToken, options={'verify_signature': False})
                print(f'Decoded id token: {decodedIDToken}\n')

                # initialize StoreData class and process payload
                data_storage = StoreData(decodedIDToken)

                # store data
                data_storage.save_to_database()

                # get user's first name
                firstName = decodedIDToken.get('fname', 'User')

                # redirect to welcome page
                # return redirect(reverse('welcome_page') + f"?first_name={firstName}")

                # redirect to 3rd-party ux solution
                return redirect("https://shorturl.at/qNeQO")
            else:
                return JsonResponse({'error': 'ID token not found in the token payload.'}, status=400)
        
        return JsonResponse({'error': 'Failed to retrieve the token payload.'}, status=response.status_code)

    return JsonResponse({'error': 'Authentication failed. Authorization code not returned or invalid.'}, status=400)

def landing_page(request):

    """
    Home page at launch, retrieves and store user input data.

    """

    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():

            # save data to csv
            userInfo = form.cleaned_data
            filePath = os.path.join('data', 'user_info.csv')
            fileExists = os.path.isfile(filePath)
            os.makedirs(os.path.dirname(filePath), exist_ok=True)

            with open(filePath, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=userInfo.keys())
                if not fileExists:
                    writer.writeheader()
                writer.writerow(userInfo)

            return redirect('success')
    else:
        form = UserInfoForm()

    context = {
        'form': form,
        'idme_client_id': client_id,
        'idme_redirect_uri': redirect_uri,
    }

    return render(request, 'landing/landing_page.html', context)

def success_page(request):

    """
    Success page after successful ID.me authentication (no longer used).

    """

    return render(request, 'landing/success_page.html')

def welcome_page(request):

    """
    Success/Welcome page after successful ID.me authentication.

    """

    firstName = request.GET.get('first_name', 'User')

    if request.method == 'POST':
        # process user choices from welcome page
        arrivalType = request.POST.get('arrival_type', None)
        POE = request.POST.get('port_of_arrival', None)

        # go to calendar view for booking if scheduled arrival
        if arrivalType == 'Scheduled' and POE:

            context = {
                'first_name': firstName,
                'arrival_type': arrivalType,
                'port_of_arrival': POE,
            }

            # return render(request, 'landing/calendar_view.html', context)

            return redirect(f"{reverse('calendar_view')}?first_name={firstName}&arrival_type={arrivalType}&port_of_arrival={POE}")

    context = {
        'first_name': firstName,
    }

    return render(request, 'landing/welcome_page.html', context)

def calendar_view(request):
    
    """
    Display available times for booking in a calendar.
    Only show timestamps with status "open" from "calendar.csv". 

    """

    BOOKING_WINDOW = 5

    # get user's poe selections
    POE = request.GET.get('port_of_arrival')

    # load the csv file for availability
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, 'data', 'calendar.csv')

    # read data
    df = pd.read_csv(path)

    # filter based on user selections ('open' poe)
    df = df[(df['status'] == 'open') & (df['poe'] == POE)]

    # convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC').dt.tz_convert('America/Tijuana')

    # get today's date and limit to next 5 days
    today = datetime.now(pytz.timezone('America/Tijuana')).date()
    end = today + pd.Timedelta(days=BOOKING_WINDOW)
    df = df[df['timestamp'].dt.date.between(today, end)]

    # store in dict to organize by day
    # availability = df.groupby(df['timestamp'].dt.date)['timestamp'].apply(list).to_dict()
    availability = {}
    for date, times in df.groupby(df['timestamp'].dt.date)['timestamp']:
        date_str = date.strftime('%Y-%m-%d')

        time_list = [time.strftime('%H:%M:%S') for time in times]
        availability[date_str] = time_list

    # Write availability to a text file for debugging
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    debug_file_path = os.path.join(base_dir, 'data', 'availability_debug.txt')
    with open(debug_file_path, 'w') as debug_file:
        debug_file.write(json.dumps(availability, indent=4))

    # make a list of current month's dates
    first = today.replace(day=1)
    last = (today.replace(day=28) + pd.Timedelta(days=4)).replace(day=1) - pd.Timedelta(days=1)
    dates = pd.date_range(first, last, freq='D').date

    # Convert dates to `datetime.date` to match the [availability] keys
    # dates = [date.date() for date in dates]

    earliest_available = min(availability.keys())

    context = {
        'availability': json.dumps(availability),
        'all_days_in_month': dates,
        'port_of_arrival': POE,
        'today': today,
        'earliest_available': earliest_available
    }

    # logger.debug(f"Context data: {context}")

    return render(request, 'landing/calendar_view.html', context)

def confirmation_page(request):

    """
    Render the confirmation page after the user selects their arrival type and port of entry.
    """

    first_name = request.GET.get('first_name', 'User')
    arrival_type = request.GET.get('arrival_type')
    port_of_arrival = request.GET.get('port_of_arrival')

    context = {
        'first_name': first_name,
        'arrival_type': arrival_type,
        'port_of_arrival': port_of_arrival,
    }

    return render(request, 'landing/confirmation_page.html', context)

def neg_avai_page(request):

    """
    Demo page in case of negative availability given a user's preferences.

    """

    return render(request, 'landing/neg_avai_page.html')

def virtual_line_page(request):

    """
    Demo virtual wait line during negative availability.

    """

    return render(request, 'landing/virtual_line_page.html')