from django.urls import path
from . import views

urlpatterns = [
    path('predict_sentiment', views.predict_sentiment, name="predict"),
]