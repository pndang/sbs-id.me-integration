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

        tokenPayloadURL = "https://api.idmelabs.com/oauth/token"

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
                data_storage.save_json()
                data_storage.save_csv()

                # get user's first name
                firstName = decodedIDToken.get('fname', 'User')

                # redirect to welcome page
                return redirect(reverse('welcome_page') + f"?first_name={firstName}")
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
        'idme_client_id': settings.IDME_CLIENT_ID,
        'idme_redirect_uri': settings.IDME_REDIRECT_URI,
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
    context = {
        'first_name': firstName,
    }
    return render(request, 'landing/welcome_page.html', context)
