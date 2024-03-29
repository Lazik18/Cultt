from django.contrib import admin
from django.urls import path

from cultt_bot import views as cultt_bot_views

from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "The Cultt"
admin.site.site_title = "The Cultt"

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    # Редирект на админу
    path('', cultt_bot_views.admin_redirect),

    # Для телеграмма
    path('telegram_bot/<str:bot_url>', cultt_bot_views.web_hook_bot),

    # Вывод карточки заявки
    path('views/application/<int:application_id>', cultt_bot_views.views_application),

    # Статус заявки
    path('status', cultt_bot_views.web_hook_amocrm),

    # Для тестов
    path('test', cultt_bot_views.test),

    path('download', cultt_bot_views.download_file)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
