from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from lunch.models import Vendor

# Create your views here.

def lunch(request):
  return render(request, 'lunch/lunch.html', { 'vendors': Vendor.objects.order_by('-attended') })

def vendor(request, vendor_id):
  vendor = get_object_or_404(Vendor, pk=vendor_id)
  return render(request, 'lunch/vendor.html', {'vendor': vendor})
