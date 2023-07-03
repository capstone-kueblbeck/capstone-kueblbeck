from flask import Flask, render_template, request, send_file, redirect, url_for
from master_df_app import setup
import uuid
import os
import pandas as pd
# import calculate_data - hier kommt das finale python-script hin

app = Flask(__name__)
UPLOADS_DIR = os.path.abspath('uploads')
OUTPUT_DIR = os.path.abspath('output')
df_master = None

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'lagerbestand' in request.files and 'verkaeufe' in request.files:
            lagerbestand = request.files['lagerbestand']
            verkaeufe = request.files['verkaeufe']

            # lagerbestand_tempname = str(uuid.uuid4())
            # verkaeufe_tempname = str(uuid.uuid4())

            lagerbestand_pfad = os.path.join(UPLOADS_DIR, 'lagerbestand.csv')
            verkaeufe_pfad = os.path.join(UPLOADS_DIR, 'verkaeufe.csv')

            lagerbestand.save(lagerbestand_pfad)
            verkaeufe.save(verkaeufe_pfad)

            global df_master
            #command = f'python master_df_app.py --lagerbestand {lagerbestand_pfad} --verkaeufe {verkaeufe_pfad}'
            df_master = setup(lagerbestand_pfad, verkaeufe_pfad)

            return redirect(url_for('output'))

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
    return render_template('output.html')

@app.route("/download")
def download():
    global df_master
    if df_master is None:
        return redirect(url_for('home'))
    
    output_pfad = 'output/output.csv'
    df_master.to_csv(output_pfad, index=False)
    return send_file(output_pfad, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)