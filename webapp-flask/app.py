from flask import Flask, render_template, request, send_file, redirect, url_for
from master_df_app import setup
from master_df_app import visuals
import sys
import os
import pandas as pd
#import concurrent.futures
import datetime
# import openpyxl
import math
import webview

app = Flask(__name__)
window = webview.create_window('Küblbeck Umlagerungen', app, fullscreen=False, confirm_close=True) # create webview by opening window

# BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
UPLOADS_DIR = os.path.join(BASE_DIR, 'temp/uploads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'temp/output')
#INPUT_DIR = os.path.join(BASE_DIR, 'temp/inputs')

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

ALLOWED_EXTENSIONS = {'csv', 'txt', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def save_df_master():
#     global output_pfad
#     datum = datetime.date.today().strftime('%Y-%m-%d')
#     output_pfad = f'output/Umlagerungen {datum}.xlsx'
#     df_master.to_excel(output_pfad, index=False)

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

                global df_master
                df_master = setup(lagerbestand_pfad, verkaeufe_pfad, lieferanten_pfad)

                return redirect(url_for('output'))
            else:
                return 'Ungültiges Dateiformat. Erlaubte Formate sind .csv, .txt, .xls und .xlsx.'

    return render_template('home.html')

@app.route("/output")
def output():
    stock_quality, sales_quality = visuals()
    return render_template('output.html', stock_quality=stock_quality, sales_quality=sales_quality)

@app.route("/download")
def download():
    datum = datetime.date.today().strftime('%Y-%m-%d')
    output_pfad = os.path.join(OUTPUT_DIR, f'Umlagerungen {datum}.xlsx')

    # df_master.to_excel(output_pfad, index=False, sheet_name='Umlagerungen')
    
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.submit(save_df_master)

    # with pd.ExcelWriter(output_pfad, engine='openpyxl') as writer:
    #     writer.book = openpyxl.Workbook()
    #     df_master.to_excel(writer, index=False)
    #     writer.save

    # df_master.to_excel(output_pfad, index=False, engine='xlsxwriter')

    chunk_size = 50000
    temp_dir = os.path.join(OUTPUT_DIR, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    save_df_chunks(df_master, chunk_size, temp_dir)

    merge_csv_files(temp_dir, output_pfad)

    return send_file(output_pfad, as_attachment=True)

if __name__ == '__main__':
    webview.start(debug=True) # run webview in window mode
    #app.run(host="0.0.0.0", debug=True)