import pandas as pd
def compter_vol(dataframe,filedate):
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

        # Return the value of nb_lignes
        return nb_lignes, df_facture