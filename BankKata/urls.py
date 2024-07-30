from django.contrib import admin
from django.urls import path
from bank_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('statement/',views.StatementView.as_view(),name="Account Statement"),
    path('statement/<int:pk>/',views.StatementView.as_view(),name="Account Statement"),
    path('deposit/',views.DepositView.as_view(),name="Deposit Amount"),
    path('deposit/<int:pk>',views.DepositView.as_view(),name="Deposit Amount"),
    path('withdraw/',views.WithdrawView.as_view(),name="Withdraw Amount"),
    path('withdraw/<int:pk>',views.WithdrawView.as_view(),name="Withdraw Amount"),
    path('transfer/',views.TransferView.as_view(),name="Transfer Amount"),
    path('transfer/<int:pk>',views.TransferView.as_view(),name="Transfer Amount"),
]
