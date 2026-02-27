from django.shortcuts import render, get_object_or_404
from django.conf import settings

# simple views that render the corresponding template
# templates live under bruckentech_app/templates/bruckentech_app/


def home(request):
    return render(request, 'bruckentech_app/home.html')


def about_us(request):
    return render(request, 'bruckentech_app/about_us.html')


def programs(request):
    return render(request, 'bruckentech_app/programs.html')


def agency(request):
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
    return render(request, 'bruckentech_app/action.html')


def impact_reports(request):
    return render(request, 'bruckentech_app/impact_reports.html')


def join_mentor(request):
    return render(request, 'bruckentech_app/join_mentor.html')


def privacy_policy(request):
    return render(request, 'bruckentech_app/privacy_policy.html')


def terms_of_service(request):
    return render(request, 'bruckentech_app/terms_of_service.html')
