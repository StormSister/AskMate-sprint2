import connection as conn
import os
import util
import datetime
questions_file = os.path.join('sample_data', 'question.csv')
answers_file = os.path.join('sample_data', 'answer.csv')


def get_data(file_name):
    return conn.read_csv(file_name)


def get_questions_sorted_by_date(questions_file):
    questions = get_data(questions_file)
    questions.sort(key=lambda x: int(x['submission_time']), reverse=True)

    return questions


def display_questions():
    questions = get_questions_sorted_by_date(questions_file)
    for question in questions:
        question["submission_time"] = util.format_submission_time(question["submission_time"])
        question["id"] = int(question["id"])
    return questions


def get_question_by_id(question_id):
    questions = conn.read_csv(questions_file)
    for question in questions:
        if int(question["id"]) == question_id:
            return question


def get_answers_for_question(question_id):

    answers = []
    all_answers = get_data(answers_file)
    for answer in all_answers:
        if answer['question_id'] == str(question_id):
            answers.append(answer)
    return answers


def add_question(title, message):
    questions = get_data(questions_file)
    new_id = str(len(questions) + 1)
    current_timestamp = util.get_current_timestamp()
    new_question = {
        'id': new_id,
        'submission_time': current_timestamp,
        'view_number': '0',
        'vote_number': '0',
        'title': title,
        'message': message,
        'image': ''
    }
    questions.append(new_question)
    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    conn.write_csv(questions_file, questions, fieldnames)
    return new_id

def add_answer(question_id, message):
    answers = get_data(answers_file)
    new_id = str(len(answers)+1)
    current_timestamp = util.get_current_timestamp()
    new_answer = {
        'id': new_id,
        'submission_time': current_timestamp,
        'vote_number': 0,
        'question_id': int(question_id),
        'message': message,
        'image': ''
    }
    answers.append(new_answer)
    fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
    conn.write_csv(answers_file, answers, fieldnames)
    return new_id


def sort_questions(questions, order_by, order_direction):
    if order_by == 'title':
        questions.sort(key=lambda x: x['title'])
    elif order_by == 'submission_time':
        questions.sort(key=lambda x: datetime.datetime.strptime(x['submission_time'], '%Y-%m-%d %H:%M:%S'))
    elif order_by == 'message':
        questions.sort(key=lambda x: x['message'])
    elif order_by == 'number_of_views':
        questions.sort(key=lambda x: int(x['number_of_views']))
    elif order_by == 'number_of_votes':
        questions.sort(key=lambda x: int(x['number_of_votes']))

    if order_direction == 'desc':
        questions.reverse()
    return questions


def delete_question(question_id):
    questions = get_data(questions_file)
    updated_questions = [question for question in questions if question['id'] != str(question_id)]
    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    conn.write_csv(questions_file, updated_questions, fieldnames)


def delete_answer(answer_id):
    answers = get_data(answers_file)
    deleted_answer = None
    for answer in answers:
        if answer['id'] == str(answer_id):
            question_id = answer['question_id']
            deleted_answer = answer
            break
    updated_answers = [answer for answer in answers if answer['id'] != str(answer_id)]
    fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
    conn.write_csv(answers_file, updated_answers, fieldnames)

    return deleted_answer, question_id


def edit_question(question_id, title, message):
    questions = get_data(questions_file)
    for question in questions:
        if question['id'] == str(question_id):
            question['title'] = title
            question['message'] = message
            break

    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    conn.write_csv(questions_file, questions, fieldnames)


def vote_question(question_id, vote_type):
    questions = get_data(questions_file)
    for question in questions:
        if question['id'] == str(question_id):
            if vote_type == 'up':
                question['vote_number'] = str(int(question['vote_number']) + 1)
            elif vote_type == 'down':
                question['vote_number'] = str(int(question['vote_number']) - 1)
            break
    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    conn.write_csv(questions_file, questions, fieldnames)


def update_question_views(question_id, updated_views):
    questions = get_data(questions_file)
    for question in questions:
        if question['id'] == str(question_id):
            question['view_number'] = str(updated_views)
            break

    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    conn.write_csv(questions_file, questions, fieldnames)



#print(get_questions(question_file))
#print(get_question_by_id(question_file, "3"))
#add_question("Help with dicts", "Please help me to create my first dict")
#print(get_questions(question_file))
#print(get_questions_sorted_by_date(question_file))
# print(get_answers_for_question(1))
# print(get_question_by_id(1))