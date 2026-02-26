from django.shortcuts import render

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


import os
import time
import requests
from django.conf import settings
from django.shortcuts import redirect, render

from .models import Donation
from .flutterwave_utils import get_flutterwave_access_token


def donation(request):
    """Render a donation form or initiate a Flutterwave payment.

    The view accepts POST submissions with `amount` and `email`, then calls
    the Flutterwave v3 payments API to create a checkout link. On success the
    user is redirected to the hosted payment page. Any errors are shown back
    on the form.
    """

    if request.method == "POST":
        amount = request.POST.get("amount")
        email = request.POST.get("email")

        # minimal validation
        if not amount or not email:
            return render(request, 'bruckentech_app/donation.html', {
                'error': 'Please provide both amount and email',
            })

        tx_ref = f"bruckentech_{int(time.time())}"

        # record an initial donation object so we can update later
        Donation.objects.create(
            tx_ref=tx_ref,
            email=email,
            amount=amount,
            status="initiated",
        )

        payload = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": "USD",
            "redirect_url": request.build_absolute_uri(
                '/donation/complete/'
            ),
            "payment_options": "card",
            "customer": {"email": email, "name": ""},
            "customizations": {
                "title": "Support Bruckentech",
                "description": "Donation to Brückentech Foundation",
            },
        }

        try:
            # Get OAuth access token
            access_token = get_flutterwave_access_token()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            
            resp = requests.post(
                "https://api.flutterwave.com/v3/payments",
                json=payload,
                headers=headers,
                timeout=10,
            )
            data = resp.json()
        except Exception as exc:
            return render(request, 'bruckentech_app/donation.html', {
                'error': f'Payment request failed: {exc}',
            })

        if data.get('status') == 'success' and data.get('data'):
            return redirect(data['data']['link'])

        # show error from API
        return render(request, 'bruckentech_app/donation.html', {
            'error': data.get('message', 'unknown error'),
            'api_response': data,
        })

    return render(request, 'bruckentech_app/donation.html')


def donation_complete(request):
    """Handle the redirect back from Flutterwave after payment."""

    # Flutterwave will append ?status=successful&tx_ref=...&transaction_id=...
    status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')

    # try to update the corresponding donation record
    donation = None
    if tx_ref:
        donation = Donation.objects.filter(tx_ref=tx_ref).first()

    # verify with Flutterwave to be safe
    verified_status = None
    if transaction_id:
        try:
            # Get OAuth access token
            access_token = get_flutterwave_access_token()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
            }
            resp = requests.get(
                f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify",
                headers=headers,
                timeout=10,
            )
            vdata = resp.json()
            # actual status is in vdata['data']['status']
            verified_status = vdata.get('data', {}).get('status')
        except Exception:
            verified_status = None

    final_status = verified_status or status

    if donation:
        donation.transaction_id = transaction_id or donation.transaction_id
        donation.status = final_status or donation.status
        donation.save()

    context = {
        'status': final_status,
        'tx_ref': tx_ref,
        'transaction_id': transaction_id,
        'donation': donation,
    }
    return render(request, 'bruckentech_app/donation_complete.html', context)


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
