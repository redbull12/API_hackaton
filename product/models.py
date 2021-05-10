from django.utils import timezone

from django.db import models

from pytils.translit import slugify

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')


    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    # ----------------------------------------------
    #       автослаг
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         current = timezone.now().strftime('%s')
    #         self.slug = slugify(self.title) + current
    #     super().save()

