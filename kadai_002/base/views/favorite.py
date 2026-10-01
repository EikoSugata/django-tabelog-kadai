from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Restaurant, Favorite
from django.shortcuts import redirect

class FavoriteCreateView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    # Favoriteテーブルに保存
    restaurant=Restaurant.objects.get(id=self.kwargs['pk'])
    Favorite.objects.create(
      restaurant_id=restaurant,
      user_id=request.user,
    )
    
    return redirect(f"/restaurants/{self.kwargs['pk']}/")

class FavoriteDeleteView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    # Favoriteテーブルから削除
    restaurant=Restaurant.objects.get(id=self.kwargs['pk'])
    favorite = Favorite.objects.filter(restaurant_id=restaurant, user_id=request.user)
    favorite.delete()

    return redirect(f"/restaurants/{self.kwargs['pk']}/")

class FavoriteListView(LoginRequiredMixin, ListView):
  model = Favorite
  template_name = 'pages/favorite.html'

  def get_queryset(self):
    return Favorite.objects.filter(user_id=self.request.user)