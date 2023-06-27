def setup():
    # Import libraries/modules
    import pandas as pd
    import sqlalchemy
    import sql_functions as sf

    # Define global variables
    sql_config = sf.get_sql_config() # Function loads credentials from a .env file and returns a dictionary with credentials
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database', # Creates a connection object called engine
                                    connect_args=sql_config)
    schema = 'capstone_kueblbeck' # Schema in our Postgresql database

    # Other settings
    pd.options.display.max_columns = 40
    pd.options.display.float_format = "{:,.2f}".format
    
    #Loading Dataframes
    sql_query = f'select * from {schema}.lagerbestand'
    df_lagerbestand = sf.get_dataframe(sql_query)

    sql_query = f'select * from {schema}.lieferanten'
    df_lieferanten = sf.get_dataframe(sql_query)

    sql_query = f'select * from {schema}.verkäufe'
    df_verkaeufe = sf.get_dataframe(sql_query)

    # Adjust column names - df_lagerbestand
    df_lagerbestand.columns = df_lagerbestand.columns.str.lower()
    df_lagerbestand.columns = [col.replace(" ", "_") for col in df_lagerbestand.columns.tolist()]
    df_lagerbestand.columns = [col.replace(".", "") for col in df_lagerbestand.columns.tolist()]

    # Change names of selected columns - df_lagerbestand
    new_columns = {'beschr':'beschreibung',
               'bkz':'bestellkennzeichen',
               'vpe':'verp_einheit',
               'stgr':'stat_gruppe',
               'basispreis':'basispreis_lager'
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

    # Adjust column names - df_lieferanten
    df_lieferanten.columns = df_lieferanten.columns.str.lower()
    df_lieferanten.columns = [col.replace(" ", "_") for col in df_lieferanten.columns.tolist()]
    df_lieferanten.columns = [col.replace(".", "") for col in df_lieferanten.columns.tolist()]

    df_lieferanten = df_lieferanten.rename(columns={'beschreibung':'lieferant'})

    # Adjust column names - df_verkaeufe
    df_verkaeufe.columns = df_verkaeufe.columns.str.lower()
    df_verkaeufe.columns = [col.replace(" ", "_") for col in df_verkaeufe.columns.tolist()]
    df_verkaeufe.columns = [col.replace(".", "") for col in df_verkaeufe.columns.tolist()]

    # Change names of selected columns
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

    # Merge df_verkaeufe on df_lagerbestand to create df_master and drop duplicates
    # Outer merge due to having articles sold in 2022 that might be out of stock at the time of our inventory data (2023-06-03)
    df_master = df_lagerbestand.merge(df_verkaeufe, how='outer', on=['lfnr', 'artnr', 'index', 'beschreibung']).fillna(0)
    df_master = df_master.drop_duplicates(['lfnr', 'artnr', 'index', 'beschreibung'])

    # Merging df_lieferanten on df_master
    df_master = df_master.merge(df_lieferanten, how='left', on='lfnr')

    # Adjusting column positions

    new_column_order = ['lfnr','lieferant', 'artnr', 'beschreibung', 'index', 'bestellkennzeichen',
         'verp_einheit', 'stat_gruppe', 'ltz_vk_ges', 'basispreis_lager', 'basispr_summe',
         'basispreis_vk', 'gesamt_lager', 'wen_lager', 'ltz_vk_wen', 'rgb_lager',
         'ltz_vk_rgb', 'amb_lager', 'ltz_vk_amb', 'cha_lager', 'ltz_vk_cha',
         'str_lager', 'ltz_vk_str', 'pas_lager', 'ltz_vk_pas', 'lan_lager',
         'ltz_vk_lan', 'müh_lager', 'ltz_vk_müh', 'ros_lager', 'ltz_vk_ros',
         'gesamt_vk', 'wen_vk', 'rgb_vk', 'str_vk', 'pas_vk',
         'amb_vk', 'cha_vk', 'lan_vk', 'müh_vk', 'ros_vk']

    df_master = df_master.reindex(columns = new_column_order)

    # Drop columns that are not needed
    df_master.drop(columns=['bestellkennzeichen', 'verp_einheit', 'stat_gruppe'], inplace=True)
    
    
    return df_master