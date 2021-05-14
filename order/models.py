from django.contrib.auth import get_user_model
from django.db import models
from product.models import Product

User = get_user_model()


class Order(models.Model):
    #id есть автоматом
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    adress = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)


    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        if Order.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save(update_fields=['activation_code'])
