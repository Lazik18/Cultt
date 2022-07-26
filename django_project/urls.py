from django.contrib import admin
from django.urls import path

from cultt_bot import views as cultt_bot_views

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    # Редирект на админу
    path('/', cultt_bot_views.admin_redirect),

    # Для телеграмма
    path('telegram_bot/<str:bot_url>', cultt_bot_views.web_hook_bot),
]
