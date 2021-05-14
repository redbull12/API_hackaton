from django.utils import timezone
from pytils.translit import slugify

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return self.title
    # ----------------------------------------------
    #       автослаг
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save()


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, primary_key=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')


    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.title

    # ----------------------------------------------
    #       автослаг
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         current = timezone.now().strftime('%s')
    #         self.slug = slugify(self.title) + current
    #     super().save()


class Review(models.Model):
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)


# 22e8c57bd213caa9bae36f0fea19acd91cbfd97a


