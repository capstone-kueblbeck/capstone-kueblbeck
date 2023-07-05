def read_dataframe(input_pfad):
    import pandas as pd
    
    if input_pfad.endswith('csv') or input_pfad.endswith('txt'):
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
    # Import libraries/modules
    import pandas as pd
    import sqlalchemy
    import sql_functions as sf

    # Define global variables
    sql_config = sf.get_sql_config() # Function loads credentials from a .env file and returns a dictionary with credentials
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database', # Creates a connection object called engine
                                    connect_args=sql_config)
    schema = 'capstone_kueblbeck' # Schema in our Postgresql database
    global df_master

    # Other settings
    pd.options.display.float_format = "{:,.2f}".format

    # sql_query = f'select * from {schema}.lieferanten'
    # df_lieferanten = sf.get_dataframe(sql_query)

    # #Loading static dataframe from Inputs
    # df_lieferanten = pd.read_excel('inputs/Lieferantenübersicht.xlsx', dtype=str)
    # df_lieferanten = df_lieferanten.drop(df_lieferanten.index[0])

    # #Loading Dataframes from Uploads
    # df_lagerbestand = pd.read_csv(lagerbestand_pfad, dtype=str, delimiter=',')
    # df_lagerbestand = df_lagerbestand.drop(df_lagerbestand.index[0])
    # df_verkaeufe = pd.read_csv(verkaeufe_pfad, dtype=str, delimiter=';')
    # df_verkaeufe = df_verkaeufe.drop(df_verkaeufe.index[0])

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