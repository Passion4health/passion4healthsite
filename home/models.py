from django.db import models

from wagtail.models import Page

from base.blocks import HelloBlock
from django.db import models
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from snippets.models import OurService
from blog.models import BlogAndNewsArticle
from scholars.models import ScholarsProgram

class HomePage(Page):
    hero_block = StreamField(
        HelloBlock(),
        blank=True,
        use_json_field=True,
        help_text="Block for Hello Section",
        null=True,
    )
    our_services = models.ForeignKey(
        'snippets.OurService',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    whyproject = models.ForeignKey(
        'snippets.WhyProjectSection',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    ourteam = models.ForeignKey(
        'snippets.OurTeam',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    call_for_volunteer = models.ForeignKey(
        'snippets.BecomeVolunteerSection',
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
        FieldPanel('our_services'),
        FieldPanel('whyproject'),
        FieldPanel('ourteam'),
        FieldPanel('call_for_volunteer'),
        FieldPanel('donations_funds_and_scholars'),
    ]
    def get_context(self, request):
        # Get the context from the superclass (Page)
        context = super().get_context(request)

        # Fetch the two latest blog articles
        articles = BlogAndNewsArticle.objects.live().order_by('-first_published_at')[:2]
        
        # Add the articles to the context
        context['blog_articles'] = articles
        
        # Let us get the context of SCholars Program
        scholars_program = ScholarsProgram.objects.all()
        context['scholars_program'] = scholars_program
        
        return context
