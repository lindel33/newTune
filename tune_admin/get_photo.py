import re


def get_photo(series):
    name = series.replace(' ', '').lower()

    path_to_iphone = 'C:\\Users\\lindel\\Py_Projects\\newTune\\tune_admin\\ac_photo\\'
    if 'iphone' in name:
        if 'iphone13mini' in name:
            return path_to_iphone + 'iphone/iphone_13_mini.jpg'

        if 'iphone13' in name and 'mini' not in name:
            return path_to_iphone + 'iphone/iphone_13_mini.jpg'

        if 'iphone12mini' in name:
            return path_to_iphone + 'iphone/iphone_12.jpg'

        if 'iphone12' in name and 'mini' not in name:
            return path_to_iphone + 'iphone/iphone_12.jpg'

        if 'iphone11' in name and 'mini' not in name:
            return path_to_iphone + 'iphone/iphone_11.jpg'

        if 'iphonese' in name:
            return path_to_iphone + 'iphone/iphone_se.PNG'

        if 'iphonexr' in name:
            return path_to_iphone + 'iphone/iphone_xr.jpg'

    if 'series' in name:
        if 'series3' in name:
            return path_to_iphone + 'watch/watch_3.jpg'

        if 'series6' in name:
            return path_to_iphone + 'watch/watch_6.jpg'

        if 'series7' in name:
            return path_to_iphone + 'watch/watch_7.jpg'

        if 'seriesse' in name:
            return path_to_iphone + 'watch/watch_se.jpg'

    if 'ipad' in name:
        if 'pro' in name and '11' in name:
            return path_to_iphone + 'ipad/Pro_11_2021.jpg'

        if 'pro' in name and '12' in name:
            return path_to_iphone + 'ipad/Pro_12_2021.jpg'

        if 'air' in name:
            return path_to_iphone + 'ipad/air_2021.jpg'

        if 'mini' in name:
            return path_to_iphone + 'ipad/mini_6.jpg'

        if re.findall('2019|2020|2021|2022|2023|2024', name) and len(name.split()) == 1:
            return path_to_iphone + 'ipad/mini_6.jpg'

    if 'airpods' in name:
        if 'airpods' in name and 'max' not in name:
            return path_to_iphone + 'airpods/airpods_mix.JPG'
        if 'airpods' in name and 'max' in name:
            return path_to_iphone + 'airpods/airpods_max.JPG'

    if 'macbook' in name:
        if 'macbook' in name:
            return path_to_iphone + 'macbook/mac.jpg'
