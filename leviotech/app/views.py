from django.shortcuts import render, get_object_or_404
from . models import ProductCategory, Product

# Create your views here.
def homepage(request):
    # test='hello world'
    menu_categories = ProductCategory.objects.all()
    featured_products = Product.objects.filter(featured=True)
    best_deals = Product.objects.filter(best_deal=True).order_by('id')

    first_four_best_deals = best_deals[:4]
    last_four_best_deals = best_deals.order_by('-id')[:4]  # last 4 by id descending
    best_deal_star = Product.objects.filter(best_deal_star=True).first()
    return render(request,'app/homepage.html',{
        'menu_categories':menu_categories,
        'featured_products':featured_products,
        'first_four_best_deals':first_four_best_deals,
        'last_four_best_deals':last_four_best_deals,
        'best_deal_star':best_deal_star,
    })

def product_detail(request, slug):
    # video_categories = VideoCategory.objects.all()
    product = get_object_or_404(Product, slug=slug)
    menu_categories = ProductCategory.objects.all()
    # all images for this product
    product_images = product.images.all()
    return render(request, 'app/product.html', {
        'menu_categories':menu_categories,
        'product':product,
        'product_images':product_images,
        # 'story': story,
        # 'video_categories':video_categories,
        # 'is_coach_story':is_coach_story,
    })
