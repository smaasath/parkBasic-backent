"""
URL configuration for parkBasic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.urls import re_path as url
from park_basic import authViews
from park_basic import bookingViews
from park_basic import authViews, mathuView,SlotView
from  rest_framework.authtoken.views import obtain_auth_token


    

urlpatterns = [
    re_path(r'^register$', authViews.RegisterApi),
    re_path(r'^login$', authViews.LoginApi),
    re_path(r'^getBooking$', mathuView.GetAllBookingAPI),
    path('admin/', admin.site.urls),
    # path('AddBooking/', bookingViews.insert_data),
    path('bookingSlots/', SlotView.BookingSlotView.as_view()),
    path('bookingSlots/<int:pk>', SlotView.BookingSlotView.as_view())
]
