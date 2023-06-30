from flask import Flask, render_template
# import calculate_data - hier kommt das finale python-script hin

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

# How-to Daten an Flask senden??
# Wie werden DAten empfangen in Flask?
# app output verändern, so dass dort die DAten an output weitergegeben werden (Jinja2 Templates)

@app.route("/output")
def output():
    # get input from index.hhtml (cvs)
    # process csv datei über calculate_data(cvs)
    # data = calculate_data(csv)
    # tempalte = create_thml_template_whti_data
    # return render_template(template)
    return render_template('output.html')

# Get-request vs post-request als einfache "Fehlerlösung" vor dem Abstürzen

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)