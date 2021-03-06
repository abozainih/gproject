from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from accounts.mixins import AdminMixin
from accounts.models import User
from employees.forms import CreateDataEntryEmployeeForm, CreateEmployeeForm, UpdateEmployeeForm
from employees.models import Employee, Absence


class EmployeesListView(AdminMixin, TemplateView):
    template_name = "employees/employeesList.html"
    login_url = reverse_lazy("login")
    redirect_field_name = 'redirect_to'


class DataEntryEmployeeCreateView(AdminMixin, CreateView):
    template_name = "employees/addDataEntryEmployee.html"
    login_url = reverse_lazy("login")
    model = User
    form_class = CreateDataEntryEmployeeForm
    success_url = reverse_lazy("EmployeesList")


class EmployeeCreateView(AdminMixin, CreateView):
    template_name = "employees/addEmployee.html"
    login_url = reverse_lazy("login")
    model = User
    form_class = CreateEmployeeForm
    success_url = reverse_lazy("EmployeesList")


class EmployeeUpdateView(AdminMixin, UpdateView):
    template_name = "employees/updateEmployee.html"
    login_url = reverse_lazy("login")
    model = User
    success_url = reverse_lazy("EmployeesList")
    form_class = UpdateEmployeeForm

    def get_object(self, queryset=None):
        employee = Employee.objects.get(pk=self.kwargs['pk'] )
        return User.objects.get(pk=employee.user.id)

    def get_initial(self):
        initial = super().get_initial()
        employee = Employee.objects.get(user=self.get_object())
        initial['salary_per_day'] = employee.salary_per_day
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        employee = Employee.objects.get(user=form.instance)
        employee.salary_per_day = form.cleaned_data['salary_per_day']
        form.instance.save()
        employee.save()
        return response


class AbsenceCreateView(AdminMixin, CreateView):
    http_method_names = ['post']
    login_url = reverse_lazy("login")
    model = Absence
    fields = ['is_paid']
    success_url = reverse_lazy("EmployeesList")

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            form.instance.employee = Employee.objects.get(pk=self.kwargs['pk'])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AbsenceListView(AdminMixin, TemplateView):
    template_name = "absences/absencesList.html"
    login_url = reverse_lazy("login")
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"employee": Employee.objects.get(pk=self.kwargs['pk'])})
        return context



