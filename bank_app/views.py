from django.shortcuts import render
# to get the decimal field
import decimal
from .serializers import AccountSerializer,MovementSerializer
from .models import Account, Movement
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework import status
from .pagination import CustomPageNubmerPagination
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Accounts'])
class Accounts(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

@extend_schema(tags=['Account Details'])
class AccountDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

@extend_schema(tags=['Account Statement'])
class AccountStatement(generics.ListAPIView):
    """
    View to get account Statement
    """
    serializer_class = MovementSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Movement.objects.filter(account_id=pk)
        return Movement.objects.none()

    pagination_class = CustomPageNubmerPagination
    #this gives the support to perform filtering and searching
    filter_backends = [SearchFilter,OrderingFilter]
    # this provides the options to order by choice
    ordering_fields = ['date']
    # this is used for default ordering of the data
    ordering = ['-date']
    # the double underscore in the account id is for solving the issue of lookups for the foreign key or many-to-many fields
    search_fields = ['movement_type','account__id']
    

@extend_schema(tags=['Deposit'])
@api_view(['POST'])
def deposit(request,pk):
    """
    api view to deposit money and saving movement
    Args: pk (int)
    """
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response({"error":"Account does'nt exist"})
    
    amount = decimal.Decimal(request.data.get('amount'))
    if amount <= 0:
        return Response({'error':'Invalid Amount!'})
    account.balance += amount
    account.save()
    Movement.objects.create(account=account,amount=+amount,balance=account.balance,movement_type="Deposit")
    return Response({'msg':'Successfully Deposited!'})



@extend_schema(tags=['Withdraw'])
@api_view(['POST'])
def withdraw(request,pk):

    """
    api view for withdrawing money from account

    Args:
    pk (int): used to get account 
    """

    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response({'error':'Account Not found!'})

    amount = decimal.Decimal(request.data.get('amount'))
    if amount<=0:
        return Response({'error':'Invalid Amount!'})
    if account.balance >= amount:
        account.balance -= amount
        account.save()
        Movement.objects.create(account=account,amount=-amount,balance=account.balance,movement_type="Withdraw")
        return Response({'msg':'Successfully Withdrawed'})
    else:
        return Response({'error':'Low Balance!'})
    


@extend_schema(tags=['Transfer'])
@api_view(['POST'])
def transfer(request):
    """
    Transfer view to transfer funds from one account to another using IBANs
    Args:   from_iban (sender's IBAN)       to_iban (receiver's IBAN)
    """

    from_iban = request.data.get('from_iban')
    to_iban = request.data.get('to_iban')
    amount = decimal.Decimal(request.data.get('amount'))

    try:
        from_account = Account.objects.get(iban=from_iban)
        to_account = Account.objects.get(iban=to_iban)
    except Account.DoesNotExist:
        return Response({'error':'One or Both Accounts do not Found!'})
    
    if amount <= 0:
        return Response({'error':'Invalid Amount!'})
    if from_account.balance >= amount:
        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()
        Movement.objects.create(account=from_account,amount=-amount,balance=from_account.balance,movement_type="Transfer")
        Movement.objects.create(account=to_account,amount=+amount,balance=to_account.balance,movement_type="Transfer")
        return Response({'msg':'Transaction Successful!'})
    return Response({'error':'Insufficient Balance!'})










































# def createMovement(movement_type,accountId,requestamount,totalBalance):
#     movement = {
#         "movement_type": movement_type,
#         "account": accountId,
#         "amount": requestamount,
#         "balance": totalBalance,
#     }
#     mov_serializer = MovementSerializer(data=movement)
#     if mov_serializer.is_valid():
#         mov_serializer.save()
#     else:
#         return Response(mov_serializer.errors)




# class DepositView(APIView):

#     def put(self,request,pk=None,format=None):
#         try:
#             account = Account.objects.get(pk=pk)
#         except Account.DoesNotExist:
#             return Response({'msg':'Invalid Account ID'})
        
#         serializer = AccountSerializer(account,data=request.data,partial=True)
#         requestamount = int(request.data.get('amount',0))
#         totalBalance = account.balance + requestamount
#         account.balance = totalBalance
#         if serializer.is_valid():
#             createMovement("Deposit",account.id,requestamount,totalBalance)
#             serializer.save()
#             return Response({'msg':'Amount Deposited'})
#         else:
#             return Response(serializer.errors)
            
        

# class WithdrawView(APIView):
#     def get(self,request,pk=None,format=None):
#         if pk is None:
#             account = Account.objects.all()
#             serializer = AccountSerializer(account,many=True)
#         account = Account.objects.get(pk=pk)
#         serializer = AccountSerializer(account)
#         return Response(serializer.data)



#     def put(self,request,pk=None,format=None):
#         try:
#             account = Account.objects.get(pk=pk)
#         except Account.DoesNotExist:
#             return Response({'msg':'Invalid Account ID'})
        
#         serializer = AccountSerializer(account,data=request.data,partial=True)
#         requestamount = int(request.data.get('amount',0))
#         if requestamount <= account.balance:
#             totalBalance = account.balance - requestamount
#         else:
#             return Response({'msg':'Low Balance!'})
        
#         if serializer.is_valid():
#             createMovement("Withdraw",account.id,-requestamount,totalBalance)
#             serializer.save()
#             return Response({'msg':'Amount Withdrawed'})
#         else:
#             return Response(serializer.errors)
            
        


# class TransferView(APIView):
#     def put(self,request,pk=None,format=None):
#         if pk is not None:
#             account = Account.objects.get(pk=pk)
#             # Can apply exception handling but not to reduce nesting and complexity
#             otheraccount = Account.objects.get(pk=request.data.get('id'))
#             requestamount = int(request.data.get('amount',0))
#             if otheraccount.is_IBAN == False:
#                 return Response({'msg':'Transfer Not Possible to NON-IBAN account.'})
            
#             if requestamount <= account.balance:
#                 myBalance = account.balance - requestamount
#                 otherBalance = otheraccount.balance + requestamount
#                 mySerializer = AccountSerializer(account,data=request.data,partial=True)
#                 otherSerializer = AccountSerializer(otheraccount,data=request.data,partial=True)
#                 if mySerializer.is_valid() and otherSerializer.is_valid():
#                     createMovement("Transfer",account.id,-requestamount,myBalance)
#                     createMovement("Transfer",otheraccount.id,requestamount,otherBalance)
#                     mySerializer.save()
#                     otherSerializer.save()
#                     return Response({'msg':'Successfully Transfered!'})
#                 else:
#                     return Response([mySerializer.errors,otherSerializer.errors])
#             else:
#                 return Response({'msg':'Low Balance!'})
#         else:
#             return Response({'msg':'Provide id in the url'})




# class StatementView(generics.ListAPIView):    
#     serializer_class = MovementSerializer

#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         if pk is not None:
#             return Movement.objects.filter(account_id=pk)
#         return Movement.objects.none()

#     #this gives the support to perform filtering and searching
#     filter_backends = [SearchFilter,OrderingFilter]
#     # this provides the options to order by choice
#     ordering_fields = ['date']
#     # this is used for default ordering of the data
#     ordering = ['-date']
#     # the double quotes in the account id is for solving the issue of lookups for the foreign key or many-to-many fields
#     search_fields = ['movement_type','account__id']

    
