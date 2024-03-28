from flask import Flask, render_template, request,redirect, url_for
from mashpit.query import get_query_sig, generate_query_table, generate_mashtree
import os
import threading


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

# Global variable to store the output of the classification
mashpit_out = None
mashpit_thread = None
mashpit_status = "in progress"

def run_mashpit(database_db,database_sig,assembly_file):
    return


@app.route("/", methods=['GET'])
def upload():
    return render_template('upload.html')

@app.route("/submit", methods=['POST'])
def submit():
    database_db = request.files['formFile_db']
    file_path_db = os.path.join(app.config['UPLOAD_FOLDER'], database_db.filename)
    database_db.save(file_path_db)
    database_sig = request.files['formFile_sig']
    file_path_sig = os.path.join(app.config['UPLOAD_FOLDER'], database_sig.filename)
    database_sig.save(file_path_sig)
    assembly_file = request.files['formFile_assembly']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], assembly_file.filename)
    assembly_file.save(file_path)

    global mashpit_thread
    global mashpit_status
    
    mashpit_thread = threading.Thread(target=run_mashpit, args=(database_db,database_sig,assembly_file,))
    mashpit_thread.start()

    return redirect(url_for('loading'))

@app.route('/loading')
def loading():
    """
    Show loading page while classification is running
    """
    global mashpit_thread
    global mashpit_status
    return render_template('loading.html')

@app.route('/result')
def result():
    """
    Show classification results
    """
    global mashpit_out
    global mashpit_status
    mashpit_status = "in progress"
    return render_template('result.html', table=mashpit_out)

@app.route('/status')
def status():
    """
    Return the current status of the classification
    """
    global mashpit_status
    return mashpit_status

def webserver(args):
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
    