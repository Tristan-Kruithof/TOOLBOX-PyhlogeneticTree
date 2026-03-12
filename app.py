from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/home/tools')
def tools():
    return render_template('tools.html')

@app.route('/home/create')
def create():
    return render_template('create.html')

@app.route('/home/compare')
def compare():
    return render_template('compare.html')

@app.route('/home/help/contact')
def contact():
    return render_template('contact.html')

@app.route('/home/help/installation')
def installation():
    return render_template('installation.html')

@app.route('/home/help/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
