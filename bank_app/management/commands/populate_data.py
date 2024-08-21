from bank_app.models import Account, Movement
from django.core.management.base import BaseCommand
# from bank_app.models import Account, Movement
import random
from faker import Faker


class Command(BaseCommand):
    """
    Django's management command to populate the database with dummy data.
    """

    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        faker = Faker()
        accounts = []
        for _ in range(10):
            name = faker.name()
            iban = faker.iban()
            balance = random.uniform(1000, 5000)
            account = Account.objects.create(name=name,IBAN=iban, balance=balance)
            accounts.append(account)

        movement_types = ["Deposit","Withdraw","Transfer"]

        for account in accounts:
            for _ in range(random.randint(5, 15)):
                amount = random.uniform(10, 1000)
                movement_type = random.choice(movement_types)
                if movement_type == "Transfer":
                    other_account = random.choice([acc for acc in accounts if acc != account])
                    account.balance -= amount
                    other_account.balance += amount
                    account.save()
                    other_account.save()
                    Movement.objects.create(account=account, amount=-amount, balance=account.balance, movement_type=movement_type)
                    Movement.objects.create(account=other_account, amount=amount, balance= other_account.balance, movement_type=movement_type)
                    
                else:
                    if movement_type == "Withdraw" and account.balance < amount:
                        amount = account.balance
                    Movement.objects.create(account=account, amount=amount, balance = account.balance, movement_type=movement_type)
                    if movement_type == "Deposit":
                        account.balance += amount
                    else:
                        account.balance -= amount
                    account.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))