from django.views.generic import ListView, DetailView
from base.models import Restaurant, Category, Favorite, Review
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexListView(LoginRequiredMixin, ListView):
  model = Category
  template_name = 'pages/index.html'

class CategoryListView(LoginRequiredMixin, ListView):
  model = Restaurant
  template_name = 'pages/list.html'
  paginate_by = 8

  def get_queryset(self):
    self.category = Category.objects.get(id=self.kwargs['pk'])
    return Restaurant.objects.filter(is_published=True, category_id=self.category)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = f'カテゴリ名 「{self.category.name}」で検索'
    return context
  
class RestaurantDetailView(LoginRequiredMixin, DetailView):
  model = Restaurant
  template_name = 'pages/restaurant.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Favoriteテーブルから値取得
    context['is_favorite'] = Favorite.objects.filter(
      restaurant_id=self.object,
      user_id=self.request.user
    ).exists()
      
    # Reviewテーブルからリスト取得
    context['review_list'] = Review.objects.filter(
      restaurant_id=self.object,
    )

    return context

class RestaurantListView(LoginRequiredMixin, ListView):
  model = Restaurant
  template_name = 'pages/list.html'
  paginate_by = 8

  def get_queryset(self):
    queryset = super().get_queryset()

    keyword=self.request.GET.get('name')
    if keyword:
      queryset=Restaurant.objects.filter(name__icontains=keyword)

    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    keyword=self.request.GET.get('name')
    if keyword:
      context['title'] = f'レストラン名 「{keyword}」で検索'
    else:
      context['title'] = f'レストラン名 「全て」で検索'
    return context
