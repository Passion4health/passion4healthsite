from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Subscriber
from .serializers import SubscriberSerializer
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe  # Import mark_safe
from django.shortcuts import render

@api_view(['POST'])
def subscribe(request):
    serializer = SubscriberSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Check if the email already exists
        if Subscriber.objects.filter(email=email).exists():
            return Response({"detail": "This email is already subscribed."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the new subscriber if email doesn't exist
        Subscriber.objects.create(email=email)
        
        # Prepare email content
        subject = 'Thank you for email subscription'
        from_email = 'info@passion4health.org'
        recipient_list = [email]

        # Render the email template with dynamic content
        email_html_content = render_to_string('emails/base_email.html', {
            'email_content': mark_safe('Thank you for subscribing to our newsletter!'),  # Mark as safe
            'email_action_button': mark_safe('<a href="https://passion4health.org/learn-more" class="button">Learn More</a>'),  # Mark as safe
        })

        # Send the email
        msg = EmailMessage(subject, email_html_content, from_email, recipient_list)
        msg.content_subtype = 'html'  # Set the email content type to HTML
        msg.send()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def adminindex(request):
    subscribers = Subscriber.objects.all()

    return render(request, 'wagtailsubscribers/index.html', {
        'subscribers': subscribers
    })
