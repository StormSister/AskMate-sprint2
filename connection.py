import csv


def read_csv(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def append_csv(file_path, data, fieldnames):
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(data)


#print(read_csv("sample_data/question.csv"))