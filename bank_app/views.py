from django.shortcuts import render
from .serializers import AccountSerializer,MovementSerializer
from .models import Account, Movement
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.filters import OrderingFilter,SearchFilter


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


    def put(self,request,pk=None,format=None):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response({'msg':'Invalid Account ID'})
        
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
            
        



class WithdrawView(APIView):
    def get(self,request,pk=None,format=None):
        if pk is None:
            account = Account.objects.all()
            serializer = AccountSerializer(account,many=True)
        account = Account.objects.get(pk=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


    def put(self,request,pk=None,format=None):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response({'msg':'Invalid Account ID'})
        
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
            
        



class TransferView(APIView):
    def put(self,request,pk=None,format=None):
        if pk is not None:
            account = Account.objects.get(pk=pk)
            # Can apply exception handling but not to reduce nesting and complexity
            otheraccount = Account.objects.get(pk=request.data.get('id'))
            requestamount = int(request.data.get('amount',0))
            if otheraccount.is_IBAN == False:
                return Response({'msg':'Transfer Not Possible to NON-IBAN account.'})
            
            if requestamount <= account.balance:
                myBalance = account.balance - requestamount
                otherBalance = otheraccount.balance + requestamount
                mySerializer = AccountSerializer(account,data=request.data,partial=True)
                otherSerializer = AccountSerializer(otheraccount,data=request.data,partial=True)
                if mySerializer.is_valid() and otherSerializer.is_valid():
                    createMovement("Transfer",account.id,-requestamount,myBalance)
                    createMovement("Transfer",otheraccount.id,requestamount,otherBalance)
                    mySerializer.save()
                    otherSerializer.save()
                    return Response({'msg':'Successfully Transfered!'})
                else:
                    return Response([mySerializer.errors,otherSerializer.errors])
            else:
                return Response({'msg':'Low Balance!'})
        else:
            return Response({'msg':'Provide id in the url'})





class StatementView(generics.ListAPIView):    
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
    # the double quotes in the account id is for solving the issue of lookups for the foreign key or many-to-many fields
    search_fields = ['movement_type','account__id']

    
