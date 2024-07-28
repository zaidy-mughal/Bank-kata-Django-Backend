from django.contrib import admin
from django.urls import path
from bank_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accountstatement/',views.statement),
    path('accountstatement/<int:pk>',views.statement),
    path('deposit/',views.depositView),
    path('deposit/<int:pk>',views.depositView),
]
