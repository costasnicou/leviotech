from django.shortcuts import render, get_object_or_404
from . models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def homepage(request):
    # test='hello world'
    menu_categories = ProductCategory.objects.all()
    featured_products = Product.objects.filter(featured=True)
    best_deals = Product.objects.filter(best_deal=True).order_by('id')
    first_four_best_deals = best_deals[:4]
    last_four_best_deals = best_deals.order_by('-id')[:4]  # last 4 by id descending
    best_deal_star = Product.objects.filter(best_deal_star=True).first()
    category_laptops = Product.objects.filter(category__name="Laptops")[:10]
    category_pcs = Product.objects.filter(category__name="PC'S")[:10]
    category_keyboards = Product.objects.filter(category__name="Keyboards")[:10]
    category_mouses = Product.objects.filter(category__name="Mouse")[:10]
    category_headsets = Product.objects.filter(category__name="Headset")[:10]
    category_chairs = Product.objects.filter(category__name="Gaming Chairs")[:10]
    return render(request,'app/homepage.html',{
        'menu_categories':menu_categories,
        'featured_products':featured_products,
        'first_four_best_deals':first_four_best_deals,
        'last_four_best_deals':last_four_best_deals,
        'best_deal_star':best_deal_star,
        'category_laptops':category_laptops,
        'category_pcs':category_pcs,
        'category_keyboards':category_keyboards,
        'category_mouses':category_mouses,
        'category_headsets':category_headsets,
        'category_chairs':category_chairs,

    })

def product_detail(request, slug):
    # video_categories = VideoCategory.objects.all()
    product = get_object_or_404(Product, slug=slug)
    menu_categories = ProductCategory.objects.all()
    all_featured_products = Product.objects.filter(featured=True)
    featured_products = all_featured_products.order_by('id')[:5]
    # all images for this product
    reverse_products = Product.objects.filter(featured=True).order_by('id')
    sidebar_products= reverse_products.order_by('-id')[:3]
    product_images = product.images.all()
    return render(request, 'app/product.html', {
        'menu_categories':menu_categories,
        'product':product,
        'product_images':product_images,
        'featured_products':featured_products,
        'sidebar_products':sidebar_products,
    })

def category_detail(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    menu_categories = ProductCategory.objects.all()
    related_products = category.products.all()
    # post_list = Post.objects.filter(published=True).order_by('-created_at')

    paginator = Paginator(related_products, 10)  # 5 posts per page
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)



    return render(request, 'app/category.html', {
        'menu_categories':menu_categories,
        'category':category,
        'related_products':related_products,
        'products':products
    })

