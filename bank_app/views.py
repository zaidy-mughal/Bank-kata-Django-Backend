from django.shortcuts import render
from .serializers import AccountSerializer,MovementSerializer
from .models import Account, Movement
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.filters import OrderingFilter,SearchFilter
# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def createMovement(movement_type,accountId,requestamount,totalBalance):
    movement = {
        "movement_type": movement_type,
        "account": accountId,
        "amount": requestamount,
        "balance": totalBalance,
    }
    mov_serializer = MovementSerializer(data=movement)
    if mov_serializer.is_valid():
        mov_serializer.save()
    else:
        return Response(mov_serializer.errors)




class DepositView(APIView):
    def get(self,request,pk=None,format=None):
        if pk is None:
            account = Account.objects.all()
            serializer = AccountSerializer(account,many=True)
        account = Account.objects.get(pk=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


    def post(self,request,pk=None,format=None):
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account,data=request.data,partial=True)
            requestamount = int(request.data.get('amount',0))
            totalBalance = account.balance + requestamount
            account.balance = totalBalance

            if serializer.is_valid():
                createMovement("Deposit",account.id,requestamount,totalBalance)
                serializer.save()
                return Response({'msg':'Amount Deposited'})
            else:
                return Response(serializer.errors)
            
        except Account.DoesNotExist:
            return Response({'msg':'Invalid Account ID'})



class WithdrawView(APIView):
    def get(self,request,pk=None,format=None):
        if pk is None:
            account = Account.objects.all()
            serializer = AccountSerializer(account,many=True)
        account = Account.objects.get(pk=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


    def post(self,request,pk=None,format=None):
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account,data=request.data,partial=True)
            requestamount = int(request.data.get('amount',0))

            if requestamount <= account.balance:
                totalBalance = account.balance - requestamount
            else:
                return Response({'msg':'Low Balance!'})
            
            if serializer.is_valid():
                createMovement("Withdraw",account.id,-requestamount,totalBalance)
                serializer.save()
                return Response({'msg':'Amount Withdrawed'})
            else:
                return Response(serializer.errors)
            
        except Account.DoesNotExist:
            return Response({'msg':'Invalid Account ID'})




class TransferView(APIView):
    def put(self,request,pk=None,format=None):
        pass



class StatementView(generics.ListAPIView,generics.RetrieveAPIView):
    
    serializer_class = MovementSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Movement.objects.filter(account_id=pk)
        return Movement.objects.none()

    #this gives the support to perform filtering and searching
    filter_backends = [SearchFilter,OrderingFilter]
    # this provides the options to order by choice
    ordering_fields = ['date']     
    # this is used for default ordering of the data   
    ordering = ['-date']
    search_fields = ['movement_type','account__id']

    
