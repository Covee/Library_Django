from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.contrib import admin


urlpatterns = [
    url(r'^catalog/', include('catalog.urls')),
    url(r'^$', RedirectView.as_view(url='/catalog/', permanent=True)),
    url(r'^admin/', admin.site.urls),
    url(r'accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
