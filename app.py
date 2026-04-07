from flask import Flask, render_template, request, redirect, url_for, session
from python.login import Account
import PipeLine
import os.path as path
from werkzeug.utils import secure_filename
import DNA

app = Flask(__name__)
app.secret_key = 'dsfklasdjfklj*(&D*(@Q#$342hjioasDjkl'



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


@app.route('/home/compare', methods=['POST', 'GET'])
def compare_route():
    login_status = session.get('login_status')

    if request.method == 'POST':
        tree1 = request.form.get('tree1')
        tree2 = request.form.get('tree2')
        compare = PipeLine.compare_trees(tree1=tree1, tree2=tree2)

        return render_template('compare.html', title="Compare", login_status=login_status, compare=compare)
    return render_template('compare.html', title="Compare", login_status=login_status)


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
    if request.method == 'POST' :
        email = request.form.get('email')
        newsletter = request.form.get('newsletter')
        acc = Account(email, newsletter)
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
