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

BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
INPUT_DIR = os.path.join(BASE_DIR, 'inputs')

app = Flask(__name__, static_folder = OUTPUT_DIR)

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
        if 'lagerbestand' in request.files and 'verkaeufe' in request.files:
            lagerbestand = request.files['lagerbestand']
            verkaeufe = request.files['verkaeufe']

            if allowed_file(lagerbestand.filename) and allowed_file(verkaeufe.filename):
                lagerbestand_pfad = os.path.join(UPLOADS_DIR, 'lagerbestand.csv')
                verkaeufe_pfad = os.path.join(UPLOADS_DIR, 'verkaeufe.csv')
                lieferanten_pfad = os.path.join(INPUT_DIR, 'Lieferantenübersicht.xlsx')

                lagerbestand.save(lagerbestand_pfad)
                verkaeufe.save(verkaeufe_pfad)

                global df_master
                df_master = setup(lagerbestand_pfad, verkaeufe_pfad, lieferanten_pfad)

                return redirect(url_for('output'))
            else:
                return 'Ungültiges Dateiformat. Erlaubte Formate sind .csv, .txt, .xls und .xlsx.'

    return render_template('home.html')

# How-to Daten an Flask senden??
# Wie werden DAten empfangen in Flask?
# app output verändern, so dass dort die DAten an output weitergegeben werden (Jinja2 Templates)

@app.route("/output")
def output():
    # get input from index.html (csv)
    # process csv file über calculate_data(csv)
    # data = calculate_data(csv)
    # template = create_html_template_with_data
    # return render_template(template)
    vis_paths = visuals()
    return render_template('output.html', vis_paths=vis_paths)

@app.route("/download")
def download():
    #global df_master
    datum = datetime.date.today().strftime('%Y-%m-%d')
    output_pfad = f'output/Umlagerungen {datum}.xlsx'

    # df_master.to_excel(output_pfad, index=False, sheet_name='Umlagerungen')
    
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.submit(save_df_master)

    # with pd.ExcelWriter(output_pfad, engine='openpyxl') as writer:
    #     writer.book = openpyxl.Workbook()
    #     df_master.to_excel(writer, index=False)
    #     writer.save

    # df_master.to_excel(output_pfad, index=False, engine='xlsxwriter')

    chunk_size = 50000
    output_dir = 'output/temp'
    os.makedirs(output_dir, exist_ok=True)
    save_df_chunks(df_master, chunk_size, output_dir)

    # merge_csv_files(output_dir, output_pfad)
    merge_csv_files(output_dir, output_pfad)

    return send_file(output_pfad, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)