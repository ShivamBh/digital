from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

class ProductDetailView(DetailView):
	model = Product


class ProductListView(ListView):
	model = Product

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data()
		print(context)
		return context



# def product_detail_func(request, id):
# 	#instance = Product.objects.get(id=id)
# 	instance = get_object_or_404(Product, id=id)
# 	template = 'products/product_detail.html'
# 	context = {
# 		"object": instance
# }
# 	return render(request, template, context)





