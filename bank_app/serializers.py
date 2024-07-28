from rest_framework import serializers
from .models import Account, Movement

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'



class MovementSerializer(serializers.ModelSerializer):
    account = Movement
    class Meta:
        model = Movement
        fields = '__all__'
