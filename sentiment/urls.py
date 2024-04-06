from django.urls import path
from . import views

urlpatterns = [
    path('predict_sentiment', views.predict_sentiment, name="predict"),
    path('get_history', views.get_history, name="get_history"),
    path('get_image', views.get_image, name="get_image"),
]