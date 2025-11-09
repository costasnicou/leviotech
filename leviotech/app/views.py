from django.shortcuts import render, get_object_or_404
from . models import ProductCategory, Product, Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.templatetags.static import static
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
    og_image = request.build_absolute_uri(static('imgs/slider1.jpg'))
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
        'og_image': og_image,
        'now': datetime.now(),

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
    
    
    
    absolute_image_url = None

    img_obj = product.get_featured_image()   # <-- call the method

    if img_obj and getattr(img_obj, "image", None):  # adjust "image" to your field name
        # .url works only if the file exists and MEDIA_* are configured
        absolute_image_url = request.build_absolute_uri(img_obj.image.url)
   
    return render(request, 'app/product.html', {
        'menu_categories':menu_categories,
        'product':product,
        'product_images':product_images,
        'featured_products':featured_products,
        'sidebar_products':sidebar_products,
        'absolute_image_url': absolute_image_url,
        'now': datetime.now(),
    })

def category_detail(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    og_image = request.build_absolute_uri(static('imgs/breadcrumb-category.jpg'))
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
        'products':products,
        'og_image': og_image,
        'now': datetime.now(),
    })


def page_detail(request,slug):
    menu_categories = ProductCategory.objects.all()
    page = get_object_or_404(Page, slug=slug)
    og_image = request.build_absolute_uri(static('imgs/breadcrumb-legal.jpg'))
    return render(request,'app/page.html',{
        'page':page,
        'og_image':og_image,
        'menu_categories':menu_categories,
        'now': datetime.now(),
    })