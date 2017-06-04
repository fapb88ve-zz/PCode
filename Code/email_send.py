import dropbox
import pandas as pd
import time
import datetime
import os
from PIL import Image
import imageio
imageio.plugins.ffmpeg.download()
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


def send_mail():
    files = os.listdir(os.getcwd())
    size = [round(os.path.getsize(i) / 10**6, 2) for i in files]
    tot_size = sum(size)
    df_size = pd.DataFrame({'file': files, 'size': size})
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login('fapb88ve@gmail.com', ###)
    if tot_size >= 25:
        num_email = math.ceil(tot_size / 25)
        ord_email = [i * 25 for i in range(num_email + 1)]
        group_names = [i + 1 for i in range(num_email)]
        df_size['cumsum'] = df_size['size'].cumsum()
        df_size['send_mail'] = pd.cut(df_size['cumsum'], ord_email, labels=group_names)
        df_size['send_mail'] = pd.cut(df_size['cumsum'], ord_email, labels=group_names)
        for i in group_names:
            chunk = df_size[df_size.send_mail == i]
            if i == 1:
                txt = """
                Hello!
                \nYou are about to receive a couple of emails with all of your imagery from your session; this will be the 1st of {}.
                \nShare your experience and enjoy a 15% discount on your next visit.
                \nClick here to reedem: https://goo.gl/rC3z9H

                \nWish you all the best! Come back soon :)

                \nThanks
                \nPancita’s Team
                \nwww.pancitas.com
                \n(305) 542-9931
                """
                txt_mail = txt.format(len(group_names))
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
                txt_mail = txt.format(i)
            msg = MIMEMultipart()
            msg['Subject'] = 'Ultrasound Imagery #{}'.format(i)
            msg['From'] = 'fapb88ve@gmail.com'
            msg['To'] = 'fapb88ve@gmail.com'
            msg.attach(MIMEText(txt_mail))
            for l in chunk.file:
                print('Loading file {}'.format(l))

        else:
            txt_mail = '''
            Hello!
            \nThis is the email number {} of your imagery.
            \nShare your experience and enjoy a 15% discount on your next visit.
            \nClick here to reedem: https://goo.gl/rC3z9H

            \nWish you all the best! Come back soon :)

            \nThanks
            \nPancita’s Team
            \nwww.pancitas.com
            \n(305) 542-9931

            '''
            msg = MIMEMultipart()
            msg['Subject'] = 'Ultrasound Imagery #{}'.format(i)
            msg['From'] = 'fapb88ve@gmail.com'
            msg['To'] = 'fapb88ve@gmail.com'
            msg.attach(MIMEText(txt_mail))

    s.quit()


if os.getcwd() == 'C:\\Users\\Frank Pinto\\desktop\\pds\\Pancitas\\Code\\Clients\\Pancitas Ultrasound Carla Tavares 39':
    os.chdir('.\Clients\Pancitas Ultrasound Carla Tavares 39')
os.getcwd()
