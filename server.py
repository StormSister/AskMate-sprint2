from flask import Flask, render_template, request, url_for, redirect
import data_manager as dm

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    latest_questions = dm.get_latest_questions(5)
    return render_template('index.html',latest_questions=latest_questions)


@app.route("/list", methods=['GET'])
def list_questions():
    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'desc')
    questions = dm.get_all_questions_ordered(order_by, order_direction)
    return render_template('list.html', questions=questions)


@app.route('/question/<int:question_id>')
def display_question(question_id):
    question = dm.get_question_by_id(question_id)
    dm.update_question_views(question_id, question['view_number'] + 1)
    answers = dm.get_answers_for_question(question_id)
    return render_template('question.html', question=question, answers=answers, question_id=question_id)


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        new_question_id = dm.add_question(title, message)
        return redirect(url_for('display_question', question_id=new_question_id))


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template('new_answer.html', question_id=question_id)
    elif request.method == 'POST':
        message = request.form.get('message')
        dm.add_answer(question_id, message)
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/delete", methods=["POST"])
def delete_question(question_id):
    dm.delete_question(question_id)
    return redirect(url_for('list_questions'))


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'GET':
        question = dm.get_question_by_id(question_id)
        return render_template('edit_question.html', question=question)
    elif request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        dm.edit_question(question_id, title, message)
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/answer/<int:answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    deleted_answer, question_id = dm.delete_answer(answer_id)
    if question_id is not None:
        return redirect(url_for('display_question', question_id=question_id))
    else:
        return "Error: Question ID not found"


@app.route('/question/<int:question_id>/vote-up', methods=['POST'])
def vote_up(question_id):
    dm.vote_question(question_id, 'up')
    return redirect(url_for('list_questions'))


@app.route('/question/<int:question_id>/vote-down', methods=['POST'])
def vote_down(question_id):
    dm.vote_question(question_id, 'down')
    return redirect(url_for('list_questions'))


@app.route('/search_results')
def search_results():
    search_phrase = request.args.get('q')
    results = dm.search_results(search_phrase)  # Wywołanie funkcji wyszukującej
    return render_template('search_results.html', search_phrase=search_phrase, results=results)

# @app.template_filter('highlight')
# def highlight(text, search_phrase):
#     return text.replace(search_phrase, f'<mark>{search_phrase}</mark>')


if __name__ == "__main__":
    app.run(debug=True)
