from django.shortcuts import render, get_object_or_404
from . models import ProductCategory, Product, Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.templatetags.static import static
from django.views.decorators.cache import cache_page


@cache_page(60 * 5)  # cache the homepage for 5 minutes
def homepage(request):
    menu_categories = ProductCategory.objects.all()
    base_qs = Product.objects.select_related("category")

    featured_products = base_qs.filter(featured=True)

    best_deals_qs = base_qs.filter(best_deal=True)
    first_four_best_deals = best_deals_qs.order_by("id")[:4]
    last_four_best_deals = best_deals_qs.order_by("-id")[:4]

    best_deal_star = base_qs.filter(best_deal_star=True).first()

    wanted_names = ["Laptops", "PC'S", "Keyboards", "Mouse", "Headset", "Gaming Chairs"]
    category_lists = {name: [] for name in wanted_names}

    cat_products = (
        base_qs
        .filter(category__name__in=wanted_names)
        .order_by("category__name", "-created_at")
    )

    for p in cat_products:
        name = p.category.name
        if len(category_lists[name]) < 10:
            category_lists[name].append(p)

    og_image = request.build_absolute_uri(static("imgs/slider1.jpg"))

    return render(request, "app/homepage.html", {
        "menu_categories": menu_categories,
        "featured_products": featured_products,
        "first_four_best_deals": first_four_best_deals,
        "last_four_best_deals": last_four_best_deals,
        "best_deal_star": best_deal_star,
        "category_laptops": category_lists["Laptops"],
        "category_pcs": category_lists["PC'S"],
        "category_keyboards": category_lists["Keyboards"],
        "category_mouses": category_lists["Mouse"],
        "category_headsets": category_lists["Headset"],
        "category_chairs": category_lists["Gaming Chairs"],
        "og_image": og_image,
        "now": datetime.now(),
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