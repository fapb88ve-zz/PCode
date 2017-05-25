import dropbox
import pandas as pd
import time
import datetime


def files():
    client = dropbox.client.DropboxClient(
        'IS-424yqxy8AAAAAAAAVLOUS9urGIH4kCxP_5Q6hxdz-WrhGMYKa-9MjMZrpwMYZ')
    metadata = client.metadata('/')
    files = [content['path'].split('/')[-1]
             for content in metadata['contents'] if content['is_dir'] == False]
    size = [round(content['bytes'] / 10**6, 2)
            for content in metadata['contents'] if content['is_dir'] == False]
    dates = [content['modified'] for content in metadata['contents'] if content['is_dir'] == False]
    name = [i[0:i.find('_')].lower().title() for i in files]
    files = pd.DataFrame({'file_name': files, 'c_name': name, 'size': size, 'dates': dates})
    files['date_mod_d'] = [time.strptime(i, "%a, %d %b %Y %H:%M:%S %z") for i in dates]
    files['date_mod_d'] = [datetime.datetime(
        *files.date_mod_d.loc[i][:6]) - datetime.timedelta(hours=4) for i in files.index]
    files['date_mod'] = [files.loc[i].date_mod_d.date() for i in files.index]
    files['hour_mod'] = [files.loc[i].date_mod_d.time() for i in files.index]
    #tday = datetime.datetime.today().date()
    #files = files[files.date_mod == tday]
    del files['date_mod_d'], files['dates']
    return files
