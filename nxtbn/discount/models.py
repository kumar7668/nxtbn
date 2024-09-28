from datetime import timedelta
from django.db import models
from nxtbn.users.models import User
from django.forms import ValidationError
from django.utils import timezone

from nxtbn.core.models import AbstractBaseModel
from nxtbn.discount import PromoCodeType
from nxtbn.order import OrderStatus
from nxtbn.product.models import Product


class PromoCode(AbstractBaseModel):
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    code_type = models.CharField(
        max_length=20,
        choices=PromoCodeType.choices,
        default=PromoCodeType.PERCENTAGE,
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 10 for 10%, or 10 for $10
    expiration_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    
    # New Fields
    specific_customers = models.ManyToManyField(
        User,
        through='PromoCodeCustomer',
        related_name='promo_codes',
        blank=True,
        help_text="Specify users who are eligible for this promo code."
    )
    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum total purchase amount required to use the promo code."
    )
    min_purchase_period = models.DurationField(
        null=True,
        blank=True,
        help_text="Time period (e.g., 30 days) within which the minimum purchase amount should be met."
    )
    applicable_products = models.ManyToManyField(
        Product,
        through='PromoCodeProduct',
        related_name='promo_codes',
        blank=True,
        help_text="Specify products that must be purchased to use the promo code."
    )
    redemption_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of times this promo code can be redeemed."
    )
    new_customers_only = models.BooleanField(
        default=False,
        help_text="If set, only newly registered customers can use this promo code."
    )
    usage_limit_per_customer = models.PositiveIntegerField(
        default=1,
        help_text="Maximum number of times a single customer can redeem this promo code."
    )
    
    def save(self, *args, **kwargs):
        # Ensure the code is in uppercase
        self.code = self.code.upper()
        super().save(*args, **kwargs)
    
    def is_valid(self, user=None):
        """
        Check if the promo code is valid for use.
        Optionally, pass the user to perform user-specific validations.
        """
        if not self.active:
            return False
        if self.expiration_date and self.expiration_date < timezone.now():
            return False
        if self.redemption_limit is not None and self.get_total_redemptions() >= self.redemption_limit:
            return False
        if user:
            if self.specific_customers.exists() and not self.specific_customers.filter(id=user.id).exists():
                return False
            if self.new_customers_only and not self.is_new_customer(user):
                return False
            if self.get_user_redemptions(user) >= self.usage_limit_per_customer:
                return False
            if self.min_purchase_amount and not self.has_min_purchase(user):
                return False
            if self.applicable_products.exists() and not self.has_applicable_products(user):
                return False
        return True
    
    def get_total_redemptions(self):
        return PromoCodeUsage.objects.filter(promo_code=self).count()
    
    def get_user_redemptions(self, user):
        return PromoCodeUsage.objects.filter(promo_code=self, user=user).count()
    
    def is_new_customer(self, user):
        # Define "new" as registered within the last 30 days
        return user.date_joined >= timezone.now() - timedelta(days=30)
    
    def has_min_purchase(self, user):
        from nxtbn.order.models import Order

        if not self.min_purchase_amount or not self.min_purchase_period:
            return True
        cutoff_date = timezone.now() - self.min_purchase_period
        total = Order.objects.filter(
            user=user,
            created_at__gte=cutoff_date,
            status__in=[OrderStatus.SHIPPED, OrderStatus.DELIVERED]
        ).aggregate(total=models.Sum('total_price_in_customer_currency'))['total'] or 0
        return total >= self.min_purchase_amount
    
    def has_applicable_products(self, user):
        from nxtbn.order.models import OrderLineItem

        # Check if the user has purchased at least one of the applicable products
        return OrderLineItem.objects.filter(
            order__user=user,
            order__status__in=[OrderStatus.PENDING, OrderStatus.SHIPPED, OrderStatus.DELIVERED],
            product__in=self.applicable_products.all()
        ).exists()
    
    def clean(self):
        if self.redemption_limit is not None and self.redemption_limit <= 0:
            raise ValidationError("Redemption limit must be a positive integer.")
        if self.min_purchase_amount is not None and self.min_purchase_amount < 0:
            raise ValidationError("Minimum purchase amount cannot be negative.")
        super().clean()
    
    class Meta:
        verbose_name = "Promo Code"
        verbose_name_plural = "Promo Codes"



class PromoCodeUsage(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Select the customer who redeemed this promo code.")
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, help_text="The promo code that was applied to the order.")
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, help_text="The order associated with the use of this promo code.")
    applied_at = models.DateTimeField(auto_now_add=True, help_text="The timestamp when the promo code was applied.")
    

class PromoCodeCustomer(models.Model):
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, help_text="The promo code that is restricted to specific customers.")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The customer who is eligible to use this promo code.")
    
    class Meta:
        unique_together = ('promo_code', 'customer')
        verbose_name = "Promo Code Customer"
        verbose_name_plural = "Promo Code Customers"
    
    def __str__(self):
        return f"{self.promo_code.code} - {self.customer.username}"
    

class PromoCodeProduct(models.Model):
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, help_text="The promo code that applies to specific products.")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="The product eligible for this promo code.")
    
    class Meta:
        unique_together = ('promo_code', 'product')
        verbose_name = "Promo Code Product"
        verbose_name_plural = "Promo Code Products"
    
    def __str__(self):
        return f"{self.promo_code.code} - {self.product.name}"
