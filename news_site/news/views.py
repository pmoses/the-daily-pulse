import json
from django.http import StreamingHttpResponse
from django.template.loader import render_to_string

from .models import NewsArticlePage, NewsCategory


def _sse_fragments(html: str, selector: str, merge_mode: str = "inner") -> str:
    """Build a Datastar SSE merge-fragments event string."""
    compact = " ".join(html.split())
    return (
        f"event: datastar-merge-fragments\n"
        f"data: selector {selector}\n"
        f"data: mergeMode {merge_mode}\n"
        f"data: fragments {compact}\n\n"
    )


def _sse_signals(signals: dict) -> str:
    """Build a Datastar SSE merge-signals event string."""
    return (
        f"event: datastar-merge-signals\n"
        f"data: signals {json.dumps(signals)}\n\n"
    )


def search_articles(request):
    """
    Datastar SSE endpoint — returns article grid and pagination signals.
    Signals sent by Datastar: query, category, page (as GET params).
    """
    query = request.GET.get("query", "").strip()
    category_slug = request.GET.get("category", "all").strip()
    page_num = max(1, int(request.GET.get("page", 1) or 1))
    per_page = 9

    articles_qs = (
        NewsArticlePage.objects.live()
        .order_by("-first_published_at")
        .select_related("author")
        .prefetch_related("categories")
    )

    if query:
        articles_qs = articles_qs.search(query)
    elif category_slug and category_slug != "all":
        articles_qs = articles_qs.filter(categories__slug=category_slug)

    total = articles_qs.count()
    start = (page_num - 1) * per_page
    articles = list(articles_qs[start : start + per_page])
    has_more = total > start + per_page
    total_pages = (total + per_page - 1) // per_page

    grid_html = render_to_string(
        "news/partials/article_grid.html",
        {
            "articles": articles,
            "query": query,
            "category": category_slug,
            "page_num": page_num,
            "has_more": has_more,
            "total": total,
        },
        request=request,
    )

    def generate():
        yield _sse_signals({"totalResults": total, "hasMore": has_more, "currentPage": page_num})
        yield _sse_fragments(grid_html, "#article-grid", "outer")

    response = StreamingHttpResponse(generate(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
