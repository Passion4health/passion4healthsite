from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable

class ScholarsProgram(models.Model):
    title = models.CharField(blank=False, null=False, verbose_name="title given to the program")
    description = models.TextField()
    burner_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+", verbose_name="Overview Burner",null=True, blank=True
    )
    target_number = models.PositiveIntegerField()
    final_year = models.PositiveIntegerField()

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('burner_image'),
        FieldPanel('target_number'),
        FieldPanel('final_year'),
    ]

    def __str__(self):
        return f"Edit the Scholars program details"
    
    def total_scholar_in_all_cohorts(self):
        cohorts = Cohort.objects.all()
        return sum(cohort.number_of_scholars for cohort in cohorts)
    def all_cohorts(sellf):
        return Cohort.objects.all()
class Cohort(ClusterableModel):
    name = models.CharField(max_length=255, verbose_name="Cohort Name", blank=False, null=True)
    description = models.TextField()
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Cohort Cover Image",
        null=True,
        blank=False
    )
    number_of_scholars = models.PositiveIntegerField()
    
    male_scholars = models.PositiveIntegerField(blank=False, null=True, default=0)
    female_scholars = models.PositiveIntegerField(blank=False, null=True, default=0)
    link_to_document = models.CharField(max_length=255, blank=True, null=True, verbose_name="Link to Document")

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('cover_image'),
        FieldPanel('number_of_scholars'),
        FieldPanel('male_scholars'),
        FieldPanel('female_scholars'),
        FieldPanel('link_to_document'),
        
        InlinePanel('cohort_gallery_images', label="Gallery Images"),
    ]

    def __str__(self):
        return self.name


class CohortImage(Orderable):
    cohort = ParentalKey(Cohort, on_delete=models.CASCADE, related_name='cohort_gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Cohort Image"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

    def __str__(self):
        return f"{self.cohort.name} - {self.caption}"