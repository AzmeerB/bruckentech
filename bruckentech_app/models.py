from django.db import models


class Donation(models.Model):
    tx_ref = models.CharField(max_length=128, unique=True)
    transaction_id = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # status: initiated before redirect, then successful/failed after verification
    status = models.CharField(
        max_length=32,
        choices=[
            ("initiated", "Initiated"),
            ("successful", "Successful"),
            ("failed", "Failed"),
        ],
        default="initiated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tx_ref} ({self.status})"
