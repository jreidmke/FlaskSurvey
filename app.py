from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

survey = surveys['satisfaction']
responses = []

@app.route('/')
def show_home():
    return render_template('home.html', survey = survey)

@app.route('/question/<int:idx>')
def show_question(idx):
    if idx > len(responses):
        flash("Do not divert from the path!")
        return redirect(f'/question/{len(responses)}')
    elif len(responses) == len(survey.questions):
        return redirect('/thank-you')
    else:
        idx=len(responses)
        return render_template('/question.html', question = survey.questions[idx])

@app.route('/answer', methods=["POST"])
def show_answer():
    answer = request.form["answer"]
    responses.append(answer)
    return redirect(f'/question/{len(responses)}')

@app.route(f'/question/{len(survey.questions)}')
def thank_you_redirect():
    return redirect('/thank-you')

@app.route('/thank-you')
def show_thank_you():
    return render_template('thank-you.html')