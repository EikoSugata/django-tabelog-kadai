from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Restaurant, Review
from django.contrib import messages
from django.shortcuts import redirect

class ReviewCreateView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):  
    restaurant=Restaurant.objects.get(id=self.kwargs['pk'])
  
    # レビュー済みチェック
    if Review.objects.filter(user_id=request.user, restaurant_id=restaurant):
      messages.error(request, '既にレビュー済みです。')
      return redirect(f"/restaurants/{self.kwargs['pk']}/")

    # Reviewテーブルに保存
    Review.objects.create(
      memo=request.POST.get('memo'),
      star_num=request.POST.get('star_num'),
      restaurant_id=restaurant,
      user_id=request.user,
    )
    
    return redirect(f"/restaurants/{self.kwargs['pk']}/")

class ReviewDeleteView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    # Reviewテーブルから削除
    restaurant=Restaurant.objects.get(id=self.kwargs['pk'])
    review = Review.objects.filter(restaurant_id=restaurant, user_id=request.user)
    review.delete()

    return redirect(f"/restaurants/{self.kwargs['pk']}/")