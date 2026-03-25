from flask import Flask, render_template, request, session
from python.login import Account
import PipeLine
import os.path as path
app = Flask(__name__)
app.secret_key = "Jl%&*ad93248908fs&*(*liA*JK:)(@*#$(*(#%"


@app.route('/')
def root_route():
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
    calc_dict = {"square": "squared.png", "division": "division.png", "multiplication": "Simple_multiplication.png",
                 "addition": "addition.png", "substraction": "substraction.jpg"}

    if request.method == 'POST':
        selection = request.form['calculator']
        value = 1
        ins = "Elephant, Pig, Cow, horse, Lion, Tiger"

        tree_pipeline = PipeLine.Organisms(value, ins)
        tree_pipeline.find_scientific_names()
        tree_pipeline.find_fastas()
        tree_pipeline.make_multi_fasta()

        Maffie = PipeLine.CC_Tools(path.abspath("Tools"), path.abspath("Tools/sequences.fasta"),
                                   path.abspath("Tools/aligned_sequences.fasta"))
        Maffie.run()

        Megurt = PipeLine.CC_Tools(path.abspath("Tools"), path.abspath("Tools/aligned_sequences.fasta"),
                                   path.abspath("Tools/newick.nwk"), path.abspath("Tools/infer_ML_nucleotide.mao"))
        Megurt.run()

        tree = PipeLine.boom()
        tree.render("static/pipeline_output/image.png")


        return render_template('create.html', title="Create", result="Number too big to calculate!", selection=selection, login_status=login_status, image="image.png")



    else:
        selector_value = request.args.get('selectorValue')
        if selector_value:
            image_source = calc_dict[selector_value]

            return f'/static/images/create/{image_source}'

        return render_template('create.html', title="Create", login_status=login_status)


@app.route('/home/compare')
def compare_route():
    login_status = session.get('login_status')
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
    if request.method == 'POST':
        email = request.form.get('email')
        newsletter = request.form.get('newsletter')
        acc = Account(email, newsletter)
        acc.signin()
        status = acc.status

        validation = status[0]
        message = status[1]

        session['login_status'] = validation
        login_status = validation


        return render_template('loginpage.html', title="Login", status=login_status, login_status=login_status, login_message=message)

    session['login_status'] = None
    login_status = session.get('login_status')
    return render_template('loginpage.html', title="Login", status=login_status, login_status=login_status)



if __name__ == '__main__':
    app.run()