from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from accounts.utils import get_user_company, get_user_role
from inventory.models import Category, Product
from inventory.forms import CategoryForm, ProductForm, StockForm


#category

class CategoryList(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        categories = Category.objects.filter(company_id=company_id)

        return render(request, 'category_list.html', {
            'categories': categories,
            'role': role})


class CategoryCreate(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to add categories.")
            return redirect('inventory:category_list')

        form = CategoryForm()
        return render(request, 'category_form.html', {'form': form, 'role': role})

    def post(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to add categories.")
            return redirect('inventory:category_list')

        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.company_id = company_id
            category.save()

            messages.success(request, "Category added successfully.")
            return redirect('inventory:category_list')

        return render(request, 'category_form.html', {'form': form, 'role': role})


class CategoryUpdate(View):
    def get(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to edit categories.")
            return redirect('inventory:category_list')

        category = get_object_or_404(Category, pk=pk, company_id=company_id)

        form = CategoryForm(instance=category)
        return render(request, 'category_form.html', {'form': form, 'role': role})

    def post(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to edit categories.")
            return redirect('inventory:category_list')

        category = get_object_or_404(Category, pk=pk, company_id=company_id)
        form = CategoryForm(request.POST, request.FILES, instance=category)

        if form.is_valid():
            category = form.save(commit=False)
            category.company_id = company_id
            category.save()

            messages.success(request, "Category updated successfully.")
            return redirect('inventory:category_list')

        return render(request, 'category_form.html', {'form': form, 'role': role})


class CategoryDelete(View):
    def get(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to delete categories.")
            return redirect('inventory:category_list')

        category = get_object_or_404(Category, pk=pk, company_id=company_id)
        category.delete()

        messages.success(request, "Category deleted successfully.")
        return redirect('inventory:category_list')


#product

class ProductList(View):
    def get(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        category = get_object_or_404(Category, id=pk, company_id=company_id)

        products = Product.objects.filter(category=category, company_id=company_id)

        return render(request, 'product_list.html', {
            'category': category,
            'products': products,
            'role': role })


class ProductDetail(View):
    def get(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        product = get_object_or_404(Product, pk=pk, company_id=company_id)

        next_page = request.GET.get("next", "all_products")
        category_id = request.GET.get("category_id", "")

        return render(request, 'product_detail.html', {
            'product': product,
            'role': role,
            'next': next_page,
            'category_id': category_id
        })


class ProductCreate(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to add products.")
            return redirect('inventory:all_products')

        next_page = request.GET.get("next")
        category_id = request.GET.get("category_id")

        form = ProductForm(initial={'category': category_id} if category_id else None)
        form.fields['category'].queryset = Category.objects.filter(company_id=company_id)

        return render(request, 'product_form.html', {
            'form': form,
            'role': role,
            'next': next_page,
            'category_id': category_id
        })

    def post(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role not in ['Admin', 'Manager']:
            messages.error(request, "You don't have permission to add products.")
            return redirect('inventory:all_products')

        form = ProductForm(request.POST, request.FILES)
        next_page = request.POST.get("next")
        category_id = request.POST.get("category_id")
        form.fields['category'].queryset = Category.objects.filter(company_id=company_id)

        if form.is_valid():
            product = form.save(commit=False)
            product.company_id = company_id
            product.created_by = request.user
            product.save()

            messages.success(request, "Product added successfully.")

            if next_page == "category_products" and category_id:
                return redirect('inventory:product_list', pk=category_id)

            return redirect('inventory:all_products')

        return render(request, 'product_form.html', {
            'form': form,
            'role': role,
            'next': next_page,
            'category_id': category_id})


class ProductDelete(View):
    def post(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        if role == 'Staff':
            messages.error(request, "You don't have permission to delete products.")
            return redirect('inventory:all_products')

        product = get_object_or_404(Product, pk=pk, company_id=company_id)

        next_page = request.POST.get("next", None)
        category_id = request.POST.get("category_id", None)

        product.delete()
        messages.success(request, "Product deleted successfully.")

        if next_page == "category_products" and category_id:
            return redirect('inventory:product_list', pk=category_id)

        return redirect('inventory:all_products')


class ProductUpdate(View):
    def get(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        product = get_object_or_404(Product, pk=pk, company_id=company_id)

        if role == 'Staff':
            messages.error(request, "You can't edit full product details.")
            return redirect('inventory:product_stock', pk=product.pk)

        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(company_id=company_id)

        return render(request, 'product_form.html', {
            'form': form,
            'role': role,
            'product': product
        })

    def post(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        product = get_object_or_404(Product, pk=pk, company_id=company_id)

        if role == 'Staff':
            messages.error(request, "You can't edit full product details.")
            return redirect('inventory:product_stock', pk=product.pk)

        form = ProductForm(request.POST, request.FILES, instance=product)
        form.fields['category'].queryset = Category.objects.filter(company_id=company_id)

        if form.is_valid():
            product = form.save(commit=False)
            product.company_id = company_id
            product.save()

            messages.success(request, "Product updated successfully.")
            return redirect('inventory:product_detail', pk=pk)

        return render(request, 'product_form.html', {
            'form': form,
            'role': role,
            'product': product
        })


class StockUpdate(View):
    def get(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        product = get_object_or_404(Product, pk=pk, company_id=company_id)

        form = StockForm(instance=product)
        return render(request, 'stock_form.html', {
            'form': form,
            'product': product,
            'role': role
        })

    def post(self, request, pk):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        product = get_object_or_404(Product, pk=pk, company_id=company_id)

        form = StockForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, "Stock updated successfully.")
            return redirect('inventory:product_detail', pk=pk)

        return render(request, 'stock_form.html', {
            'form': form,
            'product': product,
            'role': role
        })

class IncreaseStock(View):
    def get(self, request, pk):
        company_id = get_user_company(request)

        product = get_object_or_404(Product, pk=pk, company_id=company_id)
        product.stock += 1
        product.save()

        return redirect('inventory:stock_update', pk=pk)


class DecreaseStock(View):
    def get(self, request, pk):
        company_id = get_user_company(request)

        product = get_object_or_404(Product, pk=pk, company_id=company_id)
        if product.stock > 0:
            product.stock -= 1
            product.save()

        return redirect('inventory:stock_update', pk=pk)


class AllproductsList(View):
    def get(self, request):
        company_id = get_user_company(request)
        role = get_user_role(request, company_id)

        products = Product.objects.filter(company_id=company_id)

        return render(request, 'all_product_list.html', {
            'products': products,
            'role': role})
