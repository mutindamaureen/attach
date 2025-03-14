from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Django success")


urlpatterns = [
    path('', home_view, name='home'),  # Add the root URL mapping
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('activities.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

