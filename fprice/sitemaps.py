from django.contrib.sitemaps import Sitemap
from fprice.models import ProductCategory

class ProductCategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ProductCategory.objects.all()
