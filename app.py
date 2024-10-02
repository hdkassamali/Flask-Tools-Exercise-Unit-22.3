from flask import Flask, request, render_template, redirect, flash, jsonify, session

# from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)

app.config["SECRET_KEY"] = "chickenzarecool21837"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# debug = DebugToolbarExtension(app)

# Initialize empty responses list to store user answers.
# responses = []


@app.route("/")
def home_page():
    """Shows home page where a user can begin survey"""
    return render_template("home.html", survey=satisfaction_survey)


@app.route("/set-session", methods=["POST"])
def set_session():
    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<int:question_num>")
def question_form(question_num):
    """Shows each question in the survey, one at a time."""
    if question_num != len(session["responses"]):
        flash(
            "You are trying to access an invalid question!",
            "error",
        )

    question_num = len(session["responses"])

    if len(session["responses"]) >= len(satisfaction_survey.questions):
        return redirect("/thank-you")

    return render_template(
        "question_form.html",
        survey_question=satisfaction_survey.questions[question_num],
        question_num=question_num,
    )


@app.route("/answer", methods=["POST"])
def answer_to_questions():
    """Handles storing user answers in responses list. Redirects to the next question. If the user has answered all of the questions, then it redirects to the thank you page."""
    question_num = int(request.form["question_num"])
    user_answer = request.form["answer"]

    responses = session["responses"]
    responses.append(user_answer)
    session["responses"] = responses

    if question_num >= (len(satisfaction_survey.questions)):
        return redirect("/thank-you")

    return redirect(f"/questions/{question_num}")


@app.route("/thank-you")
def thank_you():
    """Simple thank you page to thank user for completing the survey."""
    return render_template("thank_you.html")
