from rest_framework import serializers
from .models import Account, Movement
import re

IBAN_REGEX = r'^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def validate_IBAN(self,value):
        if re.match(IBAN_REGEX,value):
            return value
        raise serializers.ValidationError("IBAN must be in correct form!")
    



class MovementSerializer(serializers.ModelSerializer):
    account = Movement
    class Meta:
        model = Movement
        fields = '__all__'
