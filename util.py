from datetime import datetime


def get_current_timestamp():
    current_time = datetime.now()
    return int(current_time.timestamp())


def format_submission_time(epoch_time):
    formatted_time = datetime.fromtimestamp(int(epoch_time)).strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time