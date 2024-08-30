from rest_framework import serializers
from .models import MathChallenge, ScienceChallenge, CoinTransaction, Pet

class MathChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MathChallenge
        fields = ['id', 'question', 'answer', 'difficulty', 'points']

class ScienceChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScienceChallenge
        fields = ['id', 'question', 'answer', 'difficulty', 'points']

class CoinTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinTransaction
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'