from flask import Flask, render_template, request, session
from python.login import Account
import PipeLine
import os.path as path

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
    organisms = session.get('organisms', [])
    new_image = False

    if request.method == 'POST':
        form = request.form
        input_method = form.get('input_method')
        message = ""

        if "add" in form:
            input_organism = form.get('species')
            split_input = [item.strip().lower() for item in input_organism.split(',')]

            organisms.extend(split_input)
            organisms = list(set(organisms))
            session["organisms"] = organisms

        elif "delete_all" in form:
            session["organisms"] = []
            organisms = []

        elif "delete_org" in form:
            organisms = organisms[0:-1]
            session["organisms"] = organisms

        else:
            email = session.get('email')
            fasta_extensions = ["fasta","fna","fa"]

            if input_method == "common":
                if len(organisms) >= 4:
                    tree = PipeLine.Run(email)
                    tree.standard(organisms=organisms)
                    new_image = True
                else:
                    message = "Not enough species to make a tree!"
            else:
                fasta_file = form['multi_fasta_file']

                if fasta_file.split('.')[1] in fasta_extensions:
                    # Put logic here
                    print("Correct")
                else:
                    message = "Not a fasta file!"


        return render_template('create.html', login_status=login_status, tree_image="tree.png", new_image=new_image ,organism_list=organisms, message=message, input_method=input_method)

    return render_template('create.html', login_status=login_status, tree_image="tree.png",new_image=new_image, organism_list=organisms)


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


if __name__ == '__main__':
    app.run(debug=True)
