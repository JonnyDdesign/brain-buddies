from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import MathChallengeViewSet, CoinTransactionViewSet, PetViewSet

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'challenges', MathChallengeViewSet)
router.register(r'coins', CoinTransactionViewSet)
router.register(r'pets', PetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]