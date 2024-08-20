from django.contrib import admin
from django.urls import path
from bank_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',views.Accounts.as_view(),name="Accounts"),
    path('account/<int:pk>',views.Accounts.as_view()),



    # # path('statement/',views.StatementView.as_view(),name="Account Statement"),
    # path('account/<int:pk>/statement',views.StatementView.as_view(),name="Account Statement"),
    # # path('deposit/',views.DepositView.as_view(),name="Deposit Amount"),
    # path('account/<int:pk>/deposit',views.DepositView.as_view(),name="Deposit Amount"),
    # # path('withdraw/',views.WithdrawView.as_view(),name="Withdraw Amount"),
    # path('account/<int:pk>/withdraw',views.WithdrawView.as_view(),name="Withdraw Amount"),
    # # path('transfer/',views.TransferView.as_view(),name="Transfer Amount"),
    # path('account/<int:pk>/transfer',views.TransferView.as_view(),name="Transfer Amount"),
]
