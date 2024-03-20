from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

from .models import Record, Redevance
from .redevance import compter_vol
from .models import Fichier
from .forms import FichierForm, UpdateRedevanceForm
from uuid import uuid4
from datetime import datetime

from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.http import FileResponse
import os
import os
import pandas as pd


# - Homepage 

def home(request):

    return render(request, 'webapp/index.html')


# - Register a user

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully!")

            return redirect("my-login")

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)


# - Login a user

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/my-login.html', context=context)

# - Dasboard
@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)
def dashboard2(request):

    my_records = Redevance.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/dashboard2.html', context=context)

def views_table(request):
    my_records = Redevance.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/views_table.html', context=context)

@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was created!")

            return redirect("dashboard")

    context = {'form': form}

    return render(request, 'webapp/create-record.html', context=context)


# - Update a record 

@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was updated!")

            return redirect("dashboard")
        
    context = {'form':form}

    return render(request, 'webapp/update-record.html', context=context)

@login_required(login_url='my-login')
def update_redevance(request, pk):

    record = Redevance.objects.get(id=pk)

    form = UpdateRedevanceForm(instance=record)

    if request.method == 'POST':

        form = UpdateRedevanceForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was updated!")

            return redirect("dashboard2")
        
    context = {'form':form}

    return render(request, 'webapp/update-redevance.html', context=context)

# - Read / View a singular record

@login_required(login_url='my-login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/view-record.html', context=context)

@login_required(login_url='my-login')
def singular_redevance(request, pk):

    all_records = Redevance.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/view-redevance.html', context=context)



# - Delete a record

@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("dashboard")

def upload(request):
    print(request)
    if request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        if not uploaded_file.name.endswith('.xlsx'):
            return render(request, 'webapp/upload.html', context={'error': 'Please upload a valid .xlsx file.'})
        
        # Save the uploaded file with a unique filename
        file_path = f'/home/dev-data/testpdf/exo/crm/{generate_unique_filename(uploaded_file.name)}'
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Pass the uploaded file path to the download view
        #return redirect('download', filepath=file_path)
        print("**************")
        df = pd.read_excel(file_path)
        print(df.head())
    
    return render(request, 'webapp/upload.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        print("***********")
        print(uploaded_file)
        # récupérer le chemin du répertoire courant
        path = os.getcwd()
        print("Le répertoire courant est : " + path)
        # récupérer le nom du répertoire courant
        repn = os.path.basename(path)
        print("Le nom du répertoire est : " + repn)
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file, uploaded_file)
        uploaded_file_url = str(path)+str(fs.url(filename))
        #uploaded_file = str(path)+"/"+str(uploaded_file)
        print(uploaded_file_url)

        file=traitement(request,uploaded_file_url)
        print("-+-+-+-+")
        return render(request, 'webapp/traitement_fin.html', {'file': file})
    else:
        return render(request, 'webapp/upload_file.html')

def generate_unique_filename(filename):
    # This function generates a unique filename to avoid overwriting
    import uuid
    base, ext = os.path.splitext(filename)
    return f'{base}_{uuid.uuid4()}{ext}'

def traitement(request, filepath):
    # Define the base directory where the files are located
    base_dir = '/home/dev-data/testpdf/exo/crm/'
        
    numero_vol = 1

    print("Lancement de la lecture du fichier xslx:")
    print(filepath)

    df = pd.read_excel(filepath)

    df.info()

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    df['initial_flight_rule'].value_counts()

    df[df['flpl_call_sign'] == 'FGOLS']



    df.head()

    test = 20230522000000

    df[df['file_date']==test]

    


    # Appeler la fonction
    nb_lignes,df_facture = compter_vol(df.copy(),int(20230521000000))

    # Afficher le résultat
    print(f"Nombre de vols répondant aux conditions: {nb_lignes}")

    def filtrer_vols(dataframe):
        print('debutfilteretvol')
    
        # Définir les mots à rechercher dans la colonne FTFM_FIELD15
        mots_recherches = ['OTARO', 'DOLIS', 'KAMER', 'REQIN', 'SALMA', 'CIRTA', 'MOUET']

        # Filtrer les vols répondant aux conditions
        df_facture = dataframe[dataframe['flpl_depr_airp'].str.startswith('LF')]

        print('apresnpremier filtre')
        # Filtrer les vols où la colonne flpl_arrv_airp commence par L ou E et que FTFM_FIELD15 contient un des mots de la liste
        df_facture = pd.concat([df_facture, dataframe[(dataframe['flpl_arrv_airp'].str.startswith('L') | dataframe['flpl_arrv_airp'].str.startswith('E')) & dataframe['ftfm_field15'].str.contains('|'.join(mots_recherches))]], ignore_index=True)

        return df_facture
    
    
    print('avantfilteretvol')

    # Appeler la fonction
    df_facture = filtrer_vols(df.copy())

    # Afficher le nombre de vols sélectionnés
    print(f"Nombre de vols sélectionnés: {df_facture.shape[0]}")

    def filtrer_vols(dataframe,filedate):

        mots_recherches = ["OTARO", "DOLIS", "KAMER", "REQIN", "SALMA", "CIRTA", "MOUET"," CSO "," ANB "," BJA "," ZEM "]
        dataframe = dataframe[dataframe['file_date']==filedate]

        return dataframe.loc[(dataframe['flpl_depr_airp'].str.startswith('LF')) |
                        ((dataframe['flpl_arrv_airp'].str.startswith('L') |
                        dataframe['flpl_arrv_airp'].str.startswith('E')) &
                        (dataframe['ftfm_field15'].str.contains('|'.join(mots_recherches)) |
                            dataframe['ctfm_field15'].str.contains('|'.join(mots_recherches))))]


    # Appeler la fonction
    df_facture = filtrer_vols(df.copy(),20230522000000)

    # Afficher le nombre de vols sélectionnés
    print(f"Nombre de vols sélectionnés: {df_facture.shape[0]}")

    df_facture = df_facture.sort_values(by='flpl_call_sign', ascending=True)

    df_facture = df_facture.reset_index()

    df_facture.head(10)

    df.info()

    df_facture['eobt'] = df_facture['eobt'].apply(str)
    df_facture['aobt'] = df_facture['aobt'].apply(str)

    df_facture = df_facture.fillna(' ')

    def generate_transmission(df):

        # Initialiser le compteur de position
        num = 1

        # Créer une nouvelle colonne vide
        df['transmission'] = ''

        for index, row in df.iterrows():
            # Générer la partie numérique de la transmission
            num_str = f"{num:04d}"
            # Concaténer les autres éléments de la transmission
            transmission = num_str
            transmission += "F"
            transmission += row['aobt'][8:12]
            transmission += row['flpl_depr_airp']
            transmission += row['flpl_arrv_airp']
            transmission += row['flpl_call_sign'].strip().ljust(9)
            transmission += 'Z'
            transmission += row['airc_type'].strip().ljust(7)
            transmission += 'Z  '
            transmission += str(row['ifps_registration_mark']).strip().ljust(9)
            transmission +=  f"{' ' * 21}"
            transmission += row['eobt'][7:9]
            transmission += row['eobt'][5:7] + row['eobt'][:5] + str(row['nm_ifps_id']).strip().ljust(10) + f"{' ' * 39}" + '1' + str(row['airc_modes_address']).strip().ljust(6)

            # Incrémenter le compteur de position
            num += 1

            # Affecter la valeur à la cellule courante
            df.loc[index, 'transmission'] = transmission

        return df

    # Appeler la fonction
    statut = 'F'
    df_facture = generate_transmission(df_facture.copy())

    # Afficher les premières lignes du DataFrame
    print(df_facture.head())

    df_facture['transmission'][8]

    df_facture.shape[0]

    df.head()

    df_facture[df_facture['flpl_call_sign'] == 'AFR11PM']

    df_facture[df_facture['airc_type'] == 'TBM9']

    print(df_facture['transmission'][2169])


    # Ouvrir le fichier en mode lecture
    fichier = open("/home/dev-data/testpdf/exo/crm/M-LF-20230601-090935-001-CESNAC.txt", "r")
    # Lire toutes les lignes du fichier
    lignes = fichier.readlines()
    # Fermer le fichier
    fichier.close()
    # Créer un tableau vide
    tableau_cesnac = []
    tableau_said = []

    # Parcourir la liste des lignes
    for ligne in lignes:
        # Extraire les 26 premiers caractères de la ligne
        caracteres = ligne[9:26]
        # Ajouter les caractères au tableau
        tableau_cesnac.append(caracteres)

    for ligne in df_facture['transmission']:
        # Extraire les 26 premiers caractères de la ligne
        caracteres = ligne[9:26]
        # Ajouter les caractères au tableau
        tableau_said.append(caracteres)

    print(tableau_said)

    print(tableau_cesnac)

    if tableau_cesnac[1] == tableau_said[0]:
        print('egalité')
    else:
        print(tableau_cesnac[1],'!=',tableau_said[0])

    len(tableau_cesnac[1])

    len(tableau_said[0])

    df_facture[df_facture['flpl_call_sign'] == 'DAH1162']

    df[df['flpl_call_sign'] == 'AFR87LH']

    df_facture[df_facture['flpl_call_sign'] == 'AFR98ML']

    df_facture[(df_facture['flpl_depr_airp'] == 'LFBO') & (df_facture['flpl_arrv_airp'] == 'LFBO')]

    df[(df['flpl_depr_airp'] == 'LFBO') & (df['flpl_arrv_airp'] == 'LFBO')]

    df_facture[df_facture['airc_type'] == 'TIGR']

    df[df['airc_type'] == 'TIGR']

    nombre_differences = 0
    # Parcourir le premier tableau
    for i,valeur1 in enumerate(tableau_cesnac):
        # Vérifier si la valeur du premier tableau n'est pas dans le deuxième tableau
        nb = nombre_differences
        if valeur1 not in tableau_said:
            # Il y a une différence
            # Ajouter la valeur à la liste des différences
            print('cette valeur n\'estpas dans said',valeur1,' index : ',i, ' total : ',lignes[i])

            # Incrémenter le compteur de différences
            nombre_differences += 1
        #if nb < nombre_differences:
        #  print(lignes[i])
    print('nb duff = ',nombre_differences)



    # Ouvrir le fichier en mode lecture
    fichier = open("/home/dev-data/testpdf/exo/crm/M-LF-20230601-090935-001-CESNAC.txt", "r")
    # Lire toutes les lignes du fichier
    lignes = fichier.readlines()
    # Fermer le fichier
    fichier.close()
    # Créer un tableau vide
    tableau_cesnac = []
    tableau_said = []

    # Parcourir la liste des lignes
    for ligne in lignes:
        # Extraire les 26 premiers caractères de la ligne
        caracteres = ligne[9:26]
        # Ajouter les caractères au tableau
        tableau_cesnac.append(caracteres)

    for ligne in df_facture['transmission']:
        # Extraire les 26 premiers caractères de la ligne
        caracteres = ligne[9:26]
        # Ajouter les caractères au tableau
        tableau_said.append(caracteres)

    print(tableau_said)
    print(tableau_cesnac)

    nombre_differences = 0
    # Parcourir le premier tableau
    for i,valeur1 in enumerate(tableau_said):
        # Vérifier si la valeur du premier tableau n'est pas dans le deuxième tableau
        if valeur1 not in tableau_cesnac:
            # Il y a une différence
            # Ajouter la valeur à la liste des différences
            print('cette valeur n\'estpas dans cesnac',valeur1,' index : ',i,'en comparaison avec la ligne',df_facture['transmission'][i][:83])
            # Incrémenter le compteur de différences
            nombre_differences += 1
    print('nb duff = ',nombre_differences)

    with open('test_transmission.txt', 'w') as f:
        f.write(df_facture['transmission'].to_string())
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    path = os.getcwd()
    print("Le répertoire courant est : " + path)
    # récupérer le nom du répertoire courant
    repn = os.path.basename(path)
    print("Le nom du répertoire est : " + repn)
    
    uploaded_file_url = str(path)+'/nm'+str(timestamp)

    with open(uploaded_file_url, 'w') as f:
        for index, row in df_facture.iterrows():
            f.write(f"{row.transmission}\n")
    # fs = FileSystemStorage()
    # filename = fs.save(uploaded_file, uploaded_file)
    
    context = {'file':uploaded_file_url}
    print("++++++++++++++")
    for index, row in df_facture.iterrows():
        redevance = Redevance(
        flpl_call_sign=row["flpl_call_sign"],  # Assuming "call_sign" in test table
        flpl_depr_airp = row["flpl_depr_airp"],
        flpl_arrv_airp =row["flpl_arrv_airp"],
        airc_type = row["airc_type"],
        aobt=row["aobt"],  # Assuming "aircraft_takeoff_time" in test table
        eobt = row["eobt"],                            
        file_date = row["file_date"], 
        flight_state = row["flight_state"],
        flight_type = row["flight_type"],
        ifps_registration_mark = row["ifps_registration_mark"],
        initial_flight_rule = row["initial_flight_rule"],               
        nm_ifps_id = row["nm_ifps_id"],
        nm_tactical_id = row["nm_tactical_id"],  
        )
        redevance.save()

    return uploaded_file_url
    return HttpResponse(f"The thing is called {uploaded_file_url}")
    #return render(request, "webapp/traitement_fin.html",{'file':uploaded_file_url})


def download(request):
    # Define the base directory where the files are located
    base_dir = '/home/dev-data/testpdf/exo/crm/'
        
    numero_vol = 1

    print("Lancement de la lecture du fichier xslx:")

    df = pd.read_excel('/home/dev-data/testpdf/exo/crm/exportallft2122mai2023.xlsx')

    df.info()

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    df['initial_flight_rule'].value_counts()

    df[df['flpl_call_sign'] == 'FGOLS']



    df.head()

    test = 20230522000000

    df[df['file_date']==test]

    


    # Appeler la fonction
    nb_lignes,df_facture = compter_vol(df.copy(),int(20230521000000))

    # Afficher le résultat
    print(f"Nombre de vols répondant aux conditions: {nb_lignes}")

    def filtrer_vols(dataframe):
        print('debutfilteretvol')
    
        # Définir les mots à rechercher dans la colonne FTFM_FIELD15
        mots_recherches = ['OTARO', 'DOLIS', 'KAMER', 'REQIN', 'SALMA', 'CIRTA', 'MOUET']

        # Filtrer les vols répondant aux conditions
        df_facture = dataframe[dataframe['flpl_depr_airp'].str.startswith('LF')]

        print('apresnpremier filtre')
        # Filtrer les vols où la colonne flpl_arrv_airp commence par L ou E et que FTFM_FIELD15 contient un des mots de la liste
        df_facture = pd.concat([df_facture, dataframe[(dataframe['flpl_arrv_airp'].str.startswith('L') | dataframe['flpl_arrv_airp'].str.startswith('E')) & dataframe['ftfm_field15'].str.contains('|'.join(mots_recherches))]], ignore_index=True)

        return df_facture
    
    
    print('avantfilteretvol')

    # Appeler la fonction
    df_facture = filtrer_vols(df.copy())

    # Afficher le nombre de vols sélectionnés
    print(f"Nombre de vols sélectionnés: {df_facture.shape[0]}")

    def filtrer_vols(dataframe,filedate):

        mots_recherches = ["OTARO", "DOLIS", "KAMER", "REQIN", "SALMA", "CIRTA", "MOUET"," CSO "," ANB "," BJA "," ZEM "]
        dataframe = dataframe[dataframe['file_date']==filedate]

        return dataframe.loc[(dataframe['flpl_depr_airp'].str.startswith('LF')) |
                        ((dataframe['flpl_arrv_airp'].str.startswith('L') |
                        dataframe['flpl_arrv_airp'].str.startswith('E')) &
                        (dataframe['ftfm_field15'].str.contains('|'.join(mots_recherches)) |
                            dataframe['ctfm_field15'].str.contains('|'.join(mots_recherches))))]


    # Appeler la fonction
    df_facture = filtrer_vols(df.copy(),20230522000000)

    # Afficher le nombre de vols sélectionnés
    print(f"Nombre de vols sélectionnés: {df_facture.shape[0]}")

    df_facture = df_facture.sort_values(by='flpl_call_sign', ascending=True)

    df_facture = df_facture.reset_index()

    df_facture.head(10)

    df.info()

    df_facture['eobt'] = df_facture['eobt'].apply(str)
    df_facture['aobt'] = df_facture['aobt'].apply(str)

    df_facture = df_facture.fillna(' ')

    def generate_transmission(df):

        # Initialiser le compteur de position
        num = 1

        # Créer une nouvelle colonne vide
        df['transmission'] = ''

        for index, row in df.iterrows():
            # Générer la partie numérique de la transmission
            num_str = f"{num:04d}"
            # Concaténer les autres éléments de la transmission
            transmission = num_str
            transmission += "F"
            transmission += row['aobt'][8:12]
            transmission += row['flpl_depr_airp']
            transmission += row['flpl_arrv_airp']
            transmission += row['flpl_call_sign'].strip().ljust(9)
            transmission += 'Z'
            transmission += row['airc_type'].strip().ljust(7)
            transmission += 'Z  '
            transmission += str(row['ifps_registration_mark']).strip().ljust(9)
            transmission +=  f"{' ' * 21}"
            transmission += row['eobt'][7:9]
            transmission += row['eobt'][5:7] + row['eobt'][:5] + str(row['nm_ifps_id']).strip().ljust(10) + f"{' ' * 39}" + '1' + str(row['airc_modes_address']).strip().ljust(6)

            # Incrémenter le compteur de position
            num += 1

            # Affecter la valeur à la cellule courante
            df.loc[index, 'transmission'] = transmission

        return df

    # Appeler la fonction
    statut = 'F'
    df_facture = generate_transmission(df_facture.copy())

    # Afficher les premières lignes du DataFrame
    print(df_facture.head())

    df_facture['transmission'][8]

    df_facture.shape[0]

    df.head()

    df_facture[df_facture['flpl_call_sign'] == 'AFR11PM']

    df_facture[df_facture['airc_type'] == 'TBM9']

    print(df_facture['transmission'][2169])


    # Ouvrir le fichier en mode lecture
    fichier = open("/home/dev-data/testpdf/exo/crm/M-LF-20230601-090935-001-CESNAC.txt", "r")
    # Lire toutes les lignes du fichier
    lignes = fichier.readlines()
    # Fermer le fichier
    fichier.close()
    # Créer un tableau vide
    tableau_cesnac = []
    tableau_said = []

    # Parcourir la liste des lignes
    for ligne in lignes:
        # Extraire les 26 premiers caractères de la ligne
        caracteres = ligne[9:26]
        # Ajouter les caractères au tableau
        tableau_cesnac.append(caracteres)

    for ligne in df_facture['transmission']:
        # Extraire les 26 premiers caractères de la ligne
        caracteres = ligne[9:26]
        # Ajouter les caractères au tableau
        tableau_said.append(caracteres)

    print(tableau_said)

    print(tableau_cesnac)

    if tableau_cesnac[1] == tableau_said[0]:
        print('egalité')
    else:
        print(tableau_cesnac[1],'!=',tableau_said[0])

    len(tableau_cesnac[1])

    len(tableau_said[0])

    df_facture[df_facture['flpl_call_sign'] == 'DAH1162']

    df[df['flpl_call_sign'] == 'AFR87LH']

    df_facture[df_facture['flpl_call_sign'] == 'AFR98ML']

    df_facture[(df_facture['flpl_depr_airp'] == 'LFBO') & (df_facture['flpl_arrv_airp'] == 'LFBO')]

    df[(df['flpl_depr_airp'] == 'LFBO') & (df['flpl_arrv_airp'] == 'LFBO')]

    df_facture[df_facture['airc_type'] == 'TIGR']

    df[df['airc_type'] == 'TIGR']

    nombre_differences = 0
    # Parcourir le premier tableau
    for i,valeur1 in enumerate(tableau_cesnac):
        # Vérifier si la valeur du premier tableau n'est pas dans le deuxième tableau
        nb = nombre_differences
        if valeur1 not in tableau_said:
            # Il y a une différence
            # Ajouter la valeur à la liste des différences
            print('cette valeur n\'estpas dans said',valeur1,' index : ',i, ' total : ',lignes[i])

            # Incrémenter le compteur de différences
            nombre_differences += 1
        #if nb < nombre_differences:
        #  print(lignes[i])
    print('nb duff = ',nombre_differences)



    # Ouvrir le fichier en mode lecture
    fichier = open("/home/dev-data/testpdf/exo/crm/M-LF-20230601-090935-001-CESNAC.txt", "r")
    # Lire toutes les lignes du fichier
    lignes = fichier.readlines()
    # Fermer le fichier
    fichier.close()
    # Créer un tableau vide
    tableau_cesnac = []
    tableau_said = []

    # Parcourir la liste des lignes
    for ligne in lignes:
        # Extraire les 26 premiers caractères de la ligne
        caracteres = ligne[9:26]
        # Ajouter les caractères au tableau
        tableau_cesnac.append(caracteres)

    for ligne in df_facture['transmission']:
        # Extraire les 26 premiers caractères de la ligne
        caracteres = ligne[9:26]
        # Ajouter les caractères au tableau
        tableau_said.append(caracteres)

    print(tableau_said)
    print(tableau_cesnac)

    nombre_differences = 0
    # Parcourir le premier tableau
    for i,valeur1 in enumerate(tableau_said):
        # Vérifier si la valeur du premier tableau n'est pas dans le deuxième tableau
        if valeur1 not in tableau_cesnac:
            # Il y a une différence
            # Ajouter la valeur à la liste des différences
            print('cette valeur n\'estpas dans cesnac',valeur1,' index : ',i,'en comparaison avec la ligne',df_facture['transmission'][i][:83])
            # Incrémenter le compteur de différences
            nombre_differences += 1
    print('nb duff = ',nombre_differences)

    with open('test_transmission.txt', 'w') as f:
        f.write(df_facture['transmission'].to_string())

    with open('/home/dev-data/testpdf/exo/crm/fichier-transmission2.txt', 'w') as f:
        for index, row in df_facture.iterrows():
            f.write(f"{row.transmission}\n")
    
    context = {'filedownload':'fichier-transmission2.txt'}
    
    return render(request, "webapp/download.html",context=context)

def creer_fichier(request):
    fichier_id = uuid4()
    if request.method == 'POST':
        form = FichierForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = form.save()
            return redirect('telecharger_fichier', fichier_id=fichier.id)
    else:
        form = FichierForm()
    return render(request, 'creer_fichier.html', {'form': form})

def telecharger_fichier(request, fichier_id):
    fichier = Fichier.objects.get(pk=fichier_id)
    url = f'/telecharger_fichier_direct/{fichier_id}/'
    return HttpResponseRedirect(url)

def telecharger_fichier_direct(request, fichier_id):
    fichier = Fichier.objects.get(pk=fichier_id)
    response = HttpResponse(fichier.contenu, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{fichier.nom}_{fichier.temps}.txt"'
    return response

def download_file(request):
    # 1. Define the file path to download:
    file_path = os.path.join(settings.MEDIA_ROOT, '/home/dev-data/testpdf/exo/crm/fichier-transmission2.txt')  # Replace with your actual file path
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Format: YYYY-MM-DD_HH-MM-SS

    # 2. Check if the file exists:
    if not os.path.exists(file_path):
        return HttpResponseNotFound('The requested file does not exist.')

    # 3. Open the file in binary mode:
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # 4. Create an HTTP response object:
    response = HttpResponse(file_content, content_type='application/octet-stream')

    # 5. Set the content disposition header with the filename:
    response['Content-Disposition'] = f'attachment; filename="Fichier_transmission1_{timestamp}.txt"'

    return response

def download_file2(request):
     # 1. Define the file path to download:
     file_path = os.path.join(settings.MEDIA_ROOT, '/home/dev-data/testpdf/exo/crm/nm2024-02-26_15-28-39')
    
     timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Format: YYYY-MM-DD_HH-MM-SS

     # 2. Check if the file exists:
     if not os.path.exists(file_path):
         return HttpResponseNotFound('The requested file does not exist.')

     # 3. Open the file in binary mode:
     with open(file_path, 'rb') as f:
         file_content = f.read()

     # 4. Create an HTTP response object:
     response = HttpResponse(file_content, content_type='application/octet-stream')

     # 5. Set the content disposition header with the filename:
     response['Content-Disposition'] = f'attachment; filename="fichier_trasmission2_{timestamp}.txt"'

     return response

def traitement_fin(request, file):
     # 1. Define the file path to download:
     print(file)
     print("__________________")
     

    
     return render(request, 'webapp/traitement_fin.html', file)

def table(request):

    return render(request, 'webapp/your_template.html')

def accordion(request):
    my_records = Redevance.objects.all()
    
    context = {'records': my_records}

    return render(request, 'webapp/accordion.html', context=context)

def search_records(request):
  if request.method == 'GET':
    search_query = request.GET.get('search_query')
    filtered_records = Redevance.objects.filter(  # Filter logic based on search fields
        Q(flpl_call_sign__icontains=search_query) |
        Q(flpl_depr_airp__icontains=search_query) |
        Q(flpl_arrv_airp__icontains=search_query) |
        Q(airc_type__icontains=search_query) |
        Q(aobt__icontains=search_query)
    )
    return render(request, 'accordion.html', {'filtered_records': filtered_records})
  ...




def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("my-login")

