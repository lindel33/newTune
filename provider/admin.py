from django.contrib import admin
from .models import ProviderProduct


@admin.register(ProviderProduct)
class ProviderProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'provider_device']
    exclude = ('booking', 'count', 'moderation', 'up_price', 'day_next_publish', 'name_tmp', 'device_provider', 'provider_device', 'author')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        if not obj.guaranty:
            obj.guaranty = None
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        ss = ProviderProduct.objects.filter(author=request.user)
        return ss
    
    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.readonly_fields = ['image_1',
                       'image_2',
                       'image_3',
                       'price',
                       'smile',
                       'name',
                       'tests',
                       'article',
                       'state',
                       'state_akb',
                       'works',
                       'kit',
                       'guaranty',
                       'custom_guaranty',
                       'base_text',
                       'regin',
                       'category',
                       'series',
                      ]
        self.fields = ['image_1',
                       'image_2',
                       'image_3',
                       'sell',
                       'booking',
                       'price',
                       'smile',
                       'name',
                       'tests',
                       'article',
                       'state',
                       'state_akb',
                       'works',
                       'kit',
                       'guaranty',
                       'custom_guaranty',
                       'base_text',
                       'regin',
                       'category',
                       'series',
                      ]

        return self.changeform_view(request, object_id, form_url, extra_context)
