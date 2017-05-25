import dropbox
import pandas as pd
import watermark


def dl_files(x):
    df = pd.DataFrame(x.groupby('Nombre').Nombre.count())
    files = x.file_name
    os.chdir('.\\Clients')
    for i in df.index:
        c_dir = 'Pancitas Ultrasound {}'.format(i.lower().title())
        os.mkdir(c_dir)
        os.chdir('.\\' + c_dir)
        dl_df = []
        for k in files:
            if i.upper() in k:
                dl_df.append(k)
        for j in dl_df:
            f, metadata = client.get_file_and_metadata('/' + j)
            out = open(j, 'wb')
            out.write(f.read())
            out.close()
        watermark(dl_df)
        for l in os.listdir(c_dir):
            if 'Pancitas' in l:
                pass
            else:
                os.remove(l)
        os.chdir('..\\')
