
numero_vol = 1

import pandas as pd

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

def compter_vol(dataframe,filedate):
  """
  Compte le nombre de lignes où la colonne `FLPL_DEPR_AIRP` commence par `LF` ou que la colonne `FLPL_ARRV_AIRP` commence par `L` ou `E` et que la colonne `FTFM_FIELD15` contient un des mots suivants : `OTARO`, `DOLIS`, `KAMER`, `REQIN`, `SALMA`, `CIRTA`, `MOUET`.

  Args:
    dataframe: Le DataFrame contenant les données de vol.

  Returns:
    Le nombre de lignes répondant aux conditions.
  """

  # Définir les mots à rechercher dans la colonne FTFM_FIELD15
  mots_recherches = ['OTARO', 'DOLIS', 'KAMER', 'REQIN', 'SALMA', 'CIRTA', 'MOUET']
  df_facture = pd.DataFrame()
  # Compter le nombre de lignes répondant aux conditions
  nb_lignes = 0
  dataframe = dataframe[dataframe['file_date']==filedate]
  for index, row in dataframe.iterrows():
    if row['flpl_depr_airp'].startswith('LF'):
      nb_lignes += 1
      df_facture = pd.concat([df_facture, row])
    elif row['flpl_arrv_airp'].startswith('L') or row['flpl_arrv_airp'].startswith('E'):
      if any(mot in row['ftfm_field15'] for mot in mots_recherches) or any(mot in row['ctfm_field15'] for mot in mots_recherches):
        nb_lignes += 1
        df_facture = pd.concat([df_facture, row])

  return nb_lignes,df_facture

# Appeler la fonction
nb_lignes,df_facture = compter_vol(df.copy(),int(20230521000000))

# Afficher le résultat
print(f"Nombre de vols répondant aux conditions: {nb_lignes}")

df_facture.head()

def filtrer_vols(dataframe):
  """
  Sélectionne les lignes où la colonne `FLPL_DEPR_AIRP` commence par `LF` ou que la colonne `FLPL_ARRV_AIRP` commence par `L` ou `E` et que la colonne `FTFM_FIELD15` contient un des mots suivants : `OTARO`, `DOLIS`, `KAMER`, `REQIN`, `SALMA`, `CIRTA`, `MOUET`.

  Args:
    dataframe: Le DataFrame contenant les données de vol.

  Returns:
    Un DataFrame contenant les vols répondant aux conditions.
  """

  # Définir les mots à rechercher dans la colonne FTFM_FIELD15
  mots_recherches = ['OTARO', 'DOLIS', 'KAMER', 'REQIN', 'SALMA', 'CIRTA', 'MOUET']

  # Filtrer les vols répondant aux conditions
  df_facture = dataframe[dataframe['flpl_depr_airp'].str.startswith('LF')]

  # Filtrer les vols où la colonne flpl_arrv_airp commence par L ou E et que FTFM_FIELD15 contient un des mots de la liste
  df_facture = pd.concat([df_facture, dataframe[(dataframe['flpl_arrv_airp'].str.startswith('L') | dataframe['flpl_arrv_airp'].str.startswith('E')) & dataframe['ftfm_field15'].str.contains('|'.join(mots_recherches))]], ignore_index=True)

  return df_facture

# Appeler la fonction
df_facture = filtrer_vols(df.copy())

# Afficher le nombre de vols sélectionnés
print(f"Nombre de vols sélectionnés: {df_facture.shape[0]}")

def filtrer_vols(dataframe,filedate):
  """
  Sélectionne les lignes où la colonne `FLPL_DEPR_AIRP` commence par `LF` ou que la colonne `FLPL_ARRV_AIRP` commence par `L` ou `E` et que la colonne `FTFM_FIELD15` ou `CTFM_FIELD15` contient un des mots de la liste.

  Args:
    dataframe: Le DataFrame contenant les données de vol.

  Returns:
    Un DataFrame contenant les vols répondant aux conditions.
  """

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
  """
  Crée une nouvelle colonne "transmission" dans le DataFrame df avec la formule fournie.

  Args:
    df: Le DataFrame contenant les données de vol.

  Returns:
    Le DataFrame avec la nouvelle colonne "transmission".
  """

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