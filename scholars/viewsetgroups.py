from wagtail.snippets.views.snippets import SnippetViewSetGroup
from .viewsets import ScholarsProgramViewSet, CohortViewSet

class ScholarsViewSetGroup(SnippetViewSetGroup):
    items = (ScholarsProgramViewSet, CohortViewSet)
    menu_icon = "folder-inverse"
    menu_label = "Scholars"
    menu_name = "scholars"