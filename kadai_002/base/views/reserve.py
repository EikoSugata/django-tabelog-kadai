from django.views.generic import View, ListView
from base.models import Reserve, Restaurant
from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class ReserveListView(LoginRequiredMixin, ListView):
  model = Reserve
  template_name = 'pages/reserve.html'

  def get_queryset(self):
    return Reserve.objects.filter(user_id=self.request.user)


class ReserveCreateView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    restaurant=Restaurant.objects.get(id=self.kwargs['pk'])
    reserve_at = request.POST.get('reserve_at')

    if reserve_at:
      reserve_at = datetime.strptime(reserve_at, "%Y-%m-%dT%H:%M")

      # 過去日時チェック
      if reserve_at < datetime.now():
        messages.error(request, '過去の日時は選択できません。現在より後の日時を選択してください。')
        return redirect(f"/restaurants/{self.kwargs['pk']}/")

      # 営業時間チェック
      # 通常営業パターン
      reserve_time = (reserve_at.time())
      if restaurant.open_time <= restaurant.close_time:
        if not (restaurant.open_time <= reserve_time <= restaurant.close_time):
          messages.error(request, f"営業時間外です。（営業時間：{restaurant.open_time.strftime('%H:%M')}〜{restaurant.close_time.strftime('%H:%M')}）")
          return redirect(f"/restaurants/{self.kwargs['pk']}/")
      # 深夜営業パターン(閉店時間に24時間プラスして考える)
      else:
        reserve_m = to_minutes(reserve_time)
        open_m = to_minutes(restaurant.open_time)
        close_m = to_minutes(restaurant.close_time) + 1440 #閉店時間を翌日扱いにする

        # 予約時間が深夜の場合、翌日扱いにする
        if reserve_m < open_m:
          reserve_m += 1440

        if not (open_m <= reserve_m <= close_m):
          messages.error(request, f"営業時間外です。（営業時間：{restaurant.open_time.strftime('%H:%M')}〜翌{restaurant.close_time.strftime('%H:%M')}）")
          return redirect(f"/restaurants/{self.kwargs['pk']}/")
      
      # 予約済みチェック
      if Reserve.objects.filter(user_id=request.user, reserve_at=reserve_at):
        messages.error(request, 'その時間は予約済みです。')
        return redirect(f"/restaurants/{self.kwargs['pk']}/")

      # DB登録
      Reserve.objects.create(
        reserve_at=reserve_at,
        people_num=int(request.POST.get('people_num')),
        restaurant_id=restaurant,
        user_id=request.user,
      )

    return redirect('/reserve/')

# 時刻(time)を0時から通算した「分」に変換する処理
def to_minutes(t):
  return t.hour * 60 + t.minute

class ReserveDeleteView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    reserve= Reserve.objects.get(id=self.kwargs['pk'])
    reserve.delete()

    return redirect('/reserve/')