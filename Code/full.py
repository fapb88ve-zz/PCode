import dropbox
import pandas as pd
import time
import datetime
import os
from PIL import Image
from moviepy.editor import *
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime
from email.mime.base import MIMEBase
import email.encoders as Encoders
import math
import numpy as np
import re
import shutil
import urllib.request
import imageio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
imageio.plugins.ffmpeg.download()


def have_internet():
    conn = urllib.request.urlopen("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


def files():
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


def watermark(x):
    for i in x:
        if 'AVI' in i:
            clip = VideoFileClip(i)
            # logo = (logo.set_duration(clip.duration)
            #        .resize(height=80)
            #        .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
            #       .set_pos(("right", "bottom")))
            logo = (ImageClip(logo_path)
                    .set_duration(clip.duration)
                    .resize(height=80)
                    .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
                    .set_pos(("right", "bottom")))
            final = CompositeVideoClip([clip, logo])
            final.write_videofile("Pancitas " + i + ".mp4")
        elif 'JPG' in i:
            plogo = Image.open(logo_path)
            plogow, plogoh = plogo.size
            plogo = plogo.resize((int(plogow * .1), int(plogoh * .1)))
            plogow, plogoh = plogo.size
            pic = Image.open(i)
            picw, pich = pic.size
            pic.paste(plogo, (picw - plogow, pich - plogoh), plogo)
            pic.save('Pancitas ' + i)
        elif 'MPG' in i:
            clip = VideoFileClip(i)
            # logo = (logo.set_duration(clip.duration)
            #        .resize(height=80)
            #        .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
            #       .set_pos(("right", "bottom")))
            logo = (ImageClip(logo_path)
                    .set_duration(clip.duration)
                    .resize(height=80)
                    .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
                    .set_pos(("right", "bottom")))
            final = CompositeVideoClip([clip, logo])
            final.write_videofile("Pancitas " + i + ".mp4")

        else:
            pass


def dl_files(x):
    df = pd.DataFrame(x.groupby('Nombre').Nombre.count())
    files = x.file_name
    try:
        os.chdir('.\\Clients')
    except Exception:
        os.mkdir('Clients')
    finally:
        for i in df.index:
            c_dir = 'Pancitas Ultrasound {}'.format(i.lower().title())
            try:
                os.mkdir(c_dir)
            except FileExistsError:
                shutil.rmtree(c_dir)
                os.mkdir(c_dir)
            finally:
                os.chdir('.\\' + c_dir)
                dl_df = []
                for k in files:
                    if i.upper() in k:
                        dl_df.append(k)
                for j in dl_df:
                    try:
                        f, metadata = client.get_file_and_metadata('/' + j)
                    except Exception:
                        while have_internet() != True:
                            print('No hay conneccion de Internet. Se intentara otra vez en 3 minutos.')
                            time.sleep(180)

                    finally:
                        out = open(j, 'wb')
                        out.write(f.read())
                        out.close()
                watermark(dl_df)
                for l in os.listdir(os.getcwd()):
                    if 'Pancitas' in l:
                        pass
                    else:
                        os.remove(l)
                send_mail(i)
                os.chdir('..\\')
                shutil.rmtree(c_dir)


def send_mail(x):
    name = x
    email = customers[customers.Nombre == x]['Email'].values[0]
    files = os.listdir(os.getcwd())
    size = [round(os.path.getsize(i) / 10**6, 2) for i in files]
    tot_size = sum(size)
    df_size = pd.DataFrame({'file': files, 'size': size})
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login('p.imagery.serv@gmail.com', 'rabbitrun88ve')
    except Exception:
        while have_internet() != True:
            print('No hay conneccion de Internet. Se intentara otra vez en 3 minutos.')
            time.sleep(180)
    finally:
        if tot_size >= 25:
            num_email = math.ceil(tot_size / 25)
            ord_email = [i * 25 for i in range(num_email + 1)]
            group_names = [i + 1 for i in range(num_email)]
            df_size['cumsum'] = df_size['size'].cumsum()
            df_size['send_mail'] = pd.cut(df_size['cumsum'], ord_email, labels=group_names)
            for j in group_names:
                chunk = df_size[df_size.send_mail == j]
                if j == 1:
                    txt = """
                    Hello {}!
                    \nYou are about to receive a couple of emails with all of your imagery from your session; this will be the 1st of {}.
                    \nShare your experience and enjoy a 15% discount on your next visit.
                    \nClick here to reedem: https://goo.gl/rC3z9H

                    \nWish you all the best! Come back soon :)

                    \nThanks
                    \nPancita’s Team
                    \nwww.pancitas.com
                    \n(305) 542-9931
                    """
                    txt_mail = txt.format(name, len(group_names))
                else:
                    txt = """
                    Hello!
                    \nThis is the email number {} of your imagery.
                    \nShare your experience and enjoy a 15% discount on your next visit.
                    \nClick here to reedem: https://goo.gl/rC3z9H

                    \nWish you all the best! Come back soon :)

                    \nThanks
                    \nPancita’s Team
                    \nwww.pancitas.com
                    \n(305) 542-9931
                    """
                    txt_mail = txt.format(j)
                msg = MIMEMultipart()
                msg['Subject'] = 'Ultrasound Imagery #{}'.format(j)
                msg['From'] = 'p.imagery.serv@gmail.com'
                msg['To'] = email
                msg.attach(MIMEText(txt_mail))
                for l in chunk.file:
                    if 'mp4' in l:
                        part = MIMEBase('application', "octet-stream")
                        fo = open(l, "rb")
                        part.set_payload(fo.read())
                        Encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(l))
                        msg.attach(part)
                    if 'JPG' in l:
                        img_data = open(l, 'rb').read()
                        image = MIMEImage(img_data, name=os.path.basename(l))
                        msg.attach(image)
                try:
                    s.sendmail('p.imagery.serv@gmail.com', email, msg.as_string())
                except Exception:
                    if have_internet() == False:
                        while have_internet() != True:
                            print('No hay conneccion de Internet. Se intentara otra vez en 3 minutos.')
                            time.sleep(180)
                    else:
                        email = 'vcalzadillag@gmail.com'
                        msg['To'] = email
                        s.sendmail('p.imagery.serv@gmail.com', email, msg.as_string())

        else:
            txt = '''
            Hello {}!
            \nHere are your imagery from today's session.
            \nShare your experience and enjoy a 15% discount on your next visit.
            \nClick here to reedem: https://goo.gl/rC3z9H
            \nWish you all the best! Come back soon :)

            \nThanks
            \nPancita’s Team
            \nwww.pancitas.com
            \n(305) 542-9931

            '''
            txt_mail = txt.format(name)
            msg = MIMEMultipart()
            msg['Subject'] = 'Ultrasound Imagery'
            msg['From'] = 'p.imagery.serv@gmail.com'
            msg['To'] = email
            msg.attach(MIMEText(txt_mail))
            files = os.listdir(os.getcwd())
            for l in files:
                if 'mp4' in l:
                    part = MIMEBase('application', "octet-stream")
                    fo = open(l, "rb")
                    part.set_payload(fo.read())
                    Encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(l))
                    msg.attach(part)

                if 'JPG' in l:
                    img_data = open(l, 'rb').read()
                    image = MIMEImage(img_data, name=os.path.basename(l))
                    msg.attach(image)

            try:
                s.sendmail('p.imagery.serv@gmail.com', email, msg.as_string())
            except Exception:
                if have_internet() == False:
                    while have_internet() != True:
                        print('No hay conneccion de Internet. Se intentara otra vez en 3 minutos.')
                        time.sleep(180)
                else:
                    email = 'vcalzadillag@gmail.com'
                    msg['To'] = email
                    s.sendmail('p.imagery.serv@gmail.com', email, msg.as_string())

        s.quit()


def customers():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_id.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Registro de Clientes').sheet1
    c_list = sheet.get_all_records()
    return pd.DataFrame(c_list)


def updat(a, b):
    c = []
    for i in range(len(b)):
        for j in range(len(a)):
            if a.Nombre.iloc[i] == b.Nombre.iloc[j]:
                c.append(False)
                break             # fix #1
        else:                     # fix #2
            c.append(True)

    return b[c]


def full():
    global sup
    #sup = input()
    # os.chdir('.\\Logo')

    global logo, plogo, plogow, plogoh, client, metadata, logo_path
    logo_path = os.path.abspath('.\\Logo\\pancita4.png')
    client = dropbox.client.DropboxClient('IS-424yqxy8AAAAAAAAVLOUS9urGIH4kCxP_5Q6hxdz-WrhGMYKa-9MjMZrpwMYZ')
    metadata = client.metadata('/')
    # Time Function
    d_files = files()
    global clients
    clients = clients()
    send_f = pd.merge(d_files, clients, left_on='c_name', right_on='Nombre',
                      how='inner')
    dl_files(send_f)


def full():
    global logo, plogo, plogow, plogoh, client, metadata, logo_path
    logo_path = os.path.abspath('.\\Logo\\pancita4.png')
    client = dropbox.client.DropboxClient('IS-424yqxy8AAAAAAAAVLOUS9urGIH4kCxP_5Q6hxdz-WrhGMYKa-9MjMZrpwMYZ')
    inst = 1
    while datetime.datetime.now().time() <= datetime.time(16, 00):
        if inst == 1:
            metadata = client.metadata('/')
            d_files = files()
            global customers
            customers = customers()
            print('El programa revisara dentro de 15 minutos.')
            send_f = pd.merge(d_files, customers, left_on='c_name', right_on='Nombre',
                              how='inner')
            dl_files(send_f)
        else:
            metadata = client.metadata('/')
            d_files = files()
            customers = updat(customers, customers())
            print('El programa revisara dentro de 15 minutos.')
            send_f = pd.merge(d_files, customers, left_on='c_name', right_on='Nombre',
                              how='inner')
            dl_files(send_f)
        time.sleep(15 * 60)
        inst += 1
    print('Le gustaria mantener funcionando el programa por un periodo adicional? (Indique su respuesta con un Si o un No)')
    resp1 = input()
    if 's' in resp1:
        print('Hasta que hora desea mantener el programa funcionando? (Favor utilizar format de hora de 24 horas, i.e.: 17:40')
        resp2 = input()
        hour = res2.split(':')[0]
        minutes = res2.split(':')[1]
        t_close = datetime.time(hour, minutes)
        while datetime.datetime.now().time() <= datetime.time(hour, minutes):
            metadata = client.metadata('/')
            d_files = files()
            customers = updat(customers, customers())
            send_f = pd.merge(d_files, customers, left_on='c_name', right_on='Nombre',
                              how='inner')
            dl_files(send_f)
            time.sleep(15 * 60)

    else:
        print('Hasta luego.')


if os.getcwd() != 'C:\\Users\\Frank Pinto\\desktop\\pds\\Pancitas\\Code':
    os.chdir('C:\\Users\\Frank Pinto\\desktop\\pds\\Pancitas\\Code')

full()
print(os.getcwd())
