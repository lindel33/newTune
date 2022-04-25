from django.contrib import admin
from .models import DetailModel, NewPriceModel, ProviderModel
from .restart_csv import post_cvs1, new_cvs_data, restart_server
from django.shortcuts import redirect


def get_user_by_email(price):

    return DetailModel.objects.filter(new_line__icontains=f'{price}')


class UserEmailSearchAdmin(admin.ModelAdmin):
    def get_search_results(self, request, queryset, search_term):
        user = get_user_by_email(search_term)
        if user is not None:
            queryset = queryset.filter(new_line__icontains=search_term)
            use_distinct = False
        else:
            queryset, use_distinct = super().get_search_results(request,
                                                                queryset,
                                                                search_term)
        return queryset, use_distinct



@admin.register(DetailModel)
class GlobalAdmin(UserEmailSearchAdmin):
    list_display = ['new_line', 'cost', 'device', 'series', 'memory', 'color', 'region', 'provider', 'extra', ]
    search_fields = ('series', 'memory', 'color', 'device', 'provider', )
    from django.db.models import Q
    queryset = DetailModel.objects.all()
    for word in 'текст для поиска'.split():
        q_list = Q()
        q_list |= Q(series=word)
        queryset = queryset.filter(q_list)

@admin.register(NewPriceModel)
class NewPriceModelAdmin(admin.ModelAdmin):
    actions = ['download_csv', 'drop_csv', 'full_csv', 'ready_csv', 'not_update_csv']

    def download_csv(self, request, queryset):
        from django.http import HttpResponse
        f = open('/home/apple/code/project1/tune/cost_models/store.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=pricetilda.csv'
        return response



    def drop_csv(self, request, queryset):
        from django.http import HttpResponse

        post_cvs1(new_cvs_data())
#         restart_server()
#         import subprocess
#         bashCommand = "yc compute instance restart tunedjango"
#         process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#         output, error = process.communicate()
        return HttpResponse('Перезагрузка')


    def full_csv(self, request, *args, **kwargs):
        return redirect('/csv_check/full/')

    def ready_csv(self, request, *args, **kwargs):
        return redirect('/csv_check/ready/')

    def not_update_csv(self, request, *args, **kwargs):
        return redirect('/csv_check/not_update/')

    drop_csv.short_description = "Сбросить csv к нулевым ценам"
    download_csv.short_description = "Скачать новый csv с ценами"
    full_csv.short_description = "Посмотреть весь csv"
    ready_csv.short_description = "Посмотреть обновленные"
    not_update_csv.short_description = "Посмотреть не обновленные"





@admin.register(ProviderModel)
class ProviderModelAdmin(admin.ModelAdmin):
    pass
