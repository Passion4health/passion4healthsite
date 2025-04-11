from wagtail.snippets.views.snippets import SnippetViewSet
from .models import ScholarsProgram, Cohort

class ScholarsProgramViewSet(SnippetViewSet):
    model = ScholarsProgram
    icon = "form"
    menu_label = "Overview"
    menu_name = "overview"
    menu_order = 101
    list_display = ['description', 'burner_image', 'target_number', 'final_year']

class CohortViewSet(SnippetViewSet):
    model = Cohort
    icon = "group"
    menu_label = "Cohorts"
    menu_name = "cohorts"
    menu_order = 102
    list_display = ['name', 'description', 'number_of_scholars']