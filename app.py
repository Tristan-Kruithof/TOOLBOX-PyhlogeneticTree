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
def create():
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
                    return render_template('create.html', title="Create", math=math, result="Cannot divide by 0!", input_1=input_1, input_2=input_2, selection=selection)
                result = input_1 / input_2
            elif selection == "multiplication":
                result = input_1 * input_2
            elif selection == "addition":
                result = input_1 + input_2
            elif selection == "substraction":
                result = input_1 - input_2
            else:
                result = int(float(input_1) ** float(input_2))

            return render_template('create.html', title="Create", math=math, result=result, input_1=input_1, input_2=input_2, selection=selection)

        except (OverflowError, ValueError):
            return render_template('create.html', title="Create", math=math, result="Number too big to calculate!", input_1=input_1, input_2=input_2, selection=selection)


    else:
        selector_value = request.args.get('selectorValue')
        if selector_value:
            image_source = calc_dict[selector_value]

            return f'/static/images/create/{image_source}'

        return render_template('create.html', title="Create", math="squared.png")


@app.route('/home/compare')
def compare():
    return render_template('compare.html', title="Compare")

@app.route('/home/help/contact')
def contact():
    return render_template('contact.html', title="Contact")

@app.route('/home/help/installation')
def installation():
    return render_template('installation.html', title="Installation")

@app.route('/home/help/about')
def about():
    return render_template('about.html', title="About")






































saved_organisms = []
@app.route('/home/front_end', methods=['POST', 'GET'])
def front_end():
    if request.method == 'POST':
        kwargs = {
            'species': request.form['species']
        }
        input_species = request.form.get('species')
        if input_species:
            saved_organisms.append(input_species)
            print(saved_organisms)
        return redirect(url_for('front_end'))
    return render_template('get.html')

if __name__ == '__main__':
    app.run()
