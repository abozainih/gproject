import calendar
import datetime
from decimal import Decimal

import django.views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View

from accounts.models import User
from customers.models import Customer
from .forms import CreateOrderForm, CustomerCreateOrderForm
from accounts.mixins import AdminAndEmployeeMixin, AdminMixin
from .models import Order
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = "orders/CreateOrder.html"
    login_url = reverse_lazy("login")
    form_class = CreateOrderForm
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy("OrderList")

    def form_valid(self, form):
        form.instance.made_for = User.objects.get(phone_number=form.cleaned_data['phone_number'])
        form.instance.made_by = self.request.user
        form.instance.order_status = 0
        response = super().form_valid(form)
        form.instance.save()
        return response


class CustomerOrderCreateView(LoginRequiredMixin, CreateView):

    template_name = "orders/CustomerCreateOrder.html"
    login_url = reverse_lazy("login")
    form_class = CustomerCreateOrderForm
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy("mainpanel")

    def form_valid(self, form):
        form.instance.made_for = self.request.user
        form.instance.made_by = self.request.user
        form.instance.order_status = 0
        response = super().form_valid(form)
        form.instance.save()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'price': self.request.user.user_customer.all()[0].price_per_gallon
        }
        context.update(extra_context)

        return context


class OrderListView(AdminAndEmployeeMixin, TemplateView):
    template_name = "orders/ordersList.html"
    login_url = reverse_lazy("login")
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'isAdmin': self.request.user.is_staff and self.request.user.is_superuser,
            'isEmployee': hasattr(self.request.user, 'employee_user') and self.request.user.is_active,
        }
        context.update(extra_context)

        return context


class AcceptOrder(AdminAndEmployeeMixin, django.views.View):
    http_method_names = ['post']
    login_url = reverse_lazy("login")
    redirect_field_name = 'redirect_to'

    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.order_status = 1
        order.save()
        return redirect("OrderList")


class RejectOrder(AdminAndEmployeeMixin, django.views.View):
    http_method_names = ['post']
    login_url = reverse_lazy("login")
    redirect_field_name = 'redirect_to'

    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.order_status = 2
        order.save()
        return redirect("OrderList")


class OrderHistory(AdminAndEmployeeMixin, TemplateView):
    template_name = "orders/orderHistory.html"
    login_url = reverse_lazy("login")
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'isAdmin': self.request.user.is_staff and self.request.user.is_superuser,
            'isEmployee': hasattr(self.request.user, 'employee_user') and self.request.user.is_active,
        }
        context.update(extra_context)

        return context

class CustomerOrderHistory(LoginRequiredMixin, TemplateView):
    template_name = "orders/customerOrderHistory.html"
    login_url = reverse_lazy("login")
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"customer": Customer.objects.get(pk=self.kwargs['pk'])})
        return context


class OrdersSalesCount(AdminMixin, View):

    def get(self, request, start, end):
        orders = Order.objects.filter(order_status=1, order_date__range=[start, end])
        sum = 0
        for obj in orders:
            sum += obj.made_for.user_customer.all()[0].price_per_gallon * obj.num_of_gallon

        sum = Decimal(sum).normalize()
        return JsonResponse({'ordersSales': sum})


class LastYearSales(AdminMixin, View):

    def get(self, request):
        today = datetime.datetime.today()
        year = today.year
        data = {}
        month = 1
        months_names = list(calendar.month_name)
        while month <= 12:
            data[months_names[month]] = 0
            orders = Order.objects.filter(order_status=1, order_date__month=month, order_date__year=year)

            for obj in orders:
                data[months_names[month]] += obj.num_of_gallon * obj.made_for.user_customer.all()[0].price_per_gallon
            month += 1

        return JsonResponse(data)
