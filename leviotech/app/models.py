from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from django.core.exceptions import ValidationError


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field('Content', config_name='extends')
    affiliate_url = models.URLField(max_length=500, blank=True, null=True)
    featured = models.BooleanField(default=False)
    best_deal = models.BooleanField(default=False)
    best_deal_star = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_featured_image(self):
        """Return the featured image object or the first one if none is marked."""
        featured = self.images.filter(is_featured=True).first()
        return featured or self.images.first()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.title} - Image"

    def clean(self):
        # Only check if product exists in DB
        if self.is_featured and self.product_id:
            existing_featured = ProductImage.objects.filter(
                product_id=self.product_id,
                is_featured=True
            ).exclude(pk=self.pk)
            if existing_featured.exists():
                raise ValidationError("Only one featured image is allowed per product.")

    def save(self, *args, **kwargs):
        # Automatically unset other featured images for this product
        if self.is_featured and self.product_id:
            ProductImage.objects.filter(
                product_id=self.product_id,
                is_featured=True
            ).exclude(pk=self.pk).update(is_featured=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
