from flask import Flask, render_template, request, send_file, redirect, url_for
import master_df_app as mdf
import sys
import os
import pandas as pd
import datetime
import math
import webview
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
    #Create dataframes
    global output_pfad, df_master, stock_quality, sales_quality
    df_master = mdf.setup(lagerbestand_pfad, verkaeufe_pfad, lieferanten_pfad)
    stock_quality, sales_quality = mdf.visuals()
    datum = datetime.date.today().strftime('%Y-%m-%d')
    output_pfad = os.path.join(OUTPUT_DIR, f'Umlagerungen {datum}.xlsx')
    chunk_size = 50000
    temp_dir = os.path.join(OUTPUT_DIR, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    save_df_chunks(df_master, chunk_size, temp_dir)
    merge_csv_files(temp_dir, output_pfad)

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
    # return redirect(url_for('output'))

@app.route("/download")
def download():
    return send_file(output_pfad, as_attachment=True)

if __name__ == '__main__':
    # webview.start(debug=True) # run webview in window mode
    app.run(host="0.0.0.0", debug=True)