from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from accounts.utils import get_user_company, get_user_role
from transaction.models import Order, OrderItem, Service
from customers.models import Customer,Lead
from transaction.forms import OrderForm, OrderItemForm, ServiceForm
from inventory.models import Product
from django.contrib.auth.models import User
from django.db.models import Q


class OrderList(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        orders = Order.objects.filter(company_id=company_id).order_by('-id')
        return render(request, 'order_list.html', {'orders': orders, 'role': role})


class PendingOrderList(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role in ['Admin', 'Manager']:
            orders = Order.objects.filter(company_id=company_id, status="Pending").order_by('-id')
        else:
            orders = Order.objects.filter(company_id=company_id, status="Pending", created_by=request.user).order_by('-id')

        return render(request, 'pending_order.html', {'orders': orders, 'role': role})


class OrderAdd(View):
    def get(self, request):
        company_id = get_user_company(request)

        form = OrderForm()
        form.fields['customer'].queryset = Customer.objects.filter(company_id=company_id)
        item_form = OrderItemForm()

        customers = Customer.objects.filter(company_id=company_id)
        products = Product.objects.filter(company_id=company_id)

        return render(request, 'order_form.html', {
            'form': form,
            'item_form': item_form,
            'customers': customers,
            'products': products})

    def post(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        form = OrderForm(request.POST)
        form.fields['customer'].queryset = Customer.objects.filter(company_id=company_id)
        customers = Customer.objects.filter(company_id=company_id)
        products = Product.objects.filter(company_id=company_id)

        if not form.is_valid():
            messages.error(request, "Error creating order.")
            return render(request, 'order_form.html', {
                'form': form,
                'customers': customers,
                'products': products
            })

        order = form.save(commit=False)
        order.company_id = company_id
        order.created_by = request.user
        order.total_amount = 0
        order.total_profit = 0
        order.save()

        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        selling_prices = request.POST.getlist('selling_price')

        if not product_ids or not quantities:
            messages.error(request, "Please add at least one product.")
            order.delete()
            return render(request, 'order_form.html', {
                'form': form,
                'customers': customers,
                'products': products
            })

        for i in range(len(product_ids)):
            product_id = product_ids[i]
            quantity = quantities[i]
            selling_price = selling_prices[i]

            if not product_id or not quantity or not selling_price:#skip
                continue

            product = get_object_or_404(Product, id=product_id, company_id=company_id)
            quantity = int(quantity)
            selling_price = float(selling_price)


            if role != 'Admin' and selling_price < product.min_selling_price:
                messages.error(request, " cannot sell below minimum price")
                order.delete()
                return render(request, 'order_form.html', {
                    'form': form,
                    'customers': customers,
                    'products': products
                })

            cost_price = product.buying_price or product.manufacture_price or 0
            profit = (selling_price - cost_price) * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                selling_price=selling_price,
                profit=profit
            )

            product.stock -= quantity
            product.save()

            order.total_amount += selling_price * quantity
            order.total_profit += profit

        order.save()
        messages.success(request, "Order created successfully!")
        return redirect('transaction:order_list')

class OrderUpdate(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        order = get_object_or_404(Order, id=i, company_id=company_id)
        form = OrderForm(instance=order)
        form.fields['customer'].queryset = Customer.objects.filter(company_id=company_id)
        item_form = OrderItemForm()
        customers = Customer.objects.filter(company_id=company_id)
        products = Product.objects.filter(company_id=company_id)
        return render(request, 'order_form.html', {
            'form': form,
            'order': order,
            'item_form': item_form,
            'customers': customers,
            'products': products})

    def post(self, request, i):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)
        order = get_object_or_404(Order, id=i, company_id=company_id)
        form = OrderForm(request.POST, instance=order)
        form.fields['customer'].queryset = Customer.objects.filter(company_id=company_id)
        customers = Customer.objects.filter(company_id=company_id)
        products = Product.objects.filter(company_id=company_id)

        if not form.is_valid():
            messages.error(request, "Error updating order.")
            return render(request, 'order_form.html', {
                'form': form,
                'order': order,
                'customers': customers,
                'products': products })

        order = form.save(commit=False)
        order.save()

        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        order.items.all().delete()


        order.total_amount = 0
        order.total_profit = 0

        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        selling_prices = request.POST.getlist('selling_price')

        if not product_ids or not quantities:
            messages.error(request, "Please add at least one product.")
            return render(request, 'order_form.html', {
                'form': form,
                'order': order,
                'customers': customers,
                'products': products})


        for x in range(len(product_ids)):
            product_id = product_ids[x]
            quantity = quantities[x]
            selling_price = selling_prices[x]

            if not product_id or not quantity or not selling_price:
                continue

            product = get_object_or_404(Product, id=product_id, company_id=company_id)
            quantity = int(quantity)
            selling_price = float(selling_price)

            if role != 'Admin' and selling_price < product.min_selling_price:
                messages.error(request, " cannot sell below minimum price")
                return render(request, 'order_form.html', {
                    'form': form,
                    'order': order,
                    'customers': customers,
                    'products': products })

            cost_price = product.buying_price or product.manufacture_price or 0
            profit = (selling_price - cost_price) * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                selling_price=selling_price,
                profit=profit
            )

            product.stock -= quantity
            product.save()

            order.total_amount += selling_price * quantity
            order.total_profit += profit

        order.save()
        messages.success(request, "Order updated successfully!")
        return redirect('transaction:order_list')



class OrderDelete(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        order = get_object_or_404(Order, id=i, company_id=company_id)

        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()

        order.delete()
        messages.success(request, "Order deleted successfully!")
        return redirect('transaction:order_list')


class OrderDetail(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        order = get_object_or_404(Order, id=i, company_id=company_id)
        role = get_user_role(request, company_id)
        return render(request, 'order_detail.html', {'order': order, 'role': role})

#service

class ServiceList(View):
    def get(self, request):
        company_id = get_user_company(request)

        services = Service.objects.filter(company_id=company_id).order_by('-id')

        return render(request, 'service_list.html', {'services': services})



class ServiceAdd(View):
    def get(self, request):
        company_id = get_user_company(request)

        form = ServiceForm()

        form.fields["customer"].queryset = Customer.objects.filter(company_id=company_id)
        form.fields["lead"].queryset = Lead.objects.filter(company_id=company_id).filter(Q(status="New") | Q(status="Contacted"))
        form.fields["product"].queryset = Product.objects.filter(company_id=company_id)
        form.fields["assigned_to"].queryset = User.objects.filter(
            is_superuser=False,
            companyuser__company_id=company_id,
            companyuser__status="Approved"
        )

        return render(request, "service_form.html", {"form": form})

    def post(self, request):
        company_id = get_user_company(request)

        form = ServiceForm(request.POST)


        form.fields["customer"].queryset = Customer.objects.filter(company_id=company_id)
        form.fields["lead"].queryset = Lead.objects.filter(company_id=company_id).filter(Q(status="New") | Q(status="Contacted"))
        form.fields["product"].queryset = Product.objects.filter(company_id=company_id)
        form.fields["assigned_to"].queryset = User.objects.filter(
            is_superuser=False,
            companyuser__company_id=company_id,
            companyuser__status="Approved"
        )

        if form.is_valid():
            service = form.save(commit=False)
            service.created_by = request.user
            service.company_id = company_id
            service.save()
            messages.success(request, "Service added successfully!")
            return redirect("transaction:service_list")

        messages.error(request, "Error adding service.")
        return render(request, "service_form.html", {"form": form})



class ServiceUpdate(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        service = get_object_or_404(Service, id=i, company_id=company_id)
        form = ServiceForm(instance=service)

        form.fields["customer"].queryset = Customer.objects.filter(company_id=company_id)
        form.fields["lead"].queryset = Lead.objects.filter(company_id=company_id).filter(Q(status="New") | Q(status="Contacted"))
        form.fields["product"].queryset = Product.objects.filter(company_id=company_id)
        form.fields["assigned_to"].queryset = User.objects.filter(
            is_superuser=False,
            companyuser__company_id=company_id,
            companyuser__status='Approved'
        )

        customers = Customer.objects.filter(company_id=company_id)
        products = Product.objects.filter(company_id=company_id)
        return render(request, 'service_form.html', {
            'form': form,
            'service': service,
            'customers': customers,
            'products': products
        })

    def post(self, request, i):
        company_id = get_user_company(request)
        service = get_object_or_404(Service, id=i, company_id=company_id)
        form = ServiceForm(request.POST, instance=service)

        form.fields["customer"].queryset = Customer.objects.filter(company_id=company_id)
        form.fields["lead"].queryset = Lead.objects.filter(company_id=company_id).filter(Q(status="New") | Q(status="Contacted"))
        form.fields["product"].queryset = Product.objects.filter(company_id=company_id)
        form.fields["assigned_to"].queryset = User.objects.filter(
            is_superuser=False,
            companyuser__company_id=company_id,
            companyuser__status='Approved'
        )

        customers = Customer.objects.filter(company_id=company_id)
        products = Product.objects.filter(company_id=company_id)

        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect('transaction:service_list')

        messages.error(request, "Error updating service.")
        return render(request, 'service_form.html', {
            'form': form,
            'service': service,
            'customers': customers,
            'products': products
        })


class ServiceDelete(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        service = get_object_or_404(Service, id=i, company_id=company_id)
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect('transaction:service_list')


class ServiceDetail(View):
    def get(self, request, i):
        company_id = get_user_company(request)
        service = get_object_or_404(Service, id=i, company_id=company_id)
        role = get_user_role(request, company_id)
        return render(request, 'service_detail.html', {'service': service, 'role': role})


class CompletedServiceList(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role in ['Admin', 'Manager']:
            services = Service.objects.filter(company_id=company_id, status="Completed").order_by('-id')
        else:
            services = Service.objects.filter(
                company_id=company_id, created_by=request.user, status="Completed").order_by('-id')

        return render(request, 'completed_service.html', {'services': services, 'role': role})
