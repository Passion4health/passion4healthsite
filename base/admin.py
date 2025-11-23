from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import ContactFormSubmission
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.helpers import ButtonHelper
from django.contrib import messages
from django.http import HttpResponseRedirect
from wagtail.admin import messages as wagtail_messages

class ContactFormButtonHelper(ButtonHelper):
    def edit_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.edit_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            "url": self.url_helper.get_action_url("edit", pk),
            "label": _("Respond"),
            "classname": cn,
            "title": _("Respond to this submission"),
        }

    def add_button(self, classnames_add=None, classnames_exclude=None):
        return None  # Hide the "Add" button
    
    # Custom delete all button
    def delete_all_button(self):
        return {
            "url": reverse("delete_all_submissions"),  # Custom URL for delete all
            "label": _("Delete All"),
            "classname": "button button-small button-danger",
            "title": _("Delete all messages"),
        }

class ContactFormSubmissionAdmin(ModelAdmin):
    model = ContactFormSubmission
    menu_label = "Inbox"
    menu_icon = "mail"
    list_display = ('name', 'email', 'subject', 'created_at', 'responded')
    search_fields = ('name', 'email', 'subject')
    button_helper_class = ContactFormButtonHelper
    
    def get_extra_buttons(self, *args, **kwargs):
        buttons = super().get_extra_buttons(*args, **kwargs)
        buttons.append(self.button_helper_class(self).delete_all_button())  # Add the delete all button
        return buttons

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-created_at')  # Default sorting by most recent

# Register the ModelAdmin class with Wagtail
modeladmin_register(ContactFormSubmissionAdmin)

# Custom view to delete all submissions
from django.http import HttpResponseRedirect
from django.urls import path

def delete_all_submissions(request):
    ContactFormSubmission.objects.all().delete()
    wagtail_messages.success(request, "All submissions have been deleted.")
    return HttpResponseRedirect(reverse('wagtailadmin_home'))

# Register the custom URL for deleting all submissions
from wagtail import hooks

@hooks.register('register_admin_urls')
def register_custom_admin_urls():
    return [
        path('delete_all_submissions/', delete_all_submissions, name='delete_all_submissions'),
    ]
