from django.db import models
from django.urls import reverse

from category.models import Category


class Product(models.Model):
    title        = models.CharField(max_length=255)
    author       = models.CharField(max_length=255)
    editorial    = models.CharField(max_length=255)
    slug         = models.SlugField(unique=True)
    description  = models.TextField()
    price        = models.IntegerField()
    stock        = models.IntegerField()
    image        = models.ImageField(upload_to='products')
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    modified_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('title', )

    def get_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title
    
class VariationManager(models.Manager):
    def stock(self):
        return super(VariationManager, self).filter(variation_category='stock', is_active=True)

variation_category_choice = (
    ('stock', 'stock'),
)

class Variation(models.Model):
    product            = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value    = models.IntegerField()
    is_active          = models.BooleanField(default=True)
    created_date       = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value