from django.conf import settings

def base(request):
  if request.user.is_authenticated:
    favorite_count = request.user.favorite_set.count()
  else:
    favorite_count = 0

  return {
    'TITLE': settings.TITLE,
    'FAVORITE_COUNT': favorite_count
  }