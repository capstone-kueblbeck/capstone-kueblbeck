from flask import Flask, render_template, request, send_file, redirect, url_for
import master_df_app as mdf
import sys
import os
import pandas as pd
import datetime
import math
import webview
import numpy as np
import re
import xlsxwriter
# import threading

app = Flask(__name__)
window = webview.create_window('Küblbeck Umlagerungen', app, fullscreen=False, confirm_close=True) # create webview by opening window

# BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
UPLOADS_DIR = os.path.join(BASE_DIR, 'temp', 'uploads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'temp', 'output')

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

ALLOWED_EXTENSIONS = {'csv', 'txt', 'xls', 'xlsx'}
# processing_complete = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_df_chunks(df, chunk_size, output_dir):
    num_chunks = math.ceil(len(df) / (chunk_size))

    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunk = df[start:end]

        temp_pfad = f'{output_dir}/output_chunk_{i}.csv'
        chunk.to_csv(temp_pfad, index=False)

def merge_csv_files(input_dir, output_file):
    all_data = pd.DataFrame()

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_dir, file_name)

            df_chunk = pd.read_csv(file_path)
            all_data = all_data.append(df_chunk, ignore_index=True)

    all_data.to_excel(output_file, index=False)

    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        os.remove(file_path)

    os.rmdir(input_dir)

def process_data(lagerbestand_pfad, verkaeufe_pfad, lieferanten_pfad):
    # Create dataframe df_master
    global output_pfad, df_master, stock_quality, sales_quality
    df_master = mdf.setup(lagerbestand_pfad, verkaeufe_pfad, lieferanten_pfad)
    
    # Create visualizations
    stock_quality, sales_quality = mdf.visuals()

    # Prep for distribution method
    df_master_quality = df_master.query('gesamt_quality != "0"')
    global locations
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
    for key, value in locations.items():
        df_master_quality['take_from_' + key] = df_master_quality.apply(lambda row: ', '.join([k for k, v in locations.items() if row[k + '_quality'] == '4+ sales, no stock']) if row[key + '_quality'] in ['1-3 sales, in stock', '0 sales, in stock'] else '-', axis=1)
    df_master_quality_final = df_master_quality[~(df_master_quality.filter(like='take_from_').isin(['-', ''])).all(axis=1)]

    # Distribution algorithm
    df_master_quality_distribution = df_master_quality_final
    for key, value in locations.items():
        df_master_quality_distribution['list'] = df_master_quality_distribution['take_from_' + key].apply(lambda x: [i for i in x.split(', ')])
        df_master_quality_distribution['numbers'] = df_master_quality_distribution['list'].apply(mdf.count_list_elements)
        df_master_quality_distribution['dividing'] = (df_master_quality_distribution[key +'_lager']/df_master_quality_distribution['numbers']).apply(np.floor)
        df_master_quality_distribution['remainder'] = (df_master_quality_distribution[key + '_lager']%df_master_quality_distribution['numbers'])
        df_master_quality_distribution['best_sales'] = df_master_quality_distribution.apply(mdf.best_sale, axis=1)
        df_master_quality_distribution['locations'] = df_master_quality_distribution.apply(mdf.assigning, axis=1)
        df_master_quality_distribution['locations'] = [','.join(map(str, l)) for l in df_master_quality_distribution['locations']]
        df_master_quality_distribution['locations'] = df_master_quality_distribution['locations'].replace(["- (nan)", "- (inf)", "- (-inf)"], "-")
        df_master_quality_distribution['take_from_' + key] = df_master_quality_distribution['locations']
        df_master_quality_distribution['take_from_' + key] = df_master_quality_distribution.apply(mdf.renaming, axis=1, key=key, locations=locations)
        df_master_quality_distribution['take_from_' + key] = df_master_quality_distribution.apply(mdf.formating, axis=1, key=key)
        df_master_quality_distribution['stock'] = df_master_quality_distribution.apply(mdf.calculate_stock, axis=1, locations=locations)

    # Cleaning and sorting
    take_from = ['lfnr', 'lieferant', 'artnr', 'beschreibung', 'stock']
    for key in locations.keys():
        a = f'take_from_{key}'
        take_from.append(a)

    df_master_quality_distribution.sort_values(by='stock', ascending=False, inplace=True)
    df_master_quality_distribution.reset_index(inplace=True, drop=True)
    df_master_quality_output = df_master_quality_distribution.pipe(mdf.keep_cols, take_from)

    # Write Excel file for output
    datum = datetime.date.today().strftime('%Y-%m-%d')
    output_pfad = os.path.join(OUTPUT_DIR, f'Umlagerungen {datum}.xlsx')
    # chunk_size = 10000
    # temp_dir = os.path.join(OUTPUT_DIR, 'temp')
    # os.makedirs(temp_dir, exist_ok=True)
    # save_df_chunks(df_master_quality_output, chunk_size, temp_dir)
    # merge_csv_files(temp_dir, output_pfad)

    workbook = xlsxwriter.Workbook(output_pfad)
    worksheet = workbook.add_worksheet()
    header_format = workbook.add_format({'bold':True})
    worksheet.write_row(0, 0, df_master_quality_output.columns, header_format)
    for row_num, row_data in enumerate(df_master_quality_output.values, start=1):
        worksheet.write_row(row_num, 0, row_data)
    num_rows = len(df_master_quality_output.index)
    num_cols = len(df_master_quality_output.columns)
    worksheet.autofilter(0, 0, num_rows, num_cols - 1)
    workbook.close()


    # global processing_complete
    # processing_complete = True

    return None

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'lagerbestand' in request.files and 'verkaeufe' in request.files and 'lieferanten' in request.files:
            lagerbestand = request.files['lagerbestand']
            verkaeufe = request.files['verkaeufe']
            lieferanten = request.files['lieferanten']

            if allowed_file(lagerbestand.filename) and allowed_file(verkaeufe.filename) and allowed_file(lieferanten.filename):
                lagerbestand_pfad = os.path.join(UPLOADS_DIR, lagerbestand.filename)
                verkaeufe_pfad = os.path.join(UPLOADS_DIR, verkaeufe.filename)
                lieferanten_pfad = os.path.join(UPLOADS_DIR, lieferanten.filename)

                lagerbestand.save(lagerbestand_pfad)
                verkaeufe.save(verkaeufe_pfad)
                lieferanten.save(lieferanten_pfad)

                process_data(lagerbestand_pfad, verkaeufe_pfad, lieferanten_pfad)
                #threading.Thread(target=process_data, args=(lagerbestand_pfad, verkaeufe_pfad, lieferanten_pfad)).start
                
                return redirect(url_for('output'))
            else:
                return 'Ungültiges Dateiformat. Erlaubte Formate sind .csv, .txt, .xls und .xlsx.'

    return render_template('home.html')

@app.route("/loading")
def loading():
    if processing_complete:
        return redirect(url_for('output'))
    else:
        return render_template('loading.html')

@app.route("/output")
def output():
    return render_template('output.html', stock_quality=stock_quality, sales_quality=sales_quality)

@app.route("/download")
def download():
    return send_file(output_pfad, as_attachment=True)

if __name__ == '__main__':
    # webview.start(debug=True) # run webview in window mode
    app.run(host="0.0.0.0", debug=True)