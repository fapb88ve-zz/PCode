import os
import pandas as pd
from PIL import Image
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import *


def watermark(x):
    for i in x:
        if 'AVI' in i:
            clip = VideoFileClip(i)
            logo = (logo.set_duration(clip.duration)
                    .resize(height=80)
                    .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
                    .set_pos(("right", "bottom")))
            # logo = (ImageClip("pancita4.png")
            #.set_duration(clip.duration)
           #   .resize(height=80)
            #  .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
            # .set_pos(("right","bottom")))
            final = CompositeVideoClip([clip, logo])
            final.write_videofile("Pancitas " + i + ".mp4")
        if 'JPG' in i:
            #plogo = Image.open("pancita4.png")
            #plogow, plogoh = plogo.size
            #plogo = plogo.resize((int(plogow*.1), int(plogoh*.1)))
            #plogow, plogoh = plogo.size
            pic = Image.open(i)
            picw, pich = pic.size
            pic.paste(plogo, (picw - plogow, pich - plogoh), plogo)
            pic.save('Pancitas ' + i)

        else:
            pass
