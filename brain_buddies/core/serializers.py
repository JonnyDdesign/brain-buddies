from rest_framework import serializers
from .models import MathChallenge, CoinTransaction, Pet

class MathChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MathChallenge
        fields = '__all__'

class CoinTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinTransaction
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'