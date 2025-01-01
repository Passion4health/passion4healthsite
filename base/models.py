from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.fields import RichTextField
# Create your models here.

from wagtail.admin.panels import(
    FieldPanel,
    MultiFieldPanel,
    FieldRowPanel,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from base.blocks import SimpleHeroBlock
from wagtail.fields import StreamField
class ReadOnlyPanel(FieldPanel):
    def clone(self):
        return self.__class__(self.field_name, widget=self.widget)

    def on_form_bound(self):
        super().on_form_bound()
        if self.bound_field:
            self.bound_field.field.widget.attrs['disabled'] = 'disabled'


@register_setting
class SiteSettings(BaseGenericSetting):
    site_name = models.CharField(verbose_name="Display Name", blank=False, max_length=250)
    short_name = models.CharField(verbose_name="Short Name", blank=True, max_length=10)
    org_name = models.CharField(verbose_name="Organization Name", blank=False, max_length=250)
    
    # Logos and Icons
    
    rectangle_logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+", verbose_name="Rectangle Logo",null=True, blank=True
    )
    square_logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+", verbose_name="Square Logo",null=True, blank=True
    )
    icon_logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+", verbose_name="Icon Logo", null=True, blank=True
    )
    inverted_rectangle_logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+", verbose_name="Inverted color Rectangle Logo",null=True, blank=True
    )
    
    
    
    
    # social media
    Facebook = models.URLField(verbose_name="Facebook Page", blank=True)
    Instagram = models.URLField(verbose_name="Instragram", blank=True)
    LinkedIn = models.URLField(verbose_name="LinkedIn", blank=True)
    Twitter = models.URLField(verbose_name="X (formaly Twitter)", blank=True)
    
    # contact name
    
    email = models.EmailField(verbose_name="General Email Address", blank=True)
    telephone = models.CharField(verbose_name="General Telephone line", blank=True, max_length=20)
    location_address = models.CharField(verbose_name="Loaction of the organization", blank=True, max_length=250)
    street_address = models.CharField(verbose_name="Street address of the organization", blank=True, max_length=250)
    
    # Donate Page Settings
    donate_button_text = models.CharField(
        max_length=100, 
        verbose_name="Donate Button Text", 
        help_text="Text for the donate button", 
        blank=True, 
        null=True
    )
    donate_page = models.ForeignKey(
        'DonatePage', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='+',
        verbose_name="Choose the donate page"
    )
    
    # system email settings
    email_common_message = models.CharField(
        max_length=100, 
        help_text="This message will be shown at the buttom of every system sent emails", 
        blank=True, 
        null=True
    )
    email_bunner_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+", verbose_name="Email bunner Image",null=True, blank=True
    )
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("site_name"),
                FieldPanel("short_name"),
                FieldPanel("org_name"),
            ],
            "Site Info",
        ),
        MultiFieldPanel(
            [
                FieldPanel("location_address"),
                FieldPanel("street_address"),
                FieldPanel("email"),
                FieldPanel("telephone"),
            ],
            "Contact Info",
        ),
        MultiFieldPanel(
            [
                FieldPanel("Facebook"),
                FieldPanel("Instagram"),
                FieldPanel("Twitter"),
                FieldPanel("LinkedIn"),
            ],
            "Social Media Links",
        ),
        MultiFieldPanel(
            [
                FieldPanel('rectangle_logo'),
                FieldPanel('square_logo'),
                FieldPanel('icon_logo'),
                FieldPanel('inverted_rectangle_logo'),
            ],
            "Logo settings"
        ),
        MultiFieldPanel(
            [
                FieldPanel("donate_button_text"),
                FieldPanel("donate_page"),  # Allows selecting the donate page
            ],
            "Donate Page Settings",
        ),
        MultiFieldPanel(
            [
                FieldPanel("email_common_message"),
                FieldPanel("email_bunner_image"),
            ],
            "System email settings",
        )
    ]
    
# class LogoGalleryImage(Orderable):
#     logo = ParentalKey(SiteSettings, on_delete=models.CASCADE, related_name="logo_images")
#     image = models.ForeignKey(
#         'wagtailimages.Image', on_delete=models.CASCADE, related_name="+"
#     )
#     caption = models.CharField(blank=True, max_length=250)
    
#     panels = [
#         FieldPanel('image'),
#         FieldPanel('caption'),
#     ]
    
class AboutPage(Page):
    hero_block = StreamField(
        SimpleHeroBlock(),
        blank=True,
        use_json_field=True,
        help_text="Block for Hello Section",
        null=True,
        max_num = 1,
    )
    whyproject = models.ForeignKey(
        'snippets.WhyProjectSection',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    our_services = models.ForeignKey(
        'snippets.OurService',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    donations_funds_and_scholars = models.ForeignKey(
        'snippets.DonationsFundsAndScholars',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel("hero_block"),
        FieldPanel('whyproject'),
        FieldPanel('our_services'),
        FieldPanel("donations_funds_and_scholars"),
    ]
    

class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    response_message = models.TextField(blank=True, null=True)
    responded = models.BooleanField(default=False)

    # Define the admin interface panels
    panels = [
        MultiFieldPanel([
            FieldPanel('name', classname='full', read_only=True),
            FieldPanel('email', classname='full', read_only=True),
            FieldPanel('subject', classname='full', read_only=True),
            FieldPanel('message', classname='full', read_only=True),
        ], heading="Message details"),
        MultiFieldPanel([
            FieldPanel('response_message', classname='full', ),
        ], heading="Respond to the Message"),
    ]

    def __str__(self):
        return f"Message from {self.name}"
    
    def save(self, *args, **kwargs):
        # If the object is new (first-time save), send a submission notification email
        if not self.pk:
            self.send_submission_email()
        
        # If there's a response message and it's the first time being saved, send response email
        if self.response_message and not self.responded:
            self.responded = True
            self.send_response()

        super().save(*args, **kwargs)

    def send_submission_email(self):
        """Send an email to the user confirming receipt of the message."""
        email_subject = "Thank you for contacting us!"
        from_email = 'info@passion4health.org'
        recipient_list = [self.email]

        # Render the email template
        email_html_content = render_to_string('emails/base_email.html', {
            'email_content': mark_safe(f"Dear {self.name}, thank you for reaching out! We have received your message: <br><hr>\"{self.message}\"."),
        })

        # Send the email
        send_mail(
            subject=email_subject,
            message='',  # Fallback for plain text email
            html_message=email_html_content,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

    def send_response(self):
        """Send an email response to the client with the admin's response message."""
        email_subject = f"Re: {self.subject}"
        from_email = 'info@passion4health.org'
        recipient_list = [self.email]

        # Render the response email template
        email_html_content = render_to_string('emails/base_email.html', {
            'email_content': mark_safe(f"Dear {self.name}, here is our response to your message: <br><hr>\"{self.response_message}\"."),
        })

        # Send the response email
        send_mail(
            subject=email_subject,
            message='',  # Fallback for plain text email
            html_message=email_html_content,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    
class ContactUs(Page):
    hero_block = StreamField(
        SimpleHeroBlock(),
        blank=True,
        use_json_field=True,
        help_text="Block for Hello Section",
        null=True,
        max_num = 1,
    )
    content_panels = Page.content_panels + [
        FieldPanel("hero_block"),
    ]
    
class DonatePage(Page):
    donate_page_title = models.CharField(
        blank=False,
        max_length=255,
        null=True,
    )
    donate_message = models.CharField(
        blank=False,
        max_length=255,
        null=True
    )
    
    # Instead of external link, now we use a field for embedding HTML donation forms
    donation_embed_code = models.TextField(
        blank=True,
        null=True,
        verbose_name="Donation Embed Code",
        help_text="Paste your donation form HTML from donorbox.org or similar service here."
    )
    
    # Reference to the ContactUs page
    contact_us_page = models.ForeignKey(
        'ContactUs',  # The model class for the ContactUs page
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Contact Us Page"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("donate_page_title"),
                FieldPanel("donate_message"),
                FieldPanel("donation_embed_code"),  # New panel for HTML embed
                FieldPanel("contact_us_page"),
            ],
            heading="It is better if this page is edited by a developer!"
        ),
    ]
class VolunteerJoinPage(Page):
    volunteer_section_title = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        help_text="Secondary title for the volunteer page"
    )
    volunteership_message = RichTextField(
        blank=False,
        null=True,
        help_text="A short message to attract volunteers"
    )
    form_link = models.URLField(
        blank=False,
        null=True,
        help_text="External URL link to the form (e.g. Google Form)"
    )
    button_text = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        help_text="Text displayed on the form link button"
    )

    content_panels = Page.content_panels + [
        FieldPanel("volunteer_section_title"),
        FieldPanel("volunteership_message"),
        FieldPanel("form_link"),
        FieldPanel("button_text"),
    ]
    