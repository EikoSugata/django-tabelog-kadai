from django.contrib import admin
from base.models import Restaurant, Category, Reserve, Review, Favorite, User, Order
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from base.forms import UserCreationForm

class CustomUserAdmin(UserAdmin):
  fieldsets = (
    (None, {'fields': ('username', 'password', 'is_subscriber', 'is_admin',)}),
    (None, {'fields': ('name', 'name_kana', 'phone_number', 'email', 'stripe_id_subscription',)}),
  )

  search_fields = ('username', 'email') 
  list_display = ('username', 'email', 'is_subscriber', 'is_admin',)
  list_filter = ()
  ordering = ()
  filter_horizontal = ()

  add_fieldsets = (
    (None, {'fields': ('username', 'password',)}),
  )
  add_form = UserCreationForm

class CustomRestaurantAdmin(admin.ModelAdmin):
  search_fields = ("name",)
  list_display = ("name", "is_published", "category_id", )

class CustomCategoryAdmin(admin.ModelAdmin):
  search_fields = ("name",)

admin.site.register(Restaurant, CustomRestaurantAdmin)
admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(Reserve)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Order)
admin.site.unregister(Group)