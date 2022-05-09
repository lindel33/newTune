from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.admin import AdminSite
from django.http import HttpResponse


class MyAdminSite(AdminSite):

     def get_urls(self):
         from django.urls import path
         urls = super().get_urls()
         urls += [
             path('my_view/', self.admin_view(self.my_view))
         ]
         return urls

     def my_view(self, request):
         return HttpResponse("Hello!")

admin_site = MyAdminSite()


urlpatterns = [
    path('/', admin.site.urls),
    path('api/', include('tune_admin.urls')),
    path('csv_check/', include('cost_models.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
