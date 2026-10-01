from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Order

class OrderListView(LoginRequiredMixin, ListView):
  model = Order
  template_name = 'pages/orders.html'
  ordering = '-created_at'

  def get_queryset(self):
    return Order.objects.filter(user_id=self.request.user).order_by('-created_at')