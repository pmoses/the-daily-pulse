from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter
def category_color_class(color_name):
    """Map a color name to Tailwind badge classes."""
    mapping = {
        "red": "bg-red-100 text-red-700 border-red-200",
        "blue": "bg-blue-100 text-blue-700 border-blue-200",
        "emerald": "bg-emerald-100 text-emerald-700 border-emerald-200",
        "amber": "bg-amber-100 text-amber-700 border-amber-200",
        "purple": "bg-purple-100 text-purple-700 border-purple-200",
        "pink": "bg-pink-100 text-pink-700 border-pink-200",
        "cyan": "bg-cyan-100 text-cyan-700 border-cyan-200",
        "orange": "bg-orange-100 text-orange-700 border-orange-200",
        "indigo": "bg-indigo-100 text-indigo-700 border-indigo-200",
        "slate": "bg-slate-100 text-slate-700 border-slate-200",
    }
    return mapping.get(color_name, "bg-slate-100 text-slate-700 border-slate-200")


@register.filter
def time_ago(dt):
    if not dt:
        return ""
    now = timezone.now()
    if timezone.is_naive(dt):
        from django.utils.timezone import make_aware
        dt = make_aware(dt)
    delta = now - dt
    if delta < timedelta(minutes=1):
        return "just now"
    if delta < timedelta(hours=1):
        mins = int(delta.total_seconds() // 60)
        return f"{mins}m ago"
    if delta < timedelta(days=1):
        hours = int(delta.total_seconds() // 3600)
        return f"{hours}h ago"
    if delta < timedelta(days=7):
        days = delta.days
        return f"{days}d ago"
    return dt.strftime("%b %d, %Y")
