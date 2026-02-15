from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from accounts.models import CompanyUser,Company
from accounts.utils import get_user_company, get_user_role
from inventory.models import Product,Category
from customers.models import Customer
from transaction.models import Order
from core.models import Leave
from core.forms import LeaveForm


from django.utils import timezone
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Count

class DashboardView(View):
    def get(self, request):

        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if not company_id:
            return redirect('accounts:select_company')

        company = Company.objects.filter(id=company_id).first()
        if company:
            company_name = company.name
        else:
            company_name = "N/A"

        current_year = timezone.now().year
        selected_year = int(request.GET.get("year", current_year))
        year_options = list(range(current_year, current_year - 5, -1))

        total_orders = Order.objects.filter(company_id=company_id).count()
        total_customers = Customer.objects.filter(company_id=company_id).count()
        pending_orders = Order.objects.filter(company_id=company_id, status='Pending').count()
        out_of_stock = Product.objects.filter(company_id=company_id, stock=0).count()

        orders = (Order.objects.filter(company_id=company_id, created_at__year=selected_year)
            .annotate(month=ExtractMonth('created_at'))
            .values('month')
            .annotate(total_orders=Count('id'))
            .order_by('month'))

        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        data = [0] * 12

        for o in orders:
            data[o['month'] - 1] = o['total_orders']

        chart_data = zip(month_names, data)

        context = {
            'company_name': company_name,
            'username': request.user.username,
            'role': role,
            'month_names': month_names,
            'data': data,
            'chart_data': chart_data,
            'selected_year': selected_year,
            'year_options': year_options,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'pending_orders': pending_orders,
            'out_of_stock': out_of_stock,
        }
        return render(request, 'dashboard.html', context)

class LeaveList(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role in ['Admin', 'Manager']:
            leaves = Leave.objects.filter(company_id=company_id).select_related('user').order_by('-created_at')
        else:
            leaves = Leave.objects.filter(company_id=company_id, user=request.user).order_by('-created_at')

        return render(request, 'leave_list.html', {'leaves': leaves, 'role': role})


class LeaveCreate(View):
    def get(self, request):
        form = LeaveForm()
        return render(request, 'leave_form.html', {'form': form})

    def post(self, request):
        company_id = get_user_company(request)
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.company_id = company_id
            leave.user = request.user
            leave.save()
            messages.success(request, "Leave request submitted successfully.")
            return redirect('core:leave_list')
        return render(request, 'leave_form.html', {'form': form})


class LeaveAction(View):
    def post(self, request, pk, action):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to perform this action.")
            return redirect('core:leave_list')

        leave = get_object_or_404(Leave, pk=pk, company_id=company_id)
        if action == 'approve':
            leave.status = 'Approved'
        elif action == 'reject':
            leave.status = 'Rejected'
        leave.save()

        messages.success(request, "Leave "+action+"ed successfully.")
        return redirect('core:leave_list')

class GlobalSearchView(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        query = request.GET.get('q')
        products = []
        categories = []
        customers = []

        if query:
            products = Product.objects.filter(
                Q(name__icontains=query)
                | Q(category__name__icontains=query),
            company_id = company_id
            ).distinct()

            categories = Category.objects.filter(
                Q(name__icontains=query),
                company_id=company_id
            ).distinct()

            customers = Customer.objects.filter(
                Q(name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(address__icontains=query),
                company=company_id
            ).distinct()

        context = {
            'query': query,
            'products': products,
            'categories': categories,
            'customers': customers,
            'role': role
        }
        return render(request, 'search_result.html', context)