from django.contrib import admin

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin


from .models import Category, Product


class ProductAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Category)
admin.site.register(Product)
