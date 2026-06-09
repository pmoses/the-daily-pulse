from django.db import models
from django.utils import timezone

from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    color = models.CharField(
        max_length=20,
        default="red",
        help_text="Tailwind color name (e.g. red, blue, emerald, amber)",
    )
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("color"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class NewsAuthor(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=100, blank=True, default="Reporter")
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("bio"),
        FieldPanel("photo"),
    ]

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["name"]

    def __str__(self):
        return self.name


class NewsIndexPage(Page):
    """The main news index / home page."""

    tagline = models.CharField(max_length=300, blank=True, default="Your source for breaking news and in-depth stories")

    content_panels = Page.content_panels + [
        FieldPanel("tagline"),
    ]

    subpage_types = ["news.NewsArticlePage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_articles = (
            NewsArticlePage.objects.live()
            .descendant_of(self)
            .order_by("-first_published_at")
            .select_related("author")
            .prefetch_related("categories")
        )
        context["featured_article"] = all_articles.filter(featured=True).first()
        context["breaking_articles"] = all_articles.filter(breaking=True)[:5]
        context["latest_articles"] = all_articles[:12]
        context["categories"] = NewsCategory.objects.all()
        return context

    class Meta:
        verbose_name = "News Index Page"


class NewsArticlePage(Page):
    """An individual news article."""

    summary = models.TextField(blank=True)
    body = RichTextField()
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    author = models.ForeignKey(
        NewsAuthor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles",
    )
    categories = ParentalManyToManyField(NewsCategory, blank=True)
    reading_time = models.PositiveIntegerField(default=3, help_text="Estimated reading time in minutes")
    featured = models.BooleanField(default=False, help_text="Show in the featured slot on the home page")
    breaking = models.BooleanField(default=False, help_text="Mark as breaking news")
    published_date = models.DateTimeField(default=timezone.now)

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("body"),
        index.FilterField("first_published_at"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("body"),
        FieldPanel("hero_image"),
        MultiFieldPanel(
            [
                FieldPanel("author"),
                FieldPanel("categories"),
                FieldPanel("reading_time"),
                FieldPanel("published_date"),
            ],
            heading="Article Details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("featured"),
                FieldPanel("breaking"),
            ],
            heading="Flags",
        ),
    ]

    parent_page_types = ["news.NewsIndexPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        related = (
            NewsArticlePage.objects.live()
            .exclude(pk=self.pk)
            .filter(categories__in=self.categories.all())
            .distinct()
            .order_by("-first_published_at")[:3]
        )
        context["related_articles"] = related
        return context

    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
