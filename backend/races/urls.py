from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RaceViewSet, BetViewSet

router = DefaultRouter()
router.register(r'races', RaceViewSet, basename='race')
router.register(r'bets', BetViewSet, basename='bet')

urlpatterns = [
    path('', include(router.urls)),
]
