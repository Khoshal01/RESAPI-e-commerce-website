from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class ProductModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_products'  # CHANGED: was 'product'
    )
    
    product_name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # FIXED: Added variable
    stock = models.PositiveIntegerField(default=0)  # CHANGED: Better as integer
    categories = models.CharField()  # FIXED: Added max_length
    
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    class Meta:
        unique_together = (('owner', 'product_name'),)  # FIXED: Tuple of tuples
    
    def __str__(self):
        return self.product_name  # FIXED: Changed from 'name' to 'product_name'



class OrderModel(models.Model):
    # FIXED: Unique related_name
    orderproduct_name = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name='product_orders'  # CHANGED: was 'order'
    )
    
    # FIXED: Different related_name from CartModel
    orderowner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_orders'  # CHANGED: was 'order_owner'
    )

    order_items = models.CharField(max_length=200)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # CHANGED: Better as Decimal
    
    # FIXED: Add choices for status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # FIXED: Add choices for payment status
    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('orderowner', 'orderproduct_name', 'order_items'),)

    def __str__(self):
        return f"Order: {self.order_items} - {self.get_status_display()}"


class CartModel(models.Model):
    # FIXED: Different related_name from OrderModel
    cartowner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_carts'  # CHANGED: was 'order_owner' (SAME AS OrderModel!)
    )

    # FIXED: Different related_name from OrderModel
    cartproduct_name = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name='product_carts'  # CHANGED: was 'order' (SAME AS OrderModel!)
    )

    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add price at time of adding to cart
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = (('cartowner', 'cartproduct_name'),)

    def __str__(self):
        return f"{self.quantity} x {self.cartproduct_name.product_name}"


class PaymentModel(models.Model):
    order_id = models.ForeignKey(
        OrderModel,
        on_delete=models.CASCADE,
        related_name='payments'  # CHANGED: was 'payment'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)  # CHANGED: Better as Decimal
    
    # FIXED: Add max_length and choices for method
    METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ]
    
    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        default='credit_card'
    )
    
    # FIXED: Use same payment choices
    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='pending'
    )
    
    transaction_id = models.CharField(max_length=100)  # CHANGED: CharField, not Integer
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment: {self.transaction_id} - {self.get_status_display()}"