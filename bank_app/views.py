from django.shortcuts import render
from .serializers import AccountSerializer,MovementSerializer
from .models import Account, Movement
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



class DepositView(APIView):
    def get(self,request,pk=None,format=None):
        if pk is None:
            account = Account.objects.all()
            serializer = AccountSerializer(account,many=True)
        account = Account.objects.get(pk=pk)
        serializer = AccountSerializer(account)
        return JsonResponse(serializer.data,safe=False)


    def post(self,request,pk=None,format=None):
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



class WithdrawView(APIView):
    def get(self,request,pk=None,format=None):
        if pk is None:
            account = Account.objects.all()
            serializer = AccountSerializer(account,many=True)
        account = Account.objects.get(pk=pk)
        serializer = AccountSerializer(account)
        return JsonResponse(serializer.data,safe=False)


    def post(self,request,pk=None,format=None):
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account,data=request.data,partial=True)
            requestamount = int(request.data.get('amount',0))

            if requestamount <= account.balance:
                totalBalance = account.balance - requestamount
            else:
                return JsonResponse({'msg':'Low Balance!'})
            
            account.balance = totalBalance
            movement = {
                "movement_type": "Withdraw",
                "account": account.id,
                "amount": -requestamount,
                "balance": totalBalance,
            }
            mov_serializer = MovementSerializer(data=movement)

            if serializer.is_valid() and mov_serializer.is_valid():
                serializer.save()
                mov_serializer.save()
                return JsonResponse({'msg':'Amount Withdrawed'})
            else:
                return JsonResponse([serializer.errors,mov_serializer.errors],safe=False)
            
        except Account.DoesNotExist:
            return JsonResponse({'msg':'Invalid Account ID'})





class StatementView(APIView):
    def get(self,request,pk=None,format=None):
        if pk is not None:
            statement = Movement.objects.filter(account_id=pk)
            serializer = MovementSerializer(statement,many=True)
            return JsonResponse(serializer.data,safe=False)
        return JsonResponse({'msg':'Provide Account ID in the URL'})
