from django.urls import path

from order.views import (MakeOrderView, ConfirmOrderView)

urlpatterns = [
    path('order/', MakeOrderView.as_view()),
    path('confirmation/', ConfirmOrderView.as_view()),
]