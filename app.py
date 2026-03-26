from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('home.html', title="Phylogenetic Tree")

@app.route('/home')
def home():
    return render_template('home.html', title="Home")

@app.route('/home/tools')
def tools():

    return render_template('tools.html', title="Tools")

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
                                       path.abspath("Tools/newick.nwk"), path.abspath("Tools/infer_ML_nucleotide.mao"))
            Megurt.run()

            tree = PipeLine.boom()
            tree.render("Tools/image.png")

            return render_template('create.html', title="Create", math=math, result=result, input_1=input_1, input_2=input_2, selection=selection)

        return render_template('create.html', title="Create", result="Number too big to calculate!", login_status=login_status)


    return render_template('create.html', title="Create", math="squared.png", login_status=login_status)


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
def contact():
    return render_template('contact.html', title="Contact")

  
@app.route('/home/help/installation')
def installation():
    return render_template('installation.html', title="Installation")

  
@app.route('/home/help/about')
def about():
    return render_template('about.html', title="About")

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

        if validation:
            session['email'] = email

        return render_template('loginpage.html', title="Login", status=login_status, login_status=login_status, login_message=message)

    session['login_status'] = None
    login_status = session.get('login_status')
    return render_template('loginpage.html', title="Login", status=login_status, login_status=login_status)

  
@app.route('/home/front_end', methods=['POST', 'GET'])
def front_end():
    if request.method == 'POST':
        kwargs = {
            'species': request.form['species']
        }
        saved_organisms = []
        input_species = request.form.get('species')
        if input_species:
            saved_organisms.append(input_species)
            print(saved_organisms)
        return redirect(url_for('front_end'))
    return render_template('get.html')

  
if __name__ == '__main__':
    app.run()
