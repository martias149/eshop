from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Order

STOCK_DEDUCTED_STATUSES = {'confirmed', 'shipped', 'delivered'}


@receiver(pre_save, sender=Order)
def manage_stock_on_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        previous = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    was_deducted = previous.status in STOCK_DEDUCTED_STATUSES
    will_deduct = instance.status in STOCK_DEDUCTED_STATUSES

    if was_deducted == will_deduct:
        return

    with transaction.atomic():
        items = instance.items.select_related('product').select_for_update()

        if will_deduct:
            for item in items:
                if item.product.stock < item.quantity:
                    raise ValidationError(
                        f'Not enough stock for "{item.product.name}": '
                        f'requested {item.quantity}, available {item.product.stock}.'
                    )
            for item in items:
                item.product.stock -= item.quantity
                item.product.save(update_fields=['stock'])
        else:
            for item in items:
                item.product.stock += item.quantity
                item.product.save(update_fields=['stock'])
