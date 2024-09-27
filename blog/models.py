from django.db import models

from base.blocks import HelloBlock
from django.db import models
from wagtail.fields import StreamField
from snippets.models import OurService
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet 
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from django.shortcuts import render

class BlogIndex(Page):
    def get_context(self, request):
        context = super().get_context(request)

        # Get all blog articles
        blogarticles = BlogAndNewsArticle.objects.live()

        # Check for a tag filter in the GET request
        tag_filter = request.GET.get('tag', None)
        if tag_filter:
            blogarticles = blogarticles.filter(tags__name=tag_filter)
            
        
            
        search_query = request.GET.get('search', None)
        if search_query:
            blogarticles = blogarticles.filter(
                models.Q(title__icontains=search_query) |  # Search in title
                models.Q(body__icontains=search_query)     # Search in body/description
            )
            
        paginator = Paginator(blogarticles, 2)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
            

        context['blogarticles'] = page_obj
        context['page_obj'] = page_obj
        context['all_tags'] = self.get_all_tags()  # Add all tags to the context for filtering
        

        return context

    @staticmethod
    def get_all_tags():
        """Return all unique tags from all blog and news articles, along with the number of times each tag is used."""
        return (
            BlogAndNewsArticle.objects.live()
            .values('tags__name')  # Group by the tag name
            .annotate(tag_count=models.Count('tags'))  # Count how many times each tag is used
            .order_by('-tag_count')  # Optional: order by the most used tags
        )

    
class BlogPageTag(TaggedItemBase):
    content_object =ParentalKey(
        'BlogAndNewsArticle',
        related_name = 'tagged_items',
        on_delete=models.CASCADE
    )
    
class BlogAndNewsArticle(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=False, null=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    parent_page_types = ['blog.BlogIndex']  # Restrict to BlogIndex as the parent
    
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image 
        else:
            return None
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        
        InlinePanel('gallery_images', label="Gallery images"),
    ]
    def serve(self, request):
        # Fetch the comments related to this article
        comments = self.comments.filter(parent__isnull=True)  # Top-level comments
        from .forms import CommentForm
        # Handle form submission
        if request.method == 'POST':
            
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.page = self
                comment.save()
                return HttpResponseRedirect(request.path)
        else:
            form = CommentForm()

        return render(request, self.get_template(request), {
            'page': self,
            'form': form,
            'comments': comments,
            
        })
    def get_comment_count(self):
        return self.comments.count()

    def get_comments(self):
        return self.comments.all().order_by('-created_at')
    
    def get_previous_article(self):
        """Get the previous article based on the date"""
        return BlogAndNewsArticle.objects.live().filter(date__lt=self.date).order_by('-date').first()

    def get_next_article(self):
        """Get the next article based on the date"""
        return BlogAndNewsArticle.objects.live().filter(date__gt=self.date).order_by('date').first()
    
    @staticmethod
    def get_all_tags():
        """Return all unique tags from all blog and news articles, along with the number of times each tag is used."""
        return (
            BlogAndNewsArticle.objects.live()
            .values('tags__name')  # Group by the tag name
            .annotate(tag_count=models.Count('tags'))  # Count how many times each tag is used
            .order_by('-tag_count')  # Optional: order by the most used tags
        )
        
class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogAndNewsArticle, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)
    
    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
        
    )
    panels = [
        FieldPanel('name'),
        FieldPanel('author_image')
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Authors"

class BlogTagIndexPage(Page):
    
    def get_context(self, request):
        tag = request.GET.get('tag')
        blogarticles = BlogAndNewsArticle.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context['blogarticles'] = blogarticles
        return context
        
    
class Comment(models.Model):
    page = ParentalKey('BlogAndNewsArticle', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.name}"

    def is_reply(self):
        return self.parent is not None