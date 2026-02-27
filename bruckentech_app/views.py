from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.db import connection
from django.db.utils import OperationalError
import logging

logger = logging.getLogger(__name__)

# simple views that render the corresponding template
# templates live under bruckentech_app/templates/bruckentech_app/


def _get_page_or_none(slug):
    """Safely get a page or return None if database is unavailable."""
    try:
        from .models import Page
        return Page.objects.filter(slug=slug, published=True).first()
    except OperationalError:
        logger.warning(f"Database unavailable when fetching page: {slug}")
        return None


def home(request):
    # prefer CMS page if available
    page = _get_page_or_none('home')
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/home.html')


def about_us(request):
    page = _get_page_or_none('about_us')
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/about_us.html')


def programs(request):
    page = _get_page_or_none('programs')
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/programs.html')


def agency(request):
    page = _get_page_or_none('agency')
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/agency.html')


def account_details(request):
    """Show foundation account details (bank / mobile money) for offline donations.

    Reads `ACCOUNT_DETAILS` from settings if available, otherwise shows
    placeholder information. This replaces the previously available
    online donation flow.
    """
    accounts = getattr(settings, 'ACCOUNT_DETAILS', None)
    if not accounts:
        accounts = {
            'bank': {
                'bank_name': 'Example Bank',
                'account_name': 'Brückentech Foundation',
                'account_number': '0000000000',
            },
            'mobile_money': {
                'provider': 'MTN Mobile Money',
                'number': '+256700000000',
                'account_name': 'Brückentech Foundation',
            }
        }

    return render(request, 'bruckentech_app/account_details.html', {
        'accounts': accounts,
    })


def articles_list(request):
    try:
        from .models import Article
        from django.db.models import Q

        q = request.GET.get('q', '').strip()
        qs = Article.objects.filter(published=True)
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(body__icontains=q) | Q(excerpt__icontains=q)
            )
        articles = qs.order_by('-published_at')
        return render(request, 'bruckentech_app/articles_list.html', {'articles': articles, 'q': q})
    except OperationalError:
        logger.error("Database unavailable for articles_list")
        return render(request, 'bruckentech_app/articles_list.html', {'articles': [], 'q': '', 'error': 'Database temporarily unavailable'})


def article_detail(request, slug):
    from .models import Article

    article = get_object_or_404(Article, slug=slug, published=True)
    return render(request, 'bruckentech_app/article_detail.html', {'article': article})


def action(request):
    page = _get_page_or_none('action')
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/action.html')


def impact_reports(request):
    page = _get_page_or_none('impact_reports')
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/impact_reports.html')


def join_mentor(request):
    # mentor applications form
    try:
        from .models import Page
        from .forms import MentorApplicationForm

        page = _get_page_or_none('join_mentor')
        if page:
            # if a CMS page exists we ignore the form (could enhance later)
            return render(request, 'bruckentech_app/page.html', {'page': page})

        success = False
        if request.method == "POST":
            form = MentorApplicationForm(request.POST)
            if form.is_valid():
                form.save()
                success = True
        else:
            form = MentorApplicationForm()

        return render(request, 'bruckentech_app/join_mentor.html', {
            'form': form,
            'success': success,
        })
    except OperationalError:
        logger.error("Database unavailable for join_mentor")
        # Return form anyway, but don't process submissions
        from .forms import MentorApplicationForm
        return render(request, 'bruckentech_app/join_mentor.html', {
            'form': MentorApplicationForm(),
            'success': False,
            'error': 'Application submission temporarily unavailable',
        })


def privacy_policy(request):
    from .models import Page
    page = Page.objects.filter(slug='privacy_policy', published=True).first()
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/privacy_policy.html')


def terms_of_service(request):
    from .models import Page
    page = Page.objects.filter(slug='terms_of_service', published=True).first()
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/terms_of_service.html')
