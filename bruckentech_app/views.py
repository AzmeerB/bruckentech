from django.shortcuts import render, get_object_or_404
from django.conf import settings

# simple views that render the corresponding template
# templates live under bruckentech_app/templates/bruckentech_app/


def home(request):
    # prefer CMS page if available
    from .models import Page
    page = Page.objects.filter(slug='home', published=True).first()
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/home.html')


def about_us(request):
    from .models import Page
    page = Page.objects.filter(slug='about_us', published=True).first()
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/about_us.html')


def programs(request):
    from .models import Page
    page = Page.objects.filter(slug='programs', published=True).first()
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/programs.html')


def agency(request):
    from .models import Page
    page = Page.objects.filter(slug='agency', published=True).first()
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


def article_detail(request, slug):
    from .models import Article

    article = get_object_or_404(Article, slug=slug, published=True)
    return render(request, 'bruckentech_app/article_detail.html', {'article': article})


def action(request):
    from .models import Page
    page = Page.objects.filter(slug='action', published=True).first()
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/action.html')


def impact_reports(request):
    from .models import Page
    page = Page.objects.filter(slug='impact_reports', published=True).first()
    if page:
        return render(request, 'bruckentech_app/page.html', {'page': page})
    return render(request, 'bruckentech_app/impact_reports.html')


def join_mentor(request):
    # mentor applications form
    from .models import Page
    from .forms import MentorApplicationForm

    page = Page.objects.filter(slug='join_mentor', published=True).first()
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
