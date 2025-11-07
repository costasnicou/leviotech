from django.contrib import admin
from django.utils.html import format_html
from .models import ProductCategory, Product, ProductImage,Page


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:80px; border-radius:6px; object-fit:cover;" />',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'title', 'category', 'featured', 'created_at')
    list_filter = ('featured', 'category')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]

    def thumbnail(self, obj):
        # Show featured image thumbnail (or fallback to first image)
        featured_img = obj.images.filter(is_featured=True).first() or obj.images.first()
        if featured_img and featured_img.image:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:4px; object-fit:cover;" />',
                featured_img.image.url
            )
        return "—"
    thumbnail.short_description = "Image"

admin.site.register(Page)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}