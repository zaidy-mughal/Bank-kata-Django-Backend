from django.contrib import admin
from django.urls import path
from bank_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',views.Accounts.as_view(),name="Accounts"),
    path('account/<int:pk>',views.AccountDetails.as_view()),
    path('account/<int:pk>/statement',views.AccountStatement.as_view(),name="Account Statement"),
    path('account/<int:pk>/deposit',views.deposit,name="Deposit Amount"),
    path('account/<int:pk>/withdraw',views.withdraw,name="Withdraw Amount"),
    path('account/transfer',views.transfer,name="Transfer Amount"),
]
