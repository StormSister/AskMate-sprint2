import database_common as db

def get_questions_sorted_by_date(cursor):
    query = """
        SELECT * FROM question ORDER BY submission_time DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

@db.connection_handler
def display_questions(cursor):
    return get_questions_sorted_by_date(cursor)

@db.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT * FROM question
        WHERE id = %(question_id)s;
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()

@db.connection_handler
def get_answers_for_question(cursor, question_id):
    query = """
        SELECT * FROM answer
        WHERE question_id = %(question_id)s;
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()

@db.connection_handler
def add_question(cursor, title, message):
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES (CURRENT_TIMESTAMP, 0, 0, %(title)s, %(message)s, '');
    """
    cursor.execute(query, {'title': title, 'message': message})
    return cursor.lastrowid

@db.connection_handler
def add_answer(cursor, question_id, message):
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (CURRENT_TIMESTAMP, 0, %(question_id)s, %(message)s, '');
    """
    cursor.execute(query, {'question_id': question_id, 'message': message})
    return cursor.lastrowid

@db.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question WHERE id = %(question_id)s;
    """
    cursor.execute(query, {'question_id': question_id})

@db.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE FROM answer WHERE id = %(answer_id)s;
    """
    cursor.execute(query, {'answer_id': answer_id})

@db.connection_handler
def edit_question(cursor, question_id, title, message):
    query = """
        UPDATE question
        SET title = %(title)s, message = %(message)s
        WHERE id = %(question_id)s;
    """
    cursor.execute(query, {'title': title, 'message': message, 'question_id': question_id})

@db.connection_handler
def vote_question(cursor, question_id, vote_type):
    query = """
        UPDATE question
        SET vote_number = vote_number + %(vote_value)s
        WHERE id = %(question_id)s;
    """
    vote_value = 1 if vote_type == 'up' else -1
    cursor.execute(query, {'vote_value': vote_value, 'question_id': question_id})

@db.connection_handler
def update_question_views(cursor, question_id, updated_views):
    query = """
        UPDATE question
        SET view_number = %(updated_views)s
        WHERE id = %(question_id)s;
    """
    cursor.execute(query, {'updated_views': updated_views, 'question_id': question_id})

@db.connection_handler
def get_all_questions_ordered(cursor, order_by, order_direction):
    query = f"""
        SELECT * FROM question
        ORDER BY {order_by} {order_direction}
    """
    cursor.execute(query)
    return cursor.fetchall()



# @db.connection_handler
# def search_results(cursor, search_phrase):
#     query = f"""
#         SELECT * FROM question
#         WHERE title ILIKE '%%{search_phrase}%%'
#         OR message ILIKE '%%{search_phrase}%%'
#     """
#     cursor.execute(query)
#     return cursor.fetchall()


@db.connection_handler
def get_latest_questions(cursor, number):
    query = f"""
        SELECT * FROM question
        ORDER BY submission_time DESC
        LIMIT %(number)s
    """
    cursor.execute(query, {'number': number})
    return cursor.fetchall()


def highlight_phrase(text, search_phrase):
    return text.replace(search_phrase, f'<mark>{search_phrase}</mark>')


@db.connection_handler
def search_results(cursor, search_phrase):
    query = f"""
        SELECT DISTINCT question.* FROM question
        LEFT JOIN answer ON question.id = answer.question_id
        WHERE question.title ILIKE '%%{search_phrase}%%'
        OR question.message ILIKE '%%{search_phrase}%%'
        OR answer.message ILIKE '%%{search_phrase}%%'
    """
    cursor.execute(query)
    return cursor.fetchall()

