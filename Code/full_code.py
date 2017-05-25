import files
import watermark
import dl_files
import dropbox


def full():
    client = dropbox.client.DropboxClient(
        'IS-424yqxy8AAAAAAAAVLOUS9urGIH4kCxP_5Q6hxdz-WrhGMYKa-9MjMZrpwMYZ')
    sup = input()
    os.chdir('.\\Logo')
    logo = ImageClip("pancita4.png")
    plogo = Image.open("pancita4.png")
    plogow, plogoh = plogo.size
    plogo = plogo.resize((int(plogow * .1), int(plogoh * .1)))
    plogow, plogoh = plogo.size
    os.chdir('..')
    # Time Function
    files = files()
    clients = pd.read_excel('Registro de Clientes.xlsx')
    send_f = pd.merge(files, clients, left_on='c_name', right_on='Nombre',
                      how='inner')
    # dl_files(send_f)
    print(send_f)


# full()
os.getcwd()
