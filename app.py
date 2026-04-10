"""
app.py

Has the routes and logic behind the website. Uses threading or in this case
a process for the heavier tasks.

Auth: Tristan Kruithof, Fabian Kinds, Dennis Kuiper
Date: 10/04/2026
Version: 1.0
PEP-8:
"""

import os
# Only used when using wsl
os.environ["DISPLAY"] = ":0"
os.environ["WAYLAND_DISPLAY"] = "wayland-0"
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from multiprocessing import Process, Manager
from flask import Flask, render_template, request, session, redirect, url_for
from python.login import Account
import PipeLine
import os.path as path
from werkzeug.utils import secure_filename
from python.DNA import DNA

app = Flask(__name__)
app.secret_key = 'dsfklasdjfklj*(&D*(@Q#$342hjioasDjkl'
app.config['UPLOAD_FOLDER'] = path.join(os.getcwd(), 'Tools', 'mafft_input', 'user_uploads')

# THIS GLOBAL MUST BE USED IN ORDER TO USE THREADING OR PROCESSES
manager = Manager()
threading_active = manager.dict()


def threaded_newsletter(acc, title, body, exclude):
    global threading_active
    threading_active[acc.email] = {'active': True, 'info_packet': None}
    acc.send_newsletter(title, body, exclude)
    threading_active[acc.email] = {'active': False, 'info_packet': acc.status}


def threaded_signin(acc, admin_password):
    global threading_active
    threading_active[acc.email] = {'active': True, 'info_packet': None}
    acc.signin(admin_password)
    threading_active[acc.email] = {'active': False, 'info_packet': {"status": acc.status[0], "message": acc.status[1], "admin": acc.admin, "newsletter": acc.newsletter}}


def threaded_pipeline(tree_instance, organisms, option, email):
    global threading_active
    threading_active[email] = {'active': True, 'info_packet': None}
    try:
        if option == "common":
            tree_instance.standard(organisms=organisms)
        else:
            tree_instance.fasta_run()
    finally:
        threading_active[email] = {'active': False, 'info_packet': {'new_image' : True}}


@app.route('/')
def root():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})

    return render_template('home.html',user=user, title="Phylogenetic Tree")


@app.route('/home')
def home_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})
    return render_template('home.html',user=user, title="Home")


@app.route('/home/tools')
def tools_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})
    return render_template('tools.html',user=user , title="Tools")


@app.route('/home/create', methods=['POST', 'GET'])
def create_route():
    global threading_active

    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})
    email = user["email"]
    threaded_state = threading_active.get(email, {})
    active = threaded_state.get('active')
    info_packet = threaded_state.get('info_packet')

    new_image = False
    image_path = path.join("static", "pipeline_output", f"{email}_tree.png")
    image_exists = path.exists(image_path)

    organisms = session.get('organisms', [])
    message = ''
    input_method = ''
    shape = ''

    if active:
        pass

    elif info_packet:
        new_image = info_packet['new_image']
        threading_active.pop(email, None)

    elif request.method == 'POST':
        form = request.form
        gene = form.get('gene')
        shape = form.get('Graph')
        input_method = form.get('input_method')
        sequence = form.get('sequence')

        if "add" in form:
            input_organism = form.get('species')
            split_input = [item.strip().lower() for item in input_organism.split(',')]

            if organisms:
                organisms_set = set(organisms)
                split_input_set = set(split_input)
                new_organisms = split_input_set.difference(organisms_set)
            else:
                new_organisms = split_input

            organisms.extend(new_organisms)

        elif "delete_all" in form:
            organisms = []

        elif "delete_org" in form:
            if organisms:
                organisms.pop()

        elif "save" in form:
            acc = Account(**user)
            tree_name = form.get('tree_name')
            acc.save_tree(tree_name)
            message = acc.status[1]

        else:
            acc = Account(**user)
            tree = PipeLine.Run(email, gene, shape, sequence)
            thread_kwargs =  {"organisms": organisms, "tree_instance": tree, "option": "common", "email": email}

            if input_method == "common":

                if len(organisms) >= 4:
                    status, message = acc.add_run()
                    if status:
                        thread = Process(target=threaded_pipeline, kwargs=thread_kwargs)
                        thread.start()
                        active = True
                else:
                    message = "Not enough species to make a tree!"
            else:
                file_types = ["fasta", "fna", "fa", "faa"]
                fasta_file = request.files.get('multi_fasta_file')

                if fasta_file and fasta_file.filename:
                    file_name = fasta_file.filename
                    fasta_file.save(os.path.join(app.config['UPLOAD_FOLDER'], "sequences.fasta"))

                fasta_file.seek(0)
                organisms_set = set()

                if file_name.split('.')[1] in file_types:
                    for line in fasta_file:
                        decoded_line = line.decode('utf-8')

                        if decoded_line.startswith('>'):
                            organism = decoded_line.split(' ')[0]
                            if organism not in organisms_set:
                                organisms_set.add(organism)
                            else:
                                message = "Duplicate animals!"
                                break

                    if len(organisms_set) < 4 and not message:
                        message = "Not enough species to make a tree!"

                    else:
                        status, message = acc.add_run()

                        if status:
                            thread_kwargs["option"] = "fasta"

                            thread = Process(target=threaded_pipeline, kwargs=thread_kwargs)
                            thread.start()
                            active = True
                else:
                    message = "Not a fasta file!"

        session["organisms"] = organisms

    return render_template('create.html',input_method=input_method,message=message, user=user, image_exists=image_exists ,email=email, new_image=new_image, organism_list=organisms, active_thread=active, shape=shape)


@app.route('/home/compare', methods=['POST', 'GET'])
def compare_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})

    acc = Account(**user)
    acc.load_accounts()
    trees = acc.account.get('trees')
    compare = {}

    if request.method == 'POST':
        tree1 = request.form.get('tree1')
        tree2 = request.form.get('tree2')
        compare = PipeLine.compare_trees(tree1=tree1, tree2=tree2)

    return render_template('compare.html',user=user, title="Compare",trees=trees ,compare=compare)


@app.route('/home/help/contact')
def contact_route():
    user = session.get('account', {"email": "", "admin": False, "active": False, "newsletter" : False})
    return render_template('contact.html',user=user ,title="Contact")

  
@app.route('/home/help/installation')
def installation_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})
    return render_template('installation.html',user=user,title="Installation")

  
@app.route('/home/help/about')
def about_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})
    return render_template('about.html', user=user, title="About")


@app.route('/home/signup', methods=['POST', 'GET'])
def signup_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})
    global threading_active

    email = session.get('pending_email', '') or user['email']
    threaded_state = threading_active.get(email, {})
    active = threaded_state.get('active')

    info_packet = threaded_state.get('info_packet')
    message = ''

    if active:
        pass

    elif info_packet:
        threading_active.pop(email, None)
        session.pop('pending_email', None)

        newsletter = info_packet['newsletter']
        admin = info_packet['admin']
        message = info_packet['message']

        if info_packet["status"]:
            session['account'] = {"email": email, "admin": admin, "active": True, "newsletter": newsletter}
        else:
            session['account'] = {"email": "", "admin": False, "active": False, "newsletter": False}

        user = session.get('account')

    elif request.method == 'POST':
        email = request.form.get('email')
        newsletter = bool(request.form.get('newsletter'))
        admin_password = request.form.get('admin_pass')
        session['pending_email'] = email

        acc = Account(email, newsletter)
        thread = Process(target=threaded_signin, args=[acc, admin_password])
        thread.start()
        active = True

    else:
        user['active'] = None
        session['account'] = user

    return render_template('loginpage.html', title="Login", login_message=message, user=user, thread_state=active)


@app.route('/home/newsletter', methods=['POST', 'GET'])
def newsletter_route():
    global threading_active
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})
    threaded_state = threading_active.get(user['email'], {})
    message = ''
    status = False
    active = threaded_state.get('active')
    info_packet = threaded_state.get('info_packet')

    if active:
        pass

    elif info_packet:
        message = info_packet[1]
        status = info_packet[0]
        threading_active.pop(user['email'], None)

    elif request.method == 'POST':
        acc = Account(**user)
        title = request.form.get('title')
        body = request.form.get('body')
        exclude = request.form.get('exclude')

        thread = Process(target=threaded_newsletter, args=[acc, title, body, exclude])
        thread.start()
        active = True

    return render_template('newsletter.html', user=user, message=message, status=status, title="Newsletter",
                           threaded_state=active)


@app.route('/home/DNA', methods=['GET', 'POST'])
def DNA_route():
    user = session.get('account', {"email": "", "admin": False, "active": False, "newsletter": False})
    file_lines = []

    if request.method == 'POST':
        fasta_file = request.files.get('fasta_file')

        if fasta_file:
            save_file = fasta_file.save(secure_filename(fasta_file.filename))
            valid_filename = secure_filename(fasta_file.filename)

            with open(valid_filename, 'r') as file:
                for line in file:
                    if line[0] != '>':
                        file_lines.append(line.replace('\n', ''))

            DNA_sequence = ''.join(file_lines)
            translation = DNA.DNA(DNA_sequence)
            translated_RNA = translation.vertalen_naar_RNA()
            translated_proteins = translation.vertalen_naar_eiwitten()

            RNA_dict = {'translated-sequence': translation}
            for sequence in RNA_dict:
                translated_sequence = RNA_dict['translated-sequence']

                with open(f'translated_sequence.txt', 'w') as file:
                    file.write('RNA-sequence\n')
                    for i in range(0, len(translated_RNA), 70):
                        juiste_lengte = translated_RNA[i:i + 70]
                        file.write(f'{juiste_lengte}{'\n'}')

                    file.write('\nproteins\n')
                    for i in range(0, len(translated_proteins), 70):
                        juiste_lengte = translated_proteins[i:i + 70]
                        file.write(f'{juiste_lengte}{'\n'}')

                return render_template('DNA.html', translated_sequence=translated_sequence, user=user)

        return redirect(url_for('DNA_route'))

    return render_template('DNA.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)