from flask import Flask, render_template, request, redirect, url_for, session
from python.login import Account
import PipeLine
import os.path as path
from werkzeug.utils import secure_filename
import DNA

app = Flask(__name__)
app.secret_key = 'dsfklasdjfklj*(&D*(@Q#$342hjioasDjkl'
<<<<<<< HEAD
app.config['UPLOAD_FOLDER'] = path.join(os.getcwd(), 'Tools', 'mafft_input', 'user_uploads')

# THIS GLOBAL MUST BE USED IN ORDER TO USE THREADING
threading_active = {}

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
=======


>>>>>>> 6e46949fe8d1b8d8fa7a3bfa6ad6b700bdb26b4b

@app.route('/')
def root():
    login_status = session.get('login_status')
    return render_template('home.html', title="Phylogenetic Tree", login_status=login_status)

@app.route('/home')
def home_route():
    login_status = session.get('login_status')
    return render_template('home.html', title="Home", login_status=login_status)

@app.route('/home/tools')
def tools_route():
    login_status = session.get('login_status')
    return render_template('tools.html', title="Tools", login_status=login_status)

@app.route('/home/create', methods=['POST', 'GET'])
def create_route():
    login_status = session.get('login_status')

<<<<<<< HEAD
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

    if active:
        pass

    elif info_packet:
        new_image = info_packet['new_image']
        threading_active.pop(email, None)

    elif request.method == 'POST':
        form = request.form
        gene = form.get('gene')
        input_method = form.get('input_method')

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
            organisms.pop()

        elif "save" in form:
            acc = Account(**user)
            tree_name = form.get('tree_name')
            acc.save_tree(tree_name)
            message = acc.status[1]

        else:
            acc = Account(**user)
            tree = PipeLine.Run(email, gene)
            thread_kwargs =  {"organisms": organisms, "tree_instance": tree, "option": "common", "email": email}

            if input_method == "common":

                if len(organisms) >= 4:
                    status, info = acc.add_run()
                    message = info

                    thread = threading.Thread(target=threaded_pipeline, kwargs=thread_kwargs)
                    thread.start()
                    active = True
                else:
                    message = "Not enough species to make a tree!"
            else:
                file_types = ["fasta", "fna", "fa", "faa"]
                fasta_file = request.files.get('multi_fasta_file')
                file_name = fasta_file.filename
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
                        status, info = acc.add_run()
                        if info:
                            message = info

                        fasta_file.save(os.path.join(app.config['UPLOAD_FOLDER'], "sequences.fasta"))
                        thread_kwargs["option"] = "fasta"

                        thread = threading.Thread(target=threaded_pipeline, kwargs=thread_kwargs)
                        thread.start()
                        active = True
                else:
                    message = "Not a fasta file!"

        session["organisms"] = organisms

    return render_template('create.html',input_method=input_method,message=message, user=user, image_exists=image_exists ,email=email, new_image=new_image, organism_list=organisms, active_thread=active)
=======
    if request.method == 'POST':
        if login_status:
            value = 1
            ins = "Elephant, Pig, Cow, horse, Lion, Tiger"
            email = session.get('email')

            tree_pipeline = PipeLine.Organisms(value, ins, email)
            tree_pipeline.find_scientific_names()
            tree_pipeline.find_fastas()
            tree_pipeline.make_multi_fasta()

            Maffie = PipeLine.CC_Tools(path.abspath("Tools"), path.abspath("Tools/sequences.fasta"),
                                       path.abspath("Tools/aligned_sequences.fasta"))
            Maffie.run()

            Megurt = PipeLine.CC_Tools(path.abspath("Tools"), path.abspath("Tools/aligned_sequences.fasta"),
                                       path.abspath("Tools/newick.nwk"), path.abspath(
                    "Tools/infer_ML_nucleotide.mao"))
            Megurt.run()

            tree = PipeLine.boom()
            tree.render("static/pipeline_output/image.png")

        return render_template('create.html', title="Create", login_status=login_status, image="image.png")


    return render_template('create.html', title="Create", login_status=login_status)
>>>>>>> 6e46949fe8d1b8d8fa7a3bfa6ad6b700bdb26b4b


@app.route('/home/compare', methods=['POST', 'GET'])
def compare_route():
<<<<<<< HEAD
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})

    acc = Account(**user)
    acc.load_accounts()
    trees = acc.account.get('trees')
    compare = {}
    
=======
    login_status = session.get('login_status')

>>>>>>> 6e46949fe8d1b8d8fa7a3bfa6ad6b700bdb26b4b
    if request.method == 'POST':
        tree1 = request.form.get('tree1')
        tree2 = request.form.get('tree2')
        compare = PipeLine.compare_trees(tree1=tree1, tree2=tree2)

<<<<<<< HEAD

    return render_template('compare.html',user=user, title="Compare",trees=trees ,compare=compare)
=======
        return render_template('compare.html', title="Compare", login_status=login_status, compare=compare)
    return render_template('compare.html', title="Compare", login_status=login_status)
>>>>>>> 6e46949fe8d1b8d8fa7a3bfa6ad6b700bdb26b4b


@app.route('/home/help/contact')
def contact_route():
    login_status = session.get('login_status')
    return render_template('contact.html', title="Contact", login_status=login_status)

  
@app.route('/home/help/installation')
def installation_route():
    login_status = session.get('login_status')
    return render_template('installation.html', title="Installation", login_status=login_status)

  
@app.route('/home/help/about')
def about_route():
    login_status = session.get('login_status')
    return render_template('about.html', title="About", login_status=login_status)

@app.route('/home/signup', methods=['POST', 'GET'])
def signup_route():
<<<<<<< HEAD
    user = session.get('account', {"email" : "", "admin" : False, "active" : False, "newsletter" : False})
    global threading_active
    email = session.get('pending_email', '')
    threaded_state = threading_active.get(user['email'], {})
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
=======
    if request.method == 'POST' :
>>>>>>> 6e46949fe8d1b8d8fa7a3bfa6ad6b700bdb26b4b
        email = request.form.get('email')
        newsletter = request.form.get('newsletter')
        acc = Account(email, newsletter)
<<<<<<< HEAD
        thread = threading.Thread(target=threaded_signin, args=[acc, admin_password])
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

        thread = threading.Thread(target=threaded_newsletter, args=[acc, title, body, exclude])
        thread.start()
        active = True

    return render_template('newsletter.html', user=user, message=message, status=status, title="Newsletter",
                           threaded_state=active)
=======
        acc.signin()
        status = acc.status

        validation = status[0]
        message = status[1]

        session['login_status'] = validation
        login_status = validation

        if validation:
            session['email'] = email

        return render_template('loginpage.html', title="Login", status=login_status, login_status=login_status, login_message=message)

    session['login_status'] = None
    login_status = session.get('login_status')
    return render_template('loginpage.html', title="Login", status=login_status, login_status=login_status)
>>>>>>> 6e46949fe8d1b8d8fa7a3bfa6ad6b700bdb26b4b

  
@app.route('/home/front_end', methods=['POST', 'GET'])
def front_end_route():
    login_status = session.get('login_status')
    if request.method == 'POST':
        kwargs = {
            'species': request.form['species']
        }
        saved_organisms = []
        input_species = request.form.get('species')
        if input_species:
            saved_organisms.append(input_species)
            print(saved_organisms)
        return redirect(url_for('front_end_route'))
    return render_template('get.html', login_status=login_status)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/home/DNA', methods=['GET', 'POST'])
def DNA_route():
    file_lines = []
    if request.method == 'POST':
        fasta_file = request.files.get('fasta_file')

        if fasta_file:
            valid_file = fasta_file.save(secure_filename(fasta_file.filename))
            with open(fasta_file.filename, 'r') as file:
                for line in file:
                    if line[0] != '>':
                        file_lines.append(line.replace('\n', ''))

                # opent het fasta-bestand
            DNA_sequence = ''.join(file_lines)


                # zet de regels van het bestand in een lijst


        return redirect(url_for('DNA_route'))
    return render_template('DNA.html')
if __name__ == '__main__':
    app.run()
