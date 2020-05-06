"""
Main back-end script of Flask web application. 
"""
from flask_cors import CORS
from flask import *
from werkzeug.utils import secure_filename
from Bio import SeqIO, Seq
from pathlib import Path
from models import *
import os
import shutil
import datetime
import uuid
import pandas as pd
import arrow
import annotate
import genemark

# configuration
ROOT = os.path.dirname(os.path.abspath(__file__))
FASTA_EXTENSIONS = set(['.fasta', '.fna'])
GENBANK_EXTENSIONS = set(['.gb', '.gbk'])
GDATA_EXTENSION = set(['.gdata'])
LDATA_EXTENSION = set(['.ldata'])
USERS = []
CURRENT_USER = ""

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
db.init_app(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# routers ------------------------------------------------------------------
@app.route('/api/home/<phage_id>', methods=['POST'])
def check_phage_id(phage_id):
    """
    API endpoint for '/'.
    POST method removes users that have existed for more than 90 days, creates a new
        user if it doesn't exist, else gets informations for existing user. 
    """
    response_object = {}

    if request.method == "POST":
        # remove 90 day yo users
        critical_time = arrow.now().shift(days=-90)
        for user in Path(os.path.join(ROOT, 'users')).glob('*'):
            user_time = arrow.get(user.stat().st_mtime)
            if user_time < critical_time:
                shutil.rmtree(user)

        # get list of existing users
        USERS = []
        for dir in os.listdir(os.path.join(ROOT, 'users')):
            USERS.append(dir)
        print(USERS)

        # check if user-inputted phage id exists or not
        if phage_id in USERS:
            DATABASE = "sqlite:///{}".format(os.path.join(
                ROOT, 'users', phage_id, f"{phage_id}.db"))
            app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
            response_object['message'] = "ID already exists. If this is your ID, please continue. If not, enter a new one."
        else:
            create_directory(os.path.join(ROOT, 'users', phage_id))
            create_directory(os.path.join(ROOT, 'users', phage_id, 'uploads'))
            DATABASE = "sqlite:///{}".format(os.path.join(
                ROOT, 'users', phage_id, f"{phage_id}.db"))
            app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
            with app.app_context():
                db.drop_all()
                db.create_all()
            response_object["message"] = "ID created. Please continue."

    return jsonify(response_object)


@app.route('/api/upload/<current_user>', methods=['GET', 'POST'])
def upload_files(current_user):
    """
    API endpoint for '/upload/:current_user'.
    POST method uploads files accordingly and removes files if necessary.
    """
    UPLOAD_FOLDER = os.path.join(ROOT, 'users', current_user, 'uploads')
    DATABASE = "sqlite:///{}".format(os.path.join(ROOT, 'users', current_user, f"{current_user}.db"))
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
    response_object = {}

    if request.method == "GET":
        fasta_file = get_file("Fasta", UPLOAD_FOLDER)
        genemark.run_genemark(fasta_file)
        print("ran genemark")

    if request.method == "POST":
        if 'file' not in request.files:
            response_object["status"]: "'file' not in request.files"
        else:
            file = request.files['file']
            fileType = request.form['fileType']
            if file:
                file_name = secure_filename(file.filename)
                if (fileType == "fasta" and allowed_file(file_name, FASTA_EXTENSIONS)) or \
                   (fileType == "genbank" and allowed_file(file_name, GENBANK_EXTENSIONS)) or \
                   (fileType == "gdata" and allowed_file(file_name, GDATA_EXTENSION)) or \
                   (fileType == "ldata" and allowed_file(file_name, LDATA_EXTENSION)):

                    # overwrite existing with similar extension with newly uploaded file
                    for existing_file in os.listdir(UPLOAD_FOLDER):
                        ext = os.path.splitext(existing_file)[1].lower()
                        if (fileType == "fasta" and ext in FASTA_EXTENSIONS) or \
                           (fileType == "genbank" and ext in GENBANK_EXTENSIONS) or \
                           (fileType == "gdata" and ext in GDATA_EXTENSION) or \
                           (fileType == "ldata" and ext in LDATA_EXTENSION):
                            os.remove(os.path.join(UPLOAD_FOLDER, existing_file))
                            print(f" * removed {existing_file}")

                    file.save(os.path.join(UPLOAD_FOLDER, file_name))
                    response_object["uploaded"] = file_name
                    print(' * uploaded', file_name)

                    # parse appropriate files as soon as uploaded
                    # FIXME: check file conent before parsing. 
                    file_ext = os.path.splitext(file_name)[1].lower()
                    if file_ext in GENBANK_EXTENSIONS:
                        genbank_file = get_file("GenBank", UPLOAD_FOLDER)
                        annotate.parse_dnamaster_genbank(genbank_file)
                    elif file_ext in LDATA_EXTENSION:
                        genemark_ldata_file = get_file("GeneMark_ldata", UPLOAD_FOLDER)
                        annotate.parse_genemark_ldata(genemark_ldata_file)
                else:
                    response_object["not_allowed"] = file.filename
            else:
                response_object["status"] = "error"

    return jsonify(response_object)


@app.route('/api/dnamaster/<current_user>', methods=['GET', 'POST'])
def dnamaster(current_user):
    """
    API endpoint for '/dnamaster/:current_user'.
    GET method querys database for parsed DNA Master data (from uploaded GenBank file).
    POST method adds a new CDS to the data.
    """
    DATABASE = "sqlite:///{}".format(os.path.join(ROOT, 'users', current_user, f"{current_user}.db"))
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
    response_object = {}

    if request.method == "GET":
        dnamaster = []
        for cds in db.session.query(DNAMaster).order_by(DNAMaster.start):
            dnamaster.append({'id': cds.id,
                              'start': cds.start,
                              'stop': cds.stop,
                              'strand': cds.strand})
        response_object['dnamaster'] = dnamaster

    if request.method == "POST":
        post_data = request.get_json()
        cds = DNAMaster(id = post_data.get('id'),
                        start = int(post_data.get('start')),
                        stop = int(post_data.get('stop')),
                        strand = post_data.get('strand'),
                        function = "None",
                        status = "None")
        start_exists = DNAMaster.query.filter_by(start=post_data.get('start')).first()
        stop_exists = DNAMaster.query.filter_by(stop=post_data.get('stop')).first()
        id_exists = DNAMaster.query.filter_by(id=post_data.get('id')).first()
        if cds.start > cds.stop or cds.start == cds.stop:
            response_object['message'] = 'Start is not less than start. CDS not added.'
        elif start_exists and stop_exists:
            if start_exists.id == stop_exists.id:
                response_object['message'] = 'Start and stop already exists. CDS not added.'
        elif id_exists:
            if id_exists.id == cds.id:
                response_object['message'] = 'ID already exists. CDS not added.'
        else:
            db.session.add(cds)
            db.session.commit()
            response_object['message'] = 'CDS added!'

    return jsonify(response_object)


@app.route('/api/dnamaster/<current_user>/<cds_id>', methods=['PUT', 'DELETE'])
def dnamaster_cds(current_user, cds_id):
    """
    API endpoint for '/dnamaster/:current_user/:cds_id'.
    PUT method updates a CDS.
    DELETE method deletes a CDS.
    """
    DATABASE = "sqlite:///{}".format(os.path.join(ROOT, 'users', current_user, f"{current_user}.db"))
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
    response_object = {}

    if request.method == "PUT":
        put_data = request.get_json()
        cds = DNAMaster.query.filter_by(id=put_data.get('id')).first()
        if cds:
            cds.start = put_data.get('start')
            cds.stop = put_data.get('stop')
            cds.strand = put_data.get('strand')
            db.session.commit()
            response_object['message'] = 'CDS updated!'
        else:
            response_object['message'] = 'Error: CDS could not get updated.'

    if request.method == 'DELETE':
        if DNAMaster.query.filter_by(id=cds_id).first():
            DNAMaster.query.filter_by(id=cds_id).delete()
            db.session.commit()
            response_object['message'] = 'CDS removed!'
        else:
            response_object['message'] = 'Error: CDS could not be deleted.'

    return jsonify(response_object)

# TODO: Continue checking code from here.
@app.route('/api/blast/<current_user>/<file_method>', methods=['POST'])
def upload_blast_file(current_user, file_method):
    """
    API endpoint for '/blast/:current_user'.
    POST method downloads fasta file for BLAST input or 
        uploads json file of BLAST output
    """
    UPLOAD_FOLDER = os.path.join(ROOT, 'users', current_user, 'uploads')
    DATABASE = "sqlite:///{}".format(os.path.join(ROOT, 'users', current_user, f"{current_user}.db"))
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
    response_object = {'status': 'success'}

    if request.method == "POST":
        if file_method == "download":
            print("Starting comparisons")
            annotate.compare()
            fasta_file = get_file("Fasta", UPLOAD_FOLDER)
            genemark_gdata_file = get_file("GeneMark_gdata", UPLOAD_FOLDER)
            output = annotate.create_fasta(fasta_file, genemark_gdata_file)

            with open(os.path.join(ROOT, 'users', current_user, f"{current_user}_blast.fasta"), "w") as out_handle:
                out_handle.write(output)

            f = open(os.path.join(ROOT, 'users', current_user,
                                  f"{current_user}_blast.fasta"), "r")
            return f.read()
        elif file_method == "upload":
            if 'file' not in request.files:
                response_object["status"]: "'file' not in request.files"
                print("in fail")
            else:
                print("in success")
                file = request.files['file']
                if file:
                    file_name = secure_filename(file.filename)
                    if allowed_file(file_name, set(['.json'])):

                        file_ext = file_name.rsplit('.', 1)[1].lower()
                        for existing_file in os.listdir(UPLOAD_FOLDER):
                            if existing_file.endswith(f".{file_ext}"):
                                os.remove(os.path.join(
                                    UPLOAD_FOLDER, existing_file))

                        file.save(os.path.join(UPLOAD_FOLDER, file_name))
                        response_object["uploaded"] = file_name
                        print(' * uploaded', file_name)
                    else:
                        response_object["not_allowed"] = file.filename
                else:
                    response_object["status"] = "error"

    return jsonify(response_object)


@app.route('/api/annotations/<current_user>', methods=['GET', 'POST'])
def annotate_data(current_user):
    """
    Compares DNA Master's predictions against GeneMark's.
    GET method shows all the DNA Master predictions with a status and action item for each.
    """
    DATABASE = "sqlite:///{}".format(os.path.join(ROOT,
                                                  'users', current_user, f"{current_user}.db"))
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
    UPLOAD_FOLDER = os.path.join(ROOT, 'users', current_user, 'uploads')
    response_object = {'status': 'success'}

    if request.method == "GET":
        dnamaster = []
        for cds in db.session.query(DNAMaster).order_by(DNAMaster.start):
            dnamaster.append({'id': cds.id,
                              'start': cds.start,
                              'stop': cds.stop,
                              'strand': cds.strand,
                              'function': cds.function,
                              'status': cds.status})
        response_object['dnamaster'] = dnamaster

    if request.method == "POST":
        # -------downloading GENBANK file----------
        gb_file = get_file("GenBank", UPLOAD_FOLDER)
        fasta_file = get_file("Fasta", UPLOAD_FOLDER)
        out_file = annotate.modify_genbank(gb_file, fasta_file)
        f = open(out_file, "r")
        return f.read()

    return jsonify(response_object)


@app.route('/api/annotations/cds/<current_user>/<cds_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cds_annotation(current_user, cds_id):
    """
    Annotation information for each CDS. 
    GET method gets cds, its start options, blast results, and graph data.
    PUT method updates the start position and function if the user chooses to do so.
    """
    DATABASE = "sqlite:///{}".format(os.path.join(ROOT,
                                                  'users', current_user, f"{current_user}.db"))
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
    UPLOAD_FOLDER = os.path.join(ROOT, 'users', current_user, 'uploads')
    response_object = {'status': 'success'}

    if request.method == "GET":
        cds = DNAMaster.query.filter_by(id=cds_id).first()
        response_object['cds'] = {'id': cds.id,
                                  'start': cds.start,
                                  'stop': cds.stop,
                                  'strand': cds.strand,
                                  'function': cds.function,
                                  'status': cds.status}

        # fasta_file = get_file("Fasta", UPLOAD_FOLDER)
        starts = [int(start) for start in cds.start_options.split(",")]
        print(starts)
        response_object['start_options'] = starts

        blast_file = get_file("Blast", UPLOAD_FOLDER)
        E_VALUE_THRESH = 1e-7
        print("parsing blast")
        blast_results = annotate.parse_blast_multiple(
            blast_file, cds.id, E_VALUE_THRESH)
        print("writing results to post response")
        response_object['blast'] = blast_results

        genemark_gdata_file = get_file("GeneMark_gdata", UPLOAD_FOLDER)
        gdata_df = pd.read_csv(genemark_gdata_file, sep='\t', skiprows=16)
        gdata_df.columns = ['Base', '1', '2', '3', '4', '5', '6']
        gdata_df = gdata_df[gdata_df.Base.isin(
            range(min(starts) - 100, cds.stop + 100))]
        response_object['x_data'] = gdata_df["Base"].to_list()
        response_object['y_data_1'] = gdata_df["1"].to_list()
        response_object['y_data_2'] = gdata_df["2"].to_list()
        response_object['y_data_3'] = gdata_df["3"].to_list()
        response_object['y_data_4'] = gdata_df["4"].to_list()
        response_object['y_data_5'] = gdata_df["5"].to_list()
        response_object['y_data_6'] = gdata_df["6"].to_list()

    if request.method == "PUT":
        put_data = request.get_json()
        cds = DNAMaster.query.filter_by(id=cds_id).first()
        if cds:
            cds.start = put_data.get('start')
            cds.function = put_data.get('function')
            cds.status = put_data.get('status')
            db.session.commit()
            response_object['message'] = 'CDS updated!'
        else:
            response_object['message'] = 'CDS did not update.'

    if request.method == "DELETE":
        if DNAMaster.query.filter_by(id=cds_id).first():
            DNAMaster.query.filter_by(id=cds_id).delete()
            db.session.commit()
            response_object['message'] = 'CDS removed!'
        else:
            response_object['message'] = 'Error: CDS could not be deleted.'

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()


# ---------- HELPER FUNCTIONS ----------

# check file extension. only allow specific ones
def allowed_file(filename, allowed_extensions):
    return '.' in filename and os.path.splitext(filename)[1].lower() in allowed_extensions

# create directory
def create_directory(directory):
    try:
        os.mkdir(directory)
        print("Directory \'" + directory + "\' created.")
    except FileExistsError:
        print("Directory \'" + directory + "\' already exists.")

# Get necessary file from uploads dir depending on preference
def get_file(preference, upload_directory):
    for filename in os.listdir(upload_directory):
        if preference == "GenBank":
            if filename.endswith(".gb") or filename.endswith(".genbank"):
                return os.path.join(upload_directory, filename)
        elif preference == "GeneMark_ldata":
            if filename.endswith(".ldata"):
                return os.path.join(upload_directory, filename)
        elif preference == "GeneMark_gdata":
            if filename.endswith(".gdata"):
                return os.path.join(upload_directory, filename)
        elif preference == "Fasta":
            if filename.endswith(".fasta"):
                return os.path.join(upload_directory, filename)
        elif preference == "Blast":
            if filename.endswith(".json"):
                return os.path.join(upload_directory, filename)
        else:
            return("Couldn't find file.")