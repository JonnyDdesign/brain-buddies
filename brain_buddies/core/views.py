from rest_framework import viewsets
from .models import MathChallenge, ScienceChallenge, CoinTransaction, Pet
from .serializers import MathChallengeSerializer, ScienceChallengeSerializer, CoinTransactionSerializer, PetSerializer

class MathChallengeViewSet(viewsets.ModelViewSet):
    queryset = MathChallenge.objects.all()
    serializer_class = MathChallengeSerializer

class ScienceChallengeViewSet(viewsets.ModelViewSet):
    queryset = ScienceChallenge.objects.all()
    serializer_class = ScienceChallengeSerializer

class CoinTransactionViewSet(viewsets.ModelViewSet):
    queryset = CoinTransaction.objects.all()
    serializer_class = CoinTransactionSerializer

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer