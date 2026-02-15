from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from accounts.models import Company, CompanyUser
from accounts.forms import SignupForm, StartCompanyForm, JoinCompanyForm,AdminAddUserForm, CompanyUserForm, LoginForm
from accounts.utils import get_user_company, get_user_role


class SignupView(View):
    def get(self, request):
        form_instance = SignupForm()
        return render(request, 'register.html', {'form': form_instance})

    def post(self, request):
        form_instance = SignupForm(request.POST)
        if form_instance.is_valid():
            user = form_instance.save()
            login(request, user)
            return redirect('accounts:selection')
        return render(request, 'register.html', {'form': form_instance})



class SelectionView(View):
    def get(self, request):
        return render(request, 'selection.html')


class LoginView(View):
    def get(self, request):
        form_instance = LoginForm()
        return render(request, 'login.html', {'form': form_instance})

    def post(self, request):
        form_instance = LoginForm(request.POST)
        if not form_instance.is_valid():
            return render(request, 'login.html', {'form': form_instance})

        email = form_instance.cleaned_data['email']
        password = form_instance.cleaned_data['password']

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Invalid credentials.")
            return render(request, 'login.html', {'form': form_instance})

        user_auth = authenticate(username=user.username, password=password)
        if not user_auth:
            return render(request, 'login.html', {'form': form_instance})

        companies = CompanyUser.objects.filter(user=user_auth, status='Approved')
        if not companies:
            messages.error(request, "You don't have access to any company yet.")
            return render(request, 'login.html', {'form': form_instance})

        login(request, user_auth)

        if len(companies) == 1:
            company_user = companies.first()
            request.session['company_id'] = company_user.company.id
            request.session['role'] = company_user.role
            return redirect('core:dashboard')

        return redirect('accounts:select_company')


class SelectCompanyView(View):
    def get(self, request):
        user = request.user
        companies = CompanyUser.objects.filter(user=user, status='Approved')
        return render(request, 'select_company.html', {'companies': companies})

    def post(self, request):
        company_id = request.POST.get('company_id')
        if not company_id:
            messages.error(request, "Please select a company.")
            return redirect('accounts:select_company')

        company_user = CompanyUser.objects.filter(user=request.user, company_id=company_id, status='Approved').first()

        if not company_user:
            messages.error(request, "Invalid company selection.")
            return redirect('accounts:select_company')

        request.session['company_id'] = company_user.company.id
        request.session['role'] = company_user.role
        return redirect('core:dashboard')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect('accounts:login')


class StartCompanyView(View):
    def get(self, request):
        form_instance = StartCompanyForm()
        return render(request, 'start_company.html', {'form': form_instance})

    def post(self, request):
        form_instance = StartCompanyForm(request.POST)
        if form_instance.is_valid():
            company = form_instance.save(commit=False)
            company.owner = request.user
            company.save()

            CompanyUser.objects.create(user=request.user, company=company, role='Admin', status='Approved')

            request.session['company_id'] = company.id
            request.session['role'] = 'Admin'

            messages.success(request, "Company created successfully!")
            return redirect('core:dashboard')

        return render(request, 'start_company.html', {'form': form_instance})

class JoinCompanyView(View):
    def get(self, request):
        form_instance = JoinCompanyForm(initial={'email': request.user.email})
        return render(request, 'join_company.html', {'form': form_instance})

    def post(self, request):
        form_instance = JoinCompanyForm(request.POST)
        form_instance.fields['email'].initial = request.user.email

        if not form_instance.is_valid():
            return render(request, 'join_company.html', {'form': form_instance})

        company_name = form_instance.cleaned_data['company_name']
        company = Company.objects.filter(name__iexact=company_name).first()

        if not company:
            messages.error(request, "Company not found.")
            return render(request, 'join_company.html', {'form': form_instance})

        existing = CompanyUser.objects.filter(user=request.user, company=company).exists()
        if existing:
            messages.info(request, "You already requested or joined this company.")
            return redirect('accounts:login')

        CompanyUser.objects.create(user=request.user, company=company, status='Pending')
        messages.success(request, "Join request sent successfully.")

        return redirect('accounts:login')

class PendingUserListView(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role != 'Admin':
            messages.error(request, "Access denied.")
            return redirect('core:dashboard')

        pending_users = CompanyUser.objects.filter(
            company_id=company_id,
            status='Pending'
        )

        return render(request, 'pending_users.html', {
            'pending_users': pending_users
        })

    def post(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role != 'Admin':
            messages.error(request, "Access denied.")
            return redirect('core:dashboard')

        user_id = request.POST.get('user_id')
        CompanyUser.objects.filter(pk=user_id, company_id=company_id).delete()

        messages.success(request, "User rejected successfully.")
        return redirect('accounts:pending_user_list')




class ApproveUserView(View):
    def get(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        if role != 'Admin':
            messages.error(request, "Access denied.")
            return redirect('core:dashboard')

        company_user = get_object_or_404(CompanyUser, pk=pk, company_id=company_id)
        form_instance = CompanyUserForm(instance=company_user)  # Only role, salary, status
        return render(request, 'approve_users.html', {'form': form_instance, 'company_user': company_user})

    def post(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        if role != 'Admin':
            messages.error(request, "Access denied.")
            return redirect('core:dashboard')

        company_user = get_object_or_404(CompanyUser, pk=pk, company_id=company_id)
        form_instance = CompanyUserForm(request.POST, instance=company_user)

        if form_instance.is_valid():
            company_user = form_instance.save(commit=False)
            company_user.company_id = company_id
            company_user.status = 'Approved'
            company_user.save()
            messages.success(request, "User approved successfully.")
            return redirect('core:dashboard')

        return render(request, 'approve_users.html', {'form': form_instance, 'company_user': company_user})

class AdminAddUserView(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        if role != 'Admin':
            messages.error(request, "Access denied.")
            return redirect('core:dashboard')

        form = AdminAddUserForm()
        form.fields['company'].queryset = Company.objects.filter(id=company_id)
        return render(request, 'add_user.html', {'form': form})

    def post(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        if role != 'Admin':
            messages.error(request, "Access denied.")
            return redirect('core:dashboard')

        form = AdminAddUserForm(request.POST)
        form.fields['company'].queryset = Company.objects.filter(id=company_id)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            selected_company = form.cleaned_data.get('company')
            role_choice = form.cleaned_data.get('role')
            salary = form.cleaned_data.get('salary')
            CompanyUser.objects.create(
                user=user,
                company=selected_company,
                role=role_choice,
                salary=salary,
                status='Approved'
            )
            messages.success(request, "User added successfully.")
            return redirect('accounts:user_list')

        return render(request, 'add_user.html', {'form': form})


class CompanyUserListView(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        if role != 'Admin':
            messages.error(request, "Access denied.")
            return redirect('core:dashboard')

        users = CompanyUser.objects.filter(
            company_id=company_id,
            user__is_superuser=False).select_related('user')
        return render(request, 'user_list.html', {'users': users})


class UserManageView(View):
    def get(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        if role != 'Admin':
            messages.error(request, "Access denied.")
            return redirect('core:dashboard')

        company_user = get_object_or_404(CompanyUser, pk=pk, company_id=company_id)
        form_instance = CompanyUserForm(instance=company_user)
        return render(request, 'usermanage.html', {'form': form_instance, 'company_user': company_user})

    def post(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        if role != 'Admin':
            messages.error(request, "Access denied.")
            return redirect('core:dashboard')

        company_user = get_object_or_404(CompanyUser, pk=pk, company_id=company_id)

        if 'delete' in request.POST:
            company_user.delete()
            messages.success(request, "User deleted successfully.")
            return redirect('accounts:user_list')

        form_instance = CompanyUserForm(request.POST, instance=company_user)

        if form_instance.is_valid():
            company_user = form_instance.save(commit=False)
            company_user.company_id = company_id  # auto-assign admin's company
            company_user.save()
            messages.success(request, "User updated successfully.")
            return redirect('accounts:user_list')

        return render(request, 'usermanage.html', {'form': form_instance, 'company_user': company_user})
