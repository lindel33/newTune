from cost_models.startsvc import get_cvs_data
from cost_models.models import CSVModel


def create_new_cvs():
    CSVModel.objects.all().delete()
    data = get_cvs_data()
    exit = []
    for i in data:
        if not i['Price']:
            i['Price'] = '0'

        exit.append(CSVModel(
            name=i['Title'],
            csv_id=i['Tilda UID'],
            cost=i['Price'], ))
    CSVModel.objects.bulk_create(
        exit
    )
