from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.views.static import serve


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
    path('api/', include('tune_admin.urls')),
    path('csv_check/', include('cost_models.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]
urlpatterns += [path('', admin.site.urls)]
