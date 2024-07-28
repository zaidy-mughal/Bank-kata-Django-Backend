
from django.shortcuts import render
from .serializers import AccountSerializer,MovementSerializer
from .models import Account, Movement
from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(["GET","PATCH"])
def depositView(request,pk=None):
    if request.method == "GET":
        if pk is not None:
            account = Account.objects.get(pk=pk)
        account = Account.objects.all()
        serializer = AccountSerializer(account,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == "PATCH":
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account,data=request.data,partial=True)
            requestamount = int(request.data.get('amount',0))
            totalBalance = account.balance + requestamount
            account.balance = totalBalance
            movement = {
                "movement_type": "Deposit",
                "account": account.id,
                "amount": requestamount,
                "balance": totalBalance,
            }
            mov_serializer = MovementSerializer(data=movement)

            if serializer.is_valid() and mov_serializer.is_valid():
                serializer.save()
                mov_serializer.save()
                return JsonResponse({'msg':'Amount Deposited'})
            else:
                return JsonResponse([serializer.errors,mov_serializer.errors],safe=False)
            
        except Account.DoesNotExist:
            return JsonResponse({'msg':'Invalid Account ID'})


@api_view(["GET"])
def statement(request,pk=None):
    if pk is not None:
        statement = Movement.objects.filter(account_id=pk)
        serializer = MovementSerializer(statement,many=True)
        return JsonResponse(serializer.data,safe=False)
    return JsonResponse({'msg':'Provide Account ID in the URL'})
