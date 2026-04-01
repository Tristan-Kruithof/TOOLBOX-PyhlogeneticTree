import os
import threading
from flask import Flask, render_template, request, session
from python.login import Account
import PipeLine
import os.path as path

app = Flask(__name__)
app.secret_key = 'dsfklasdjfklj*(&D*(@Q#$342hjioasDjkl'
app.config['UPLOAD_FOLDER'] = path.join(os.getcwd(), 'Tools', 'mafft_input', 'user_uploads')

# THIS GLOBAL MUST BE USED IN ORDER TO USE THREADING
threading_active = {}


def threaded(tree_instance, organisms, option, email):
    global threading_active
    threading_active[email] = True
    try:
        if option == "common":
            tree_instance.standard(organisms=organisms)
        else:
            tree_instance.fasta_run()
    finally:
        threading_active.pop(email)

@app.route('/')
def root():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False})

    return render_template('home.html',user=user, title="Phylogenetic Tree")


@app.route('/home')
def home_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False})
    return render_template('home.html',user=user, title="Home")


@app.route('/home/tools')
def tools_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False})
    return render_template('tools.html',user=user , title="Tools")


@app.route('/home/create', methods=['POST', 'GET'])
def create_route():
    global threading_active

    user = session.get('account', {"email" : "", "admin" : False, "active" : False})
    email = user["email"]
    active_pipeline = threading_active.get(email, False)

    organisms = session.get('organisms', [])
    new_image = False
    message = ''

    image_path = path.join("static", "pipeline_output", f"{email}_tree.png")
    image_exists = path.exists(image_path)

    if request.method == 'POST':
        if not active_pipeline:
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

            else:
                acc = Account(email=email)
                tree = PipeLine.Run(email, gene)
                thread_kwargs =  {"organisms": organisms, "tree_instance": tree, "option": "common", "email": email}

                if input_method == "common":

                    if len(organisms) >= 4:
                        status, info = acc.add_run()
                        message = info

                        thread = threading.Thread(target=threaded, kwargs=thread_kwargs)
                        thread.start()

                        active_pipeline = threading_active.get(email, True)
                        new_image = True
                    else:
                        message = "Not enough species to make a tree!"
                else:
                    file_types = ["fasta", "fna", "fa", "faa"]
                    fasta_file = request.files['multi_fasta_file']
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

                            thread = threading.Thread(target=threaded, kwargs=thread_kwargs)
                            thread.start()

                            active_pipeline = threading_active.get(email, True)
                            new_image = True
                    else:
                        message = "Not a fasta file!"

            session["organisms"] = organisms

            return render_template('create.html', user=user,image_exists=image_exists ,email=email, new_image=new_image,
                           organism_list=organisms, message=message, input_method=input_method,
                           active_pipeline=active_pipeline)

    return render_template('create.html', user=user, image_exists=image_exists ,email=email, new_image=new_image, organism_list=organisms, active_pipeline=active_pipeline)


@app.route('/home/compare', methods=['POST', 'GET'])
def compare_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False})
    
    if request.method == 'POST':
        tree1 = request.form.get('tree1')
        tree2 = request.form.get('tree2')
        compare = PipeLine.compare_trees(tree1=tree1, tree2=tree2)

        return render_template('compare.html',user=user, title="Compare", compare=compare)
    return render_template('compare.html',user=user ,title="Compare")


@app.route('/home/help/contact')
def contact_route():
    user = session.get('account', {"email": "", "admin": False, "active": False})
    return render_template('contact.html',user=user ,title="Contact")

  
@app.route('/home/help/installation')
def installation_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False})
    return render_template('installation.html',user=user,title="Installation")

  
@app.route('/home/help/about')
def about_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False})
    return render_template('about.html', user=user, title="About")


@app.route('/home/signup', methods=['POST', 'GET'])
def signup_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False})
    if request.method == 'POST' :
        email = request.form.get('email')
        newsletter = request.form.get('newsletter')
        admin_password = request.form.get('admin_pass')

        acc = Account(email, newsletter)
        acc.signin(admin_password)
        status = acc.status

        admin = acc.admin
        validation = status[0]
        message = status[1]

        if validation:
            session['account'] = {"email" : email, "admin" : admin, "active" : True}
        else:
            session['account'] = {"email" : "", "admin" : False, "active" : False}

        user = session.get('account')
        return render_template('loginpage.html', title="Login",user=user, login_message=message)

    user["active"] = None
    session['account'] = user
    return render_template('loginpage.html', title="Login", user=user)


@app.route('/home/newsletter')
def newsletter_route():
    user = session.get('account', {"email" : "", "admin" : False, "active" : False})
    return render_template('newsletter.html', user=user, title="Newsletter")


if __name__ == '__main__':
    app.run(debug=True)