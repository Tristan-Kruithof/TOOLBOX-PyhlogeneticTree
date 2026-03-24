from flask import Flask, render_template, request, session
from python.login import Account
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
        input_1 = int(request.form['input_field'])
        input_2 = int(request.form['input_field_2'])

        math = calc_dict[selection]


        try:
            if selection == "division":
                if input_2 == 0:
                    return render_template('create.html', title="Create", math=math, result="Cannot divide by 0!", input_1=input_1, input_2=input_2, selection=selection, login_status=login_status)
                result = input_1 / input_2
            elif selection == "multiplication":
                result = input_1 * input_2
            elif selection == "addition":
                result = input_1 + input_2
            elif selection == "substraction":
                result = input_1 - input_2
            else:
                result = int(float(input_1) ** float(input_2))

            return render_template('create.html', title="Create", math=math, result=result, input_1=input_1, input_2=input_2, selection=selection, login_status=login_status)

        except (OverflowError, ValueError):
            return render_template('create.html', title="Create", math=math, result="Number too big to calculate!", input_1=input_1, input_2=input_2, selection=selection, login_status=login_status)


    else:
        selector_value = request.args.get('selectorValue')
        if selector_value:
            image_source = calc_dict[selector_value]

            return f'/static/images/create/{image_source}'

        return render_template('create.html', title="Create", math="squared.png", login_status=login_status)


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
    login_status = session.get('login_status')

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

