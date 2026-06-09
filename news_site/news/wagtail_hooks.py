from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import NewsAuthor, NewsCategory


class NewsCategoryViewSet(SnippetViewSet):
    model = NewsCategory
    menu_label = "Categories"
    icon = "tag"
    list_display = ["name", "slug", "color"]


class NewsAuthorViewSet(SnippetViewSet):
    model = NewsAuthor
    menu_label = "Authors"
    icon = "user"
    list_display = ["name", "role"]


class NewsSnippetGroup(SnippetViewSetGroup):
    menu_label = "News"
    menu_icon = "newspaper"
    menu_order = 200
    items = [NewsCategoryViewSet, NewsAuthorViewSet]


register_snippet(NewsSnippetGroup)
