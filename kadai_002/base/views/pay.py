import stripe
from django.conf import settings
from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Order, Reserve
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib import messages

stripe.api_key = settings.STRIPE_API_SECRET_KEY

class PaySuccessView(LoginRequiredMixin, TemplateView):
  template_name = 'pages/success.html'

  def get(self, request, *args, **kwargs):
    # checkout_sessionで渡したクエリを取得
    order_id = request.GET.get('order_id')
    # 対象のOrderオブジェクトを取得し、注文確定に変更
    order = Order.objects.filter(user_id=request.user, id=order_id)[0]
    order.is_confirmed = True  # 注文確定
    order.save()

    # クレジットカード情報を保存して、有料会員に変更
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    user = request.user
    user.is_subscriber = True
    user.stripe_id_subscription = session.subscription
    user.save()

    return super().get(request, *args, **kwargs)

class PayCancelView(LoginRequiredMixin, TemplateView):
  template_name = 'pages/cancel.html'

  def get(self, request, *args, **kwargs):
    # 現userの仮Orderオブジェクトのリストを全削除
    orders = Order.objects.filter(user_id=request.user, is_confirmed=False)
    orders.delete()

    return super().get(request, *args, **kwargs)

def check_account_filled(user):
  if user.name is None or user.name == '':
    return False
  if user.name_kana is None or user.name_kana == '':
    return False
  if user.phone_number is None or user.phone_number == '':
    return False
  if user.email is None or user.email == '':
    return False
  return True

def create_line_item():
  return [{
    'price_data': {
      'currency': 'JPY',
      'unit_amount': 300,
      'product_data': {'name': "NAGOYAMESHI有料会員(月額)", },
      "recurring": {"interval": "month", },  # 毎月課金
    },
    'quantity': 1,
  }]

class PayWithStripe(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    if not check_account_filled(request.user):
      messages.error(request, '有料会員になるため会員情報を全て入力してください。')
      return redirect('/account/')

    # 仮注文を作成（is_confirmed=Flase)
    order = Order.objects.create(
      amount=300,
      subscription_start_at=timezone.now(),
      subscription_end_at=timezone.now()+relativedelta(months=1, days=-1),
      user_id=request.user,
    )

    checkout_session = stripe.checkout.Session.create(
      customer_email=request.user.email,
      payment_method_types=['card'],
      line_items=create_line_item(),
      mode='subscription',
      success_url=f'{settings.MY_URL}/pay/success/?order_id={order.pk}&session_id={{CHECKOUT_SESSION_ID}}',
      cancel_url=f'{settings.MY_URL}/pay/cancel/?order_id={order.pk}',
    )
  
    return redirect(checkout_session.url)

class CancelWithStripeView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    # 未来予約チェック
    if Reserve.objects.filter(user_id=request.user, reserve_at__gt=timezone.now()).exists():
      messages.error(request, '未来の予約があるため解約できません。')
      return redirect("/reserve/")

    # Stripe側のサブスクリプションをキャンセル(解約)
    stripe.Subscription.delete(request.user.stripe_id_subscription)
    
    # クレジットカード情報を削除して、無料会員に変更
    request.user.is_subscriber = False
    request.user.stripe_id_subscription = None
    request.user.save()

    messages.success(request, "有料プランを解約しました。")

    return redirect('/account/')