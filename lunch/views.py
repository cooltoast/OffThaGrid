from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from lunch.models import Vendor

# Create your views here.

def index(request):
# now = datetime.now()
# previous_midnight = datetime(now.year, now.month, now.day)
# thirty = previous_midnight - timedelta(days=30)
# Vendor.objects.filter(date__gte=thirty)
  return render(request, 'lunch/index.html', { 'vendors': Vendor.objects.order_by('-attended') })

def detail(request, vendor_id):
  vendor = get_object_or_404(Vendor, pk=vendor_id)
  return render(request, 'lunch/detail.html', {'vendor': vendor})
