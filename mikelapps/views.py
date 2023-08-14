#from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Product, Entry
from .forms import ProductForm, EntryForm

# Create your views here.

def index(request):
    """The home page for Mikel App."""
    return render(request, 'mikelapps/index.html')

@login_required
def products(request):
    """Show all products."""
    products = Product.objects.filter(owner=request.user).order_by('date_added')
    context = {'products': products}
    return render(request, 'mikelapps/products.html', context)

@login_required
def product(request, product_id):
    """Show a single product and all its entries."""
    product = Product.objects.get(id=product_id)
    # Make sure the product belongs to the current user.
    if product.owner != request.user:
        raise Http404

    entries = product.entry_set.order_by('-date_added')
    context = {'product': product, 'entries': entries}
    return render(request, 'mikelapps/product.html', context)

@login_required    
def new_product(request):
    """Add a new product."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ProductForm()
    else:
        # POST data submitted; process data.
        form = ProductForm(data=request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.owner = request.user
            new_product.save()
            return redirect('mikelapps:products')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'mikelapps/new_product.html', context)

@login_required    
def new_entry(request, product_id):
    """Add a new entry for a particular product."""
    product = Product.objects.get(id=product_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.product = product
            new_entry.save()
            return redirect('mikelapps:product', product_id=product_id)

    # Display a blank or invalid form.
    context = {'product': product, 'form': form}
    return render(request, 'mikelapps/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    product = entry.product
    if product.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('mikelapps:product', product_id=product.id)

    context = {'entry': entry, 'product': product, 'form': form}
    return render(request, 'mikelapps/edit_entry.html', context)