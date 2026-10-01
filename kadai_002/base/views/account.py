from django.views.generic import CreateView, UpdateView
from base.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class SignUpView(CreateView):
  form_class = UserCreationForm
  success_url = '/login/'
  template_name = 'pages/login_signup.html'

  def form_valid(self, form):
    messages.success(self.request, '新規登録が完了しました。続けてログインしてください。')
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'ユーザー名が既に登録済みです。')
    return super().form_invalid(form)

class Login(LoginView):
  template_name = 'pages/login_signup.html'

  def form_invalid(self, form):
    messages.error(self.request, 'ユーザー名かパスワードが違います。')
    return super().form_invalid(form)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
  model = get_user_model()
  template_name = 'pages/account.html'
  fields = ('name', 'name_kana', 'phone_number', 'email',)
  success_url = '/account/'

  def get_object(self):
    # URL変数ではなく、現在のユーザーから直接pkを取得
    self.kwargs['pk'] = self.request.user.pk
    return super().get_object()

  def form_valid(self, form):
    messages.success(self.request, '会員情報の変更が完了しました。')
    return super().form_valid(form)
  
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
  template_name = 'pages/password.html'
  success_url = '/password/'

  def form_valid(self, form):
    messages.success(self.request, 'パスワードの変更が完了しました。')
    return super().form_valid(form)
