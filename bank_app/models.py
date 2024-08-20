from django.db import models


class Account(models.Model):
    """
    Account Model used to show account of users.
    Attributes:

    name: name of account owner
    balance: total balance of owner
    IBAN: International Bank Account Number of 24-Characters.
    """
    
    name = models.CharField(max_length=100)
    balance = models.PositiveIntegerField(default=0)
    IBAN = models.CharField(max_length=34,unique=True)

    def __str__(self) -> str:
        return str(self.name)


class Movement(models.Model):

    """
    Model Representing a transaction in the Account.

    Attributes:

    account: Foreign key used to link user with the transactions (One-to-Many Relationship)
    movement_type: used to describe the type of transaction
    date: tells the date and time of transaction
    balance: Balance after the completed transaction.

    """

    MOVEMENT_CHOICES = [
        ('Deposit','deposit'),
        ('Withdraw','withdraw'),
        ('Transfer','transfer'),
    ]
    movement_type = models.CharField(choices=MOVEMENT_CHOICES,max_length=10)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    balance = models.PositiveIntegerField()

    class Meta:
        ordering = ["date"]

    def __str__(self) -> str:
        return str(self.movement_type)
    

 
 
