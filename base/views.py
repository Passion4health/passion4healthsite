# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ContactFormSerializer
import requests
from django.conf import settings  # Assuming  store  reCAPTCHA secret key in settings

@api_view(['POST'])
def contact_form_submission(request):
    # Retrieve the reCAPTCHA token from the request data
    recaptcha_token = request.data.get('recaptcha_token')
    
    # Check if the reCAPTCHA token is provided
    if not recaptcha_token:
        return Response({'error': 'Missing reCAPTCHA token'}, status=status.HTTP_400_BAD_REQUEST)

    # Prepare the request for verifying the reCAPTCHA token with Google's API
    recaptcha_secret_key = settings.RECAPTCHA_SECRET_KEY  # Store this in your Django settings
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    recaptcha_data = {
        'secret': recaptcha_secret_key,
        'response': recaptcha_token,
        'remoteip': request.META.get('REMOTE_ADDR')  # Optional: The user's IP address
    }

    # Make the request to verify the reCAPTCHA response
    recaptcha_response = requests.post(recaptcha_url, data=recaptcha_data)
    recaptcha_result = recaptcha_response.json()

    # Check the reCAPTCHA response
    if not recaptcha_result.get('success'):
        return Response({'error': 'Invalid reCAPTCHA. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)

    # If reCAPTCHA is valid, proceed with form submission
    serializer = ContactFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Optionally send a confirmation email here
        return Response({'message': 'Thank you for contacting us!'}, status=status.HTTP_201_CREATED)
    
    # If the form data is invalid, return the errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
