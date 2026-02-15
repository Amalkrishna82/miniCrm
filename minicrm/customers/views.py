from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from accounts.utils import get_user_company, get_user_role
from customers.models import Lead, Customer
from customers.forms import LeadForm, CustomerForm
from django.contrib.auth.models import User


class LeadAdd(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role in ['Admin', 'Manager', 'Staff']:
            form_instance = LeadForm()

            form_instance.fields['assigned_to'].queryset = User.objects.filter(
                is_superuser=False,
                companyuser__company_id=company_id,
                companyuser__status='Approved')

            context = {'form': form_instance}
            return render(request, 'lead_add.html', context)

        messages.error(request, "You don't have permission to add leads.")
        return redirect('customers:lead_list')

    def post(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role in ['Admin', 'Manager', 'Staff']:
            form_instance = LeadForm(request.POST)

            form_instance.fields['assigned_to'].queryset = User.objects.filter(
                is_superuser=False,
                companyuser__company_id=company_id,
                companyuser__status='Approved' )

            if form_instance.is_valid():
                lead = form_instance.save(commit=False)
                lead.created_by = request.user
                lead.company_id = company_id
                lead.save()
                messages.success(request, 'Lead added successfully.')
                return redirect('customers:lead_list')

            context = {'form': form_instance}
            return render(request, 'lead_add.html', context)

        messages.error(request, "You don't have permission to add leads.")
        return redirect('customers:lead_list')


class LeadList(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        leads = Lead.objects.filter(company_id=company_id).order_by('-created_at')
        context = {'leads': leads, 'role': role}
        return render(request, 'lead_list.html', context)



class LeadUpdate(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to update leads.")
            return redirect('customers:lead_list')

        lead = get_object_or_404(Lead, id=i, company_id=company_id)
        form = LeadForm(instance=lead)
        context = {'form': form, 'lead': lead}
        return render(request, 'lead_update.html', context)

    def post(self, request, i):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to update leads.")
            return redirect('customers:lead_list')

        lead = get_object_or_404(Lead, id=i, company_id=company_id)
        form = LeadForm(request.POST, instance=lead)

        if form.is_valid():
            lead = form.save()
            if lead.status == 'Converted':
                existing_customer = Customer.objects.filter(
                    email=lead.email, company_id=company_id).first()

                if not existing_customer:
                    Customer.objects.create(
                        name=lead.name,
                        email=lead.email,
                        phone=lead.phone,
                        address=lead.address,
                        created_by=request.user,
                        company_id=company_id,
                    )

            messages.success(request, 'Lead updated successfully.')
            return redirect('customers:lead_list')

        context = {'form': form, 'lead': lead}
        return render(request, 'lead_update.html', context)


class LeadDelete(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        if role == 'Admin':
            lead = get_object_or_404(Lead, id=i, company_id=company_id)
            lead.delete()
            messages.success(request, 'Lead deleted successfully')
        else:
            messages.error(request, "You don't have permission to delete leads.")
        return redirect('customers:lead_list')


class CustomerList(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)


        customers = Customer.objects.filter(company_id=company_id).order_by('-id')

        context = {'customers': customers, 'role': role}
        return render(request, 'customer_list.html', context)


class CustomerAdd(View):
    def get(self, request):

        form_instance = CustomerForm()
        context = {'form': form_instance}
        return render(request, 'customer_form.html', context)

    def post(self, request):
        company_id = get_user_company(request)
        form_instance = CustomerForm(request.POST)

        if form_instance.is_valid():
            customer = form_instance.save(commit=False)
            customer.created_by = request.user
            customer.company_id = company_id
            customer.save()
            messages.success(request, 'Customer added successfully')
            return redirect('customers:customer_list')

        context = {'form': form_instance}
        return render(request, 'customer_form.html', context)


class CustomerUpdate(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        customer = get_object_or_404(Customer, id=i, company_id=company_id)

        if role in ['Admin', 'Manager']:
            form_instance = CustomerForm(instance=customer)
            context = {'form': form_instance}
            return render(request, 'customer_form.html', context)

        messages.warning(request, "You don't have permission to edit customers.")
        return redirect('customers:customer_list')

    def post(self, request, i):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        customer = get_object_or_404(Customer, id=i, company_id=company_id)

        if role in ['Admin', 'Manager']:
            form_instance = CustomerForm(request.POST, instance=customer)
            if form_instance.is_valid():
                form_instance.save()
                messages.success(request, 'Customer updated successfully')
                return redirect('customers:customer_list')
            context = {'form': form_instance}
            return render(request, 'customer_form.html', context)

        messages.warning(request, "You don't have permission to edit customers.")
        return redirect('customers:customer_list')


class CustomerDelete(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role == 'Admin':
            customer = get_object_or_404(Customer, id=i, company_id=company_id)
            customer.delete()
            messages.success(request, 'Customer deleted successfully')
        else:
            messages.error(request, "You don't have permission to delete customers.")
        return redirect('customers:customer_list')



