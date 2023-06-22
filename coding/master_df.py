def setup():

    import pandas as pd
    import sqlalchemy
    import sql_functions as sf

    sql_config = sf.get_sql_config() # Function loads credentials from a .env file and returns a dictionary with credentials
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database', # Creates a connection object called engine
                                    connect_args=sql_config)
    schema = 'capstone_kueblbeck' # Schema in our Postgresql database

    pd.options.display.max_columns = 30
    pd.options.display.float_format = "{:,.2f}".format

    sql_query = f'select * from {schema}.lagerbestand'
    df_lagerbestand = sf.get_dataframe(sql_query)


    sql_query = f'select * from {schema}.lieferanten'
    df_lieferanten = sf.get_dataframe(sql_query)

    sql_query = f'select * from {schema}.verkäufe'
    df_verkaeufe = sf.get_dataframe(sql_query)

    df_lagerbestand.columns = df_lagerbestand.columns.str.lower()
    df_lagerbestand.columns = [col.replace(" ", "_") for col in df_lagerbestand.columns.tolist()]
    df_lagerbestand.columns = [col.replace(".", "") for col in df_lagerbestand.columns.tolist()]

    new_columns = {'beschr':'beschreibung',
               'bkz':'bestellkennzeichen',
               'vpe':'verp_einheit',
               'stgr':'stat_gruppe',
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

    df_lagerbestand['index'] = df_lagerbestand['index'].astype(int)

    df_lieferanten.columns = df_lieferanten.columns.str.lower()
    df_lieferanten.columns = [col.replace(" ", "_") for col in df_lieferanten.columns.tolist()]
    df_lieferanten.columns = [col.replace(".", "") for col in df_lieferanten.columns.tolist()]

    df_lieferanten = df_lieferanten.rename(columns={'beschreibung':'lieferant'})

    df_verkaeufe.columns = df_verkaeufe.columns.str.lower()
    df_verkaeufe.columns = [col.replace(" ", "_") for col in df_verkaeufe.columns.tolist()]
    df_verkaeufe.columns = [col.replace(".", "") for col in df_verkaeufe.columns.tolist()]

    new_columns = {'lfr':'lfnr',
               'ind': 'index',
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

    df_verkaeufe['index'] = df_verkaeufe['index'].astype(int)

    df_master = df_lagerbestand.merge(df_lieferanten, how='left', on='lfnr')

    df_master = df_master.merge(df_verkaeufe, how='left', on=['lfnr', 'artnr', 'index', 'beschreibung'])

    df_master.columns = ['lfnr','lieferant', 'artnr', 'index', 'beschreibung', 'bestellkennzeichen',
       'verp_einheit', 'stat_gruppe', 'ltz_vk_ges', 'basispreis',
       'basispr_summe', 'gesamt_lager', 'wen_lager', 'ltz_vk_wen', 'rgb_lager',
       'ltz_vk_rgb', 'amb_lager', 'ltz_vk_amb', 'cha_lager', 'ltz_vk_cha',
       'str_lager', 'ltz_vk_str', 'pas_lager', 'ltz_vk_pas', 'lan_lager',
       'ltz_vk_lan', 'müh_lager', 'ltz_vk_müh', 'ros_lager', 'ltz_vk_ros',
        'gesamt_vk', 'wen_vk', 'rgb_vk', 'str_vk', 'pas_vk',
       'amb_vk', 'cha_vk', 'lan_vk', 'müh_vk', 'ros_vk']
    
    return df_master