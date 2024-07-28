from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.PositiveIntegerField(default=0)
    is_IBAN = models.BooleanField(default=False)
    IBAN = models.CharField(max_length=34,blank=True,null=True)

    def __str__(self) -> str:
        return str(self.id)


class Movement(models.Model):
    MOVEMENT_CHOICES = [
        ('Deposit','deposit'),
        ('Withdraw','withdraw'),
        ('Transfer','transfer')
    ]
    movement_type = models.CharField(choices=MOVEMENT_CHOICES,max_length=10)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    amount = models.IntegerField()
    balance = models.PositiveIntegerField()

    class Meta:
        ordering = ["date"]

 
 
