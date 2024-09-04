from django.shortcuts import render, get_object_or_404
from .models import Category, Product
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, 
                                     slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})
# def product_detail(request, id, slug):
#     # product = get_object_or_404(Product,
#     #                             id=id,
#     #                             slug=slug,
#     #                             available=True)
#     # return render(request,
#     #               'shop/product/detail.html',
#     #               {'product': product})
#     from django.shortcuts import get_object_or_404, render
# from .models import Product

def product_detail(request, id, slug):
    print(f"Fetching product with ID: {id} and slug: {slug}")
    
    # Fetch the product
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    print(f"Product found: {product.name}")
    
    # Render the template
    return render(request, 'shop/product/detail.html', {'product': product})
