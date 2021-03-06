from django.contrib import admin
from django.utils.safestring import mark_safe
from provider.models import ProviderProduct
from .models import Product, Category, SeriesCategory,\
    BookingProduct, GuarantyModel, KitModel, StateModel,\
    StaticUserHourModel, UserModel, RegionUserModel, SetTelegramModel, SendGlobalMessage


@admin.register(SendGlobalMessage)
class SendGlobalMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_id', 'first_name', 'last_name', 'region_user', 'notifications', ]
    search_fields = ('user_id', 'name', )

@admin.register(RegionUserModel)
class RegionUserModelAdmin(admin.ModelAdmin):
    pass


# @admin.register(SetTelegramModel)
# class SetTelegramModelAdmin(admin.ModelAdmin):
#     pass


@admin.register(StaticUserHourModel)
class StaticUserHourModelAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'full_id', 'hour_created', ]
    search_fields = ('hour_created', 'user_id', )

@admin.register(StateModel)
class StateModelAdmin(admin.ModelAdmin):
    pass



@admin.register(KitModel)
class KitModelAdmin(admin.ModelAdmin):
    product_ = Product.objects.all()
    bookingproduct = ProviderProduct.objects.all()

    def save_model(self, request, obj, form, change):
        for i in self.product_:
            if str(i.kit) == str(obj.kit):
                print(i.kit, obj.id)
                Product.objects.filter(id=i.id).update(kit=str(obj.id))
        for i in self.bookingproduct:
            if str(i.kit) == str(obj.kit):
                ProviderProduct.objects.filter(id=i.id).update(kit=str(obj.id))
        super().save_model(request, obj, form, change)
        

@admin.register(GuarantyModel)
class GuarantyModelAdmin(admin.ModelAdmin):
    product_ = Product.objects.all()
    bookingproduct = ProviderProduct.objects.all()

    def save_model(self, request, obj, form, change):
        for i in self.product_:
            if str(i.guaranty) == str(obj.guaranty):
                print(i.guaranty, obj.id)
                Product.objects.filter(id=i.id).update(guaranty=obj.id)
        for i in self.bookingproduct:
            if str(i.guaranty) == str(obj.guaranty):
                ProviderProduct.objects.filter(id=i.id).update(guaranty=obj.id)
        super().save_model(request, obj, form, change)
        



@admin.action(description='++ 1000 ?? ????????')
def plus(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='+')
    pass

@admin.action(description='-- 1000 ?? ????????')
def minus(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='-')
    pass

@admin.action(description='++ 4000 ?? ????????')
def plust(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='????????????????+')
    pass

@admin.action(description='-- 4000 ?? ????????')
def minust(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='????????????????-')
    pass

@admin.action(description='???????????????? ??????????????????')
def sell(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='??????????????')
    pass

@admin.action(description='+ 10 ??????????????????')
def cost10(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='????????10')
    pass

@admin.action(description='+ 20 ??????????????????')
def cost20(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='????????20')
    pass

@admin.action(description='+ 30 ??????????????????')
def cost30(modeladmin, request, queryset):
    for i in queryset:
        i.save(extra='????????30')
    pass

@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'article', 'category', 'series', 'sale', 'moderation', 'booking', 'sell', 'author', 'day_created', ]
    search_fields = ('name','article', 'provider_device', 'author__username', )
    exclude = ('name_tmp', 'up_price', 'author', 'day_next_publish', 'device_provider', 'www')
    actions = [plus, plust, minus, minust, cost10, cost20, cost30, sell, 'new_sale', 'drop_sale']
    list_filter = ('sell', 'booking', 'moderation', 'sale', 'author', )
    
    admin.site.site_header = 'TuneApple'
    admin.site.site_title = 'TuneAppleAdmin'
    admin.site.index_title = 'TuneApple'
    # def image_show(self, obj):
    #     if obj.image_1:
    #         return mark_safe("<img src='{}' width='60' />".format(obj.image_1))
    #     return 'None'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    @staticmethod
    @admin.action(description='???????????????? ??????????')
    def new_sale(modeladmin, request, queryset):
        all_pro = Product.objects.all()
        for i in all_pro:
            if i.sale == True:
                i.discount_cost = 0
                i.save()
        Product.objects.update(sale=False)
        import random
        queryset_products = all_pro.filter(sell=False).filter(moderation=True).filter(booking=False)
        exit_list = []
        while len(exit_list) != 10:

            import datetime

            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=5)
            random_index = random.randrange(len(queryset_products))
            sale_products = queryset_products[random_index]
            day_created = str(sale_products.day_created).split()[0]
            tomorrow = str(tomorrow).split()[0]
            if sale_products not in exit_list:
                if day_created < tomorrow:
                    sale_products.discount_cost = sale_products.price - 2000
                    sale_products.sale = True
                    sale_products.save()
                    exit_list.append(1)

#     @staticmethod
#     @admin.action(description='???????????????? ?????? ??????????')
#     def drop_sale(modeladmin, request, queryset):
#         all_pro = Product.objects.all()
#         for i in all_pro:
#             if i.sale == True:
#                 i.discount_cost = 0
#                 i.save()
#         Product.objects.update(sale=False)
    @staticmethod
    @admin.action(description='???????????????? ?????? ??????????')
    def drop_sale(modeladmin, request, queryset):
        all_pro = Product.objects.all()
        for i in all_pro:
            if i.sale == True:
                i.price = i.price + 2000
                i.save()
        Product.objects.update(sale=False)
#     def get_queryset(self, request):
#         return Product.objects.filter(sell=False)
        
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', ]


@admin.register(SeriesCategory)
class SeriesCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', ]


@admin.register(BookingProduct)
class BookingProductAdmin(admin.ModelAdmin):
    list_display = ['product_pka', 'booking_flag', 'sell_flag', 'name_user', 'phone', ]
    exclude = ('product_pka', 'date_sell', )
    search_fields = ['product_pka__name', 'product_pka__article', ]
