from flask import Flask, render_template, request, redirect, url_for, \
abort, session
from fc import compare

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
	session['link1'] = request.form['link1']
	session['link2'] = request.form['link2']
	session['my_results'] = compare("film", session['link1'], session['link2'])
	return redirect(url_for('results'))

@app.route('/results')
def results():
#	if not 'username' in session:
#		return abort(403)
	return render_template('results.html', link1 = session['link1'], \
link2 = session['link2'], my_results = session['my_results'])

if __name__ == '__main__':
	app.run(debug=True)
