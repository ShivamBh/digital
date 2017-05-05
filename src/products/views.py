from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import VariationInventoryFormSet
from .mixins import StaffRequiredmixin, LoginRequiredMixin
from .models import Product, Variation, Category

# Create your views here.

class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = "products/product_list.html"

class CategoryDetailView(DetailView):
	model = Category

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = (product_set | default_products).distinct()
		context["products"] = products
		return context

class ProductDetailView(DetailView):
	model = Product

class VariationListView(StaffRequiredmixin, ListView):
	model = Variation

	def get_context_data(self, *args, **kwargs):
		context = super(VariationListView, self).get_context_data(*args, **kwargs)
		context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):
		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk=product_pk)
			queryset = Variation.objects.filter(product=product)
		return queryset

	def post(self, request, *args, **kwargs):
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				#print("New item: ",new_item)
				#if new_item.title:

				product_pk = self.kwargs.get("pk")
				product = get_object_or_404(Product, pk=product_pk)
				
				new_item.product = product
				new_item.save()

			messages.success(request, "Your inventory has been updated.")
			return redirect("products")
		print (request.POST)
		raise Http404	

class ProductListView(ListView):
	model = Product

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q")
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) | 
				Q(description__icontains=query)
				)

			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs


# def product_detail_func(request, id):
# 	#instance = Product.objects.get(id=id)
# 	instance = get_object_or_404(Product, id=id)
# 	template = 'products/product_detail.html'
# 	context = {
# 		"object": instance
# }
# 	return render(request, template, context)





