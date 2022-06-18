def get_photo(series):
    name = series.replace(' ', '').lower()

    path_to_iphone = '/home/apple/code/project1/tune/tune_admin/ac_photo/'
    if 'iphone' in name:
      if 'iphone13mini' in name:
          return path_to_iphone + 'iphone/iphone_13_mini.jpg'

      if 'iphone13' in name and 'mini' not in name:
          return path_to_iphone + 'iphone/iphone_13.jpg'

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
