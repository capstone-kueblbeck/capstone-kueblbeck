# Importing modules/libraries globally:
import pandas as pd
import os
import sys
import numpy as np
import re
import math

def read_dataframe(input_pfad):
    if input_pfad.endswith('.csv') or input_pfad.endswith('.txt'):
        with open(input_pfad, 'r') as file:
            first_line = file.readline()
            if ';' in first_line:
                delimiter = ';'
            else:
                delimiter = ','

        df_input = pd.read_csv(input_pfad, dtype=str, delimiter=delimiter)

    elif input_pfad.endswith('.xls') or input_pfad.endswith('.xlsx'):
        df_input = pd.read_excel(input_pfad, dtype=str)

    else:
        raise ValueError("Ungültiger Dateityp. Unterstütze Formate sind .csv, .txt, .xls und .xlsx.")
    
    df_input = df_input.drop(df_input.index[0])
    return df_input
    
def setup(lagerbestand_pfad, verkaeufe_pfad, lieferanten_pfad):
    # General settings
    global df_master

    # Loading Dataframes via function
    df_lieferanten = read_dataframe(lieferanten_pfad)
    df_lagerbestand = read_dataframe(lagerbestand_pfad)
    df_verkaeufe = read_dataframe(verkaeufe_pfad)

    #Adjust columns - df_lieferanten
    df_lieferanten.columns = df_lieferanten.columns.str.lower()
    df_lieferanten.columns = [col.replace(" ", "_") for col in df_lieferanten.columns.tolist()]
    df_lieferanten.columns = [col.replace(".", "") for col in df_lieferanten.columns.tolist()]
    df_lieferanten = df_lieferanten.rename(columns={'beschreibung':'lieferant'})
    
    # Adjust datatypes where necessary - df_lagerbestand
    # date_columns = ["Ltz. VK ges.", "Ltz. VK WEN", "Ltz. VK RGB", "Ltz. VK AMB", "Ltz. VK CHA", "Ltz. VK STR", "Ltz. VK PAS", "Ltz. VK LAN", "Ltz. VK MÜH", "Ltz. VK ROS"]
    # for column in date_columns:
    #     df_lagerbestand[column] = pd.to_datetime(df_lagerbestand[column], format='%d.%m.%Y', errors='coerce')
    
    numeric_columns = ['Gesamt', 'WEN', 'RGB', 'AMB', 'CHA', 'STR', 'PAS', 'LAN', 'MÜH', 'ROS']
    for column in numeric_columns:
        df_lagerbestand[column] = pd.to_numeric(df_lagerbestand[column].str.replace('.', '').str.replace(',','.'), errors='coerce')

    numeric_columns_basis = ['Basispreis', 'Basispr. Summe']
    for column in numeric_columns_basis:
        df_lagerbestand[column] = pd.to_numeric(df_lagerbestand[column].str.replace('.', '').str.replace(',','.'))

    df_lagerbestand['Index'] = df_lagerbestand['Index'].astype(int).astype(str)
    df_lagerbestand['Lfnr'] = df_lagerbestand['Lfnr'].astype(int).astype(str)

    # Adjust column names - df_lagerbestand
    df_lagerbestand.columns = df_lagerbestand.columns.str.lower()
    df_lagerbestand.columns = [col.replace(" ", "_") for col in df_lagerbestand.columns.tolist()]
    df_lagerbestand.columns = [col.replace(".", "") for col in df_lagerbestand.columns.tolist()]

    # Change names of selected columns - df_lagerbestand
    new_columns = {'beschr':'beschreibung',
               'bkz':'bestellkennzeichen',
               'vpe':'verp_einheit',
               'stgr':'stat_gruppe',
               'basispreis':'basispreis_lager',
               'gesamt':'gesamt_lager',
               'wen':'wen_lager',
               'rgb':'rgb_lager',
               'str':'str_lager',
               'pas':'pas_lager',
               'amb':'amb_lager',
               'cha':'cha_lager',
               'lan':'lan_lager',
               'müh':'müh_lager',
               'ros':'ros_lager'}

    df_lagerbestand = df_lagerbestand.rename(columns=new_columns)

    # Adjust datatypes where necessary - df_verkaeufe
    numeric_columns = ["WAWI_Artikel.Einstandspreis (fest)","Gesamt", "WEN", "RGB", "AMB", "CHA", "STR", "PAS", "LAN", "MÜH", "ROS"]
    for column in numeric_columns:
        df_verkaeufe[column] = pd.to_numeric(df_verkaeufe[column].str.replace('.', '').str.replace(',', '.'), errors='coerce')

    df_verkaeufe['Lfr.'] = df_verkaeufe['Lfr.'].astype(int).astype(str)

    # Adjust column names - df_verkaeufe
    df_verkaeufe.columns = df_verkaeufe.columns.str.lower()
    df_verkaeufe.columns = [col.replace(" ", "_") for col in df_verkaeufe.columns.tolist()]
    df_verkaeufe.columns = [col.replace(".", "") for col in df_verkaeufe.columns.tolist()]

    # Change names of selected columns - df_verkaeufe
    new_columns = {'lfr':'lfnr',
               'ind': 'index',
               'wawi_artikeleinstandspreis_(fest)':'basispreis_vk',
               'gesamt':'gesamt_vk',
               'wen':'wen_vk',
               'rgb':'rgb_vk',
               'str':'str_vk',
               'pas':'pas_vk',
               'amb':'amb_vk',
               'cha':'cha_vk',
               'lan':'lan_vk',
               'müh':'müh_vk',
               'ros':'ros_vk'}

    df_verkaeufe = df_verkaeufe.rename(columns=new_columns)

    # Filtering out unusable article numbers (due to formatting in source file) - df_verkaeufe
    df_verkaeufe = df_verkaeufe[~df_verkaeufe['artnr'].str.contains('E\+')]

    # Adjust column names - df_lieferanten
    df_lieferanten.columns = df_lieferanten.columns.str.lower()
    df_lieferanten.columns = [col.replace(" ", "_") for col in df_lieferanten.columns.tolist()]
    df_lieferanten.columns = [col.replace(".", "") for col in df_lieferanten.columns.tolist()]

    df_lieferanten = df_lieferanten.rename(columns={'beschreibung':'lieferant'})

    # Merge df_verkaeufe on df_lagerbestand to create df_master and drop duplicates
    # Outer merge due to having articles sold in 2022 that might be out of stock at the time of our inventory data (2023-06-03)
    df_master = df_lagerbestand.merge(df_verkaeufe, how='outer', on=['lfnr', 'artnr', 'index', 'beschreibung']).fillna(0)
    df_master = df_master.drop_duplicates(['lfnr', 'artnr', 'index', 'beschreibung'])

    # Checking maximum price from basispreis_lager and basispreis_vk and creating new column
    df_master['basispreis'] = df_master[['basispreis_lager', 'basispreis_vk']].apply(max, axis=1)

    # Calculating new inventory value with the new 'basispreis'
    df_master['basispr_summe'] = df_master['basispreis'] * df_master['gesamt_lager']

    # Merging df_lieferanten on df_master
    df_master = df_master.merge(df_lieferanten, how='left', on='lfnr')

    # Adjusting column positions
    new_column_order = [        # These columns will be left out: 'bestellkennzeichen', 'verp_einheit', 'stat_gruppe', 'basispreis_lager', 'basispreis_vk'
        'lfnr','lieferant', 'artnr', 'beschreibung', 'index',
        'basispreis', 'basispr_summe', 'gesamt_lager', 'ltz_vk_ges',
        'wen_lager', 'ltz_vk_wen', 'rgb_lager', 'ltz_vk_rgb', 'amb_lager', 'ltz_vk_amb',
        'cha_lager', 'ltz_vk_cha', 'str_lager', 'ltz_vk_str', 'pas_lager', 'ltz_vk_pas',
        'lan_lager', 'ltz_vk_lan', 'müh_lager', 'ltz_vk_müh', 'ros_lager', 'ltz_vk_ros',
        'gesamt_vk', 'wen_vk', 'rgb_vk', 'str_vk', 'pas_vk',
        'amb_vk', 'cha_vk', 'lan_vk', 'müh_vk', 'ros_vk'
        ]
    df_master = df_master.reindex(columns = new_column_order)
    
    return df_master

def visuals():
    # Import specific libraries/modules
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    from io import BytesIO
    import base64

    # Visualization quality stock
    global locations
    locations = {'gesamt': 'Gesamt', 
             'wen': 'Weiden', 
             'rgb': 'Regensburg', 
             'amb': 'Amberg', 
             'cha': 'Cham', 
             'str': 'Straubing', 
             'pas': 'Passau', 
             'lan': 'Landshut', 
             'müh': 'Mühldorf', 
             'ros': 'Rosenheim'}

    PE_categories = ['In stock, 4+ sales', 'In stock, 3 sales', 'In stock, 2 sales', 'In stock, 1 sale', 'In stock, 0 sales']
    display_order_quality = PE_categories

    for x in locations.keys():
        PE_condition = [
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] > 3),
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] == 3),
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] == 2),
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] == 1),
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] == 0)   
        ]

        df_master[x+'_quality'] = np.select(PE_condition, PE_categories)

    fig1, axes = plt.subplots(4, 3, figsize=(25,20))
    fig1.suptitle('Warehouse management quality stock', fontweight='bold', fontsize=30)
    fig1.tight_layout(pad=5.0)

    for i in range (13):
        y = 0
        z = 1

        for key, value in locations.items():

                
            location = df_master.query(key + '_quality != "0"')

            sub = sns.countplot(ax=axes[y, z], x=key + '_quality', data=location, order=display_order_quality)
            axes[y, z].set_title("Qualität " + value, fontsize=15.0)
            axes[y, z].set_xlabel('Qualität', fontsize=10.0)
            axes[y, z].set_ylabel('Anzahl', fontsize=10.0)
            # Erhalten Sie die Gesamtzahl der Qualitätsspalte
            total = location[key + '_quality'].count()

            freq_series = location[key + '_quality'].value_counts()
            freq_series = freq_series.reindex(display_order_quality)

            rects = sub.patches
            labels = [f'{(x/total)*100:.1f}%' for x in freq_series]
            for rect, label in zip(rects, labels):
                height = rect.get_height()
                axes[y, z].text(rect.get_x() + rect.get_width() / 2, height + 5, label,
                        ha='center', va='bottom')
                
            z += 1  
            if y == 0 and z == 2:
                y = 1
                z = 0
                
            elif z >= 3:
                y += 1
                z = 0

    image_bytes1 = BytesIO()
    fig1.savefig(image_bytes1, format='png')
    image_bytes1.seek(0)
    stock_quality = base64.b64encode(image_bytes1.getvalue()).decode('utf-8')


    # Visualization quality sales
    PE_categories = ['4+ sales, in stock', '4+ sales, no stock', '1-3 sales, in stock', '1-3 sales, no stock', '0 sales, in stock']
    display_order_quality = PE_categories

    for x in locations.keys():
        PE_condition = [
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] > 3),
            (df_master[x+'_lager'] == 0) & (df_master[x+'_vk'] > 3),
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] < 3) & (df_master[x+'_vk'] > 0),
            (df_master[x+'_lager'] == 0) & (df_master[x+'_vk'] < 3) & (df_master[x+'_vk'] > 0),
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] == 0)
        ]

        df_master[x+'_quality'] = np.select(PE_condition, PE_categories)

    fig2, axes = plt.subplots(4, 3, figsize=(25,20))
    fig2.suptitle('Warehouse management quality sales', fontweight='bold', fontsize=30)
    fig2.tight_layout(pad=5.0)

    for i in range (13):
        y = 0
        z = 1

        for key, value in locations.items():

                
            location = df_master.query(key + '_quality != "0"').reset_index()

            sub = sns.countplot(ax=axes[y, z], x=key + '_quality', data=location, order=display_order_quality)
            axes[y, z].set_title("Qualität " + value, fontsize=15.0)
            axes[y, z].set_xlabel('Qualität', fontsize=10.0)
            axes[y, z].set_ylabel('Anzahl', fontsize=10.0)
            # Erhalten Sie die Gesamtzahl der Qualitätsspalte
            total = location[key + '_quality'].count()

            freq_series = location[key + '_quality'].value_counts()
            freq_series = freq_series.reindex(display_order_quality)

            rects = sub.patches
            labels = [f'{(x/total)*100:.1f}%' for x in freq_series]
            for rect, label in zip(rects, labels):
                height = rect.get_height()
                axes[y, z].text(rect.get_x() + rect.get_width() / 2, height + 5, label,
                        ha='center', va='bottom')
                
            z += 1  
            if y == 0 and z == 2:
                y = 1
                z = 0
                
            elif z >= 3:
                y += 1
                z = 0

    image_bytes2 = BytesIO()
    fig2.savefig(image_bytes2, format='png')
    image_bytes2.seek(0)
    sales_quality = base64.b64encode(image_bytes2.getvalue()).decode('utf-8')

    return stock_quality, sales_quality

def distribution_prep():
    df_master_quality = df_master.query('gesamt_quality != "0"')

    locations = {'wen': 'Weiden', 
             'rgb': 'Regensburg', 
             'amb': 'Amberg', 
             'cha': 'Cham', 
             'str': 'Straubing', 
             'pas': 'Passau', 
             'lan': 'Landshut', 
             'müh': 'Mühldorf', 
             'ros': 'Rosenheim'}

    PE_categories = ['4+ sales, in stock', '4+ sales, no stock', '1-3 sales, in stock', '1-3 sales, no stock', '0 sales, in stock']
    #display_order_quality = PE_categories

    for x in locations.keys():
        PE_condition = [
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] > 3),
            (df_master[x+'_lager'] == 0) & (df_master[x+'_vk'] > 3),
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] < 3) & (df_master[x+'_vk'] > 0),
            (df_master[x+'_lager'] == 0) & (df_master[x+'_vk'] < 3) & (df_master[x+'_vk'] > 0),
            (df_master[x+'_lager'] > 0) & (df_master[x+'_vk'] == 0)
        ]

        df_master[x+'_quality'] = np.select(PE_condition, PE_categories)

    for key, value in locations.items():
        df_master_quality['take_from_' + key] = df_master_quality.apply(lambda row: ', '.join([k for k, v in locations.items() if row[k + '_quality'] == '4+ sales, no stock']) if row[key + '_quality'] in ['1-3 sales, in stock', '0 sales, in stock'] else '-', axis=1)

    global df_master_quality_final
    df_master_quality_final = df_master_quality[~(df_master_quality.filter(like='take_from_').isin(['-', ''])).all(axis=1)]
    
    return df_master_quality_final

def count_list_elements(x):
    if x == ['-']:
        return 0
    else:
        return len(x)
    
def assigning(row):
    a = row['list']
    b = row['dividing']
    c = row['remainder']
    d = row['best_sales']
    result = [f"{x} ({b + c:.0f})" if x == d else f"{x} ({b:.0f})" for x in a]
    return result

def best_sale(row):
    a = row['list']
    if not a:  # Überprüfen, ob a leer ist
        return '-'
    else:
        best_sales = sorted([row[k + '_vk'] for k in a if k != '-' and k + '_vk' in row.index and row[k + '_vk'] is not None], key=lambda y: float(y) if isinstance(y, str) else y, reverse=True)
        if best_sales:
            return best_sales[0]
        else:
            return '-'
        
def calculate_stock(row):
    total_stock = 0
    pattern = r'\(\d+\)'
    for key in locations.keys():
        if isinstance(row['take_from_' + key], str) and row['take_from_' + key] != '-':
            matches = re.findall(pattern, row['take_from_' + key])
            for match in matches:
                stock = int(match[1:-1])
                total_stock += stock
    total_stock *= row['basispreis']
    return total_stock

def renaming(row, key):
    pattern = '|'.join(locations.keys())
    a = row['take_from_' + key]
    p = pattern
    res = re.sub(pattern, lambda match: locations[match.group(0)], a)
    return res

def formating(row, key):
    a = row['take_from_' + key]
    res_blank = a.replace(',', ',\n')
    #res_double = a.replace(') (', ',)""')
    return res_blank

def distribution():
    for key, value in locations.items():
        df_master_quality_final['list'] = df_master_quality_final['take_from_' + key].apply(lambda x: [i for i in x.split(', ')])
        df_master_quality_final['numbers'] = df_master_quality_final['list'].apply(count_list_elements)
        df_master_quality_final['dividing'] = (df_master_quality_final[key +'_lager']/df_master_quality_final['numbers']).apply(np.floor)
        df_master_quality_final['remainder'] = (df_master_quality_final[key + '_lager']%df_master_quality_final['numbers'])
        df_master_quality_final['best_sales'] = df_master_quality_final.apply(best_sale, axis=1)
        df_master_quality_final['locations'] = df_master_quality_final.apply(assigning, axis=1)
        df_master_quality_final['locations'] = [','.join(map(str, l)) for l in df_master_quality_final['locations']]
        df_master_quality_final['locations'] = df_master_quality_final['locations'].replace(["- (nan)", "- (inf)", "- (-inf)"], "-")
        df_master_quality_final['take_from_' + key] = df_master_quality_final['locations']
        df_master_quality_final['take_from_' + key] = df_master_quality_final.apply(renaming, axis=1, key=key)
        df_master_quality_final['take_from_' + key] = df_master_quality_final.apply(formating, axis=1, key=key)
        df_master_quality_final['stock'] = df_master_quality_final.apply(calculate_stock, axis=1)
    
    return df_master_quality_final

def keep_cols(DataFrame, keep_these):
    """Keep only the columns [keep_these] in a DataFrame, delete
    all other columns. 
    """
    drop_these = list(set(list(DataFrame)) - set(keep_these))

    return DataFrame.drop(drop_these, axis = 1)

def final_output():
    take_from = ['lieferant', 'artnr', 'beschreibung']
    for key in locations.keys():
        a = f'take_from_{key}'
        take_from.append(a)

    df_master_quality_final.sort_values(by='stock', ascending=False, inplace=True)
    df_master_quality_final.reset_index(inplace=True, drop=True)
    global df_master_quality_output
    df_master_quality_output = df_master_quality_final.pipe(keep_cols, take_from)

    return df_master_quality_output