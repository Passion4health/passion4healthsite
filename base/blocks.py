from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
    ListBlock,
    EmailBlock,
    IntegerBlock,
    
)

from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import PageChooserBlock

from wagtail.images.widgets import AdminImageChooser
import os
from django.core.exceptions import ValidationError

# this class overide the imagechooserblock to allow only icon chooser block
class IconChooserBlock(ImageChooserBlock):
    def __init__(self, *args, **kwargs):
        self.target_collection = 'icons'
        super().__init__(*args, **kwargs)
        
    def get_form_class(self):
         # Override the widget to filter by collection
         form_class = super.get_form_class()
         form_class.base_fields['image'].widget = AdminImageChooser(collection=self.target_collection)
         return form_class
    
    
     
# Define a CTA button block
class CTAButtonBlock(StructBlock):
    button_text = CharBlock(required=True, max_length=50, help_text="Text to display on the button")
    button_link = PageChooserBlock(required=True, help_text="The page the button links to")
    button_color = ChoiceBlock(
        choices=[
            ('primary', 'Primary'),
            ('transparent', 'Transparent'),
        ],
        required=True,
        help_text="Choose the color of the button",
    )

    class Meta:
        icon = 'link'
        label = 'CTA Button'
        template = 'blocks/cta_button_block.html'  # You can define a custom template if needed

class HelloBlockStruct(StructBlock):
    hero_text = CharBlock(
        classname="title",
        required=True,
        help_text="Write the main display text"
        )
    bg_img = ImageChooserBlock(
        required=False
        )
    sub_text = CharBlock(
        required=False,
        help_text="Add sub text to the main Hero Text"
        )
    cta_buttons = ListBlock(
        CTAButtonBlock(),
        min_num=1,
        max_num=5,
        required=False,
        help_text="Add more call-to-action buttons"
    )
    class Meta:
        template = 'blocks/hero_block.html'
        icon = "image"
        label = "Hero Block"
    
class HelloBlock(StreamBlock):
    templated = HelloBlockStruct()
    
    
# Let's now do about the ourservices snippet
class ServicesBlockStructItem(StructBlock):
    name = CharBlock(
        required=True, 
        max_length=50,
        help_text="The name of the service ",
        )
    short_description = CharBlock(
        required=True, 
        max_length=250,
        help_text="A short description of the service!",
        )
    icon_image = IconChooserBlock(required=True)
    
class ServicesBlockStruct(StructBlock):
    snippet_title = CharBlock(
        required=True,
        max_length=250,
        help_text="Write the title for the Services"
    )
    snippet_description = CharBlock(
        required=True,
        max_length=250,
        help_text="Write the something about the Services"
    )
    services = ListBlock(
        ServicesBlockStructItem(),
        min_num=1,
        max_num=3,
        required=False,
        help_text="Add the main services"
    )
    
    class Meta:
        template = "blocks/servicelist.html"
        icon = "clipboard-list"
    
class ServicesBlock(StreamBlock):
    templated = ServicesBlockStruct()
    

class OverlappingImageStruct(StructBlock):
    image_1 = ImageChooserBlock(required=True)
    image_2 = ImageChooserBlock(required=True)
    
    class Meta:
        template = "blocks/overlappingimage.html"
        icon = "image"
        
        
class OverlappingImage(StreamBlock):
    templated = OverlappingImageStruct()
    
class coreTeamOneMember(StructBlock):
    
    picture = ImageChooserBlock(
        max_num = 1,
        required=True
    )
    first_name = CharBlock(
        required=True,
        max_length=255
    )
    second_name = CharBlock(
        required=True,
        max_length=255
    )
    email = EmailBlock(
        required=True
    )
    phone = CharBlock(
        min_length=10,
        required=True
    )
    linkedIn = URLBlock(
        required=False,
    )
    role = CharBlock(
        max_length=30,
        required=True
    )
    
class coreTeamBlockStruct(StructBlock):
    block_title = CharBlock(
        required=True,
    )
    title = CharBlock(
        required=True,
    )
    members = ListBlock(
        coreTeamOneMember(),
        max_num = 5
    )
    class Meta:
        icon = "user"
        template = "blocks/coreTeam.html"
        
class coreTeamBlock(StreamBlock):
    templated = coreTeamBlockStruct()
    
    
class CallForVolunteerStruct(StructBlock):
    textshow = CharBlock(
        required=True,
        verbose_name="the message to display on the 'Become a volunteer section'",
        max_num =1
    )
    action_page = PageChooserBlock(
        target_model='base.VolunteerJoinPage',  # Restrict to VolunteerJoinPage only
        required=True,
        verbose_name="The page where the volunteer registration form will be",
        max_num=1
    )
    background_image = ImageChooserBlock(
        required=True,
        verbose_name="this image will be in the background section of the page.",
    )
    class Meta:
        icon = "tick-inverse"
        template = "blocks/callforvolunteer.html"
        
class CallForVolunteerBlock(StreamBlock):
    templated = CallForVolunteerStruct()
    
class DonationsFundScholarsStruct(StructBlock):
    donations = IntegerBlock(
        required=True,
        help_text="Number of received donations",
        
    )
    funds = IntegerBlock(
        required=True,
        help_text="The amount raised, in US dollars!"
    )
    scholars = IntegerBlock(
        required=True,
        help_text="Number of scholars in the project"
    )
    background_image = ImageChooserBlock(
        required=True,
        help_text="This the image that will be the background of the section."
    )
    class Meta:
        icon = "list-ol"
        template = "blocks/donationfundscholars.html"
        
        
class DonationsFundScholarsBlock(StreamBlock):
    tamplated = DonationsFundScholarsStruct()
    
class SimpleHeroBlockStruct(StructBlock):
    welcome_text = CharBlock(
        required=True,
        help_text="This title will display on the page welcome section!",
        max_num = 1,
        )

    class Meta:
        template = "blocks/simpleheroblock.html"
        icon = "title"  # Optional: choose an icon for the block
        label = "Auto Title"
        
class SimpleHeroBlock(StreamBlock):
    templated = SimpleHeroBlockStruct()
    
class MoreAboutStruct(StructBlock):
    section_title = CharBlock(
        required=True,
        max_num=1,
        help_text="Title to display on the section"
    )
    main_title = CharBlock(
        required=True,
        max_num=1,
        help_text="Titlte to display on the section"
    )
    class Meta:
        template = "blocks/simpleheroblock.html"
        icon = "title"  # Optional: choose an icon for the block
        label = "Auto Title"
    

    