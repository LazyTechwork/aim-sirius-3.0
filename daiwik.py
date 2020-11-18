import pandas as pd
import random
import json


def main_function(src_path, out_file_path):
    path_to_results = src_path + '/results.csv'
    path_to_ids = src_path + '/task_ids.csv'

    def check_varients(large, Lsum, small, Ssum):

        def generate_all_students(all_cnt, x):
            students = []
            for i in range(int(all_cnt * x)):
                students.append(1)
            for i in range(int(all_cnt * (1 - x))):
                students.append(0)
            return students

        success_rate1, participants_cnt1 = large, Lsum
        success_rate2, participants_cnt2 = small, Ssum

        success_rate_in_all_students = (
                                                   success_rate1 * participants_cnt1 + success_rate2 * participants_cnt2) / (
                                                   participants_cnt1 + participants_cnt2)

        all_students = generate_all_students(1000,
                                             success_rate_in_all_students)

        source_diff = abs(success_rate1 - success_rate2)

        repeats_cnt = 10000
        success_cnt = 0
        for i in range(repeats_cnt):
            random.shuffle(all_students)
            participants1 = all_students[:participants_cnt1]

            random.shuffle(all_students)
            participants2 = all_students[:participants_cnt2]

            diff = abs(sum(participants1) / len(participants1) - sum(
                participants2) / len(participants2))

            if diff >= source_diff:
                success_cnt += 1
        return round(success_cnt / repeats_cnt, 2)

    Ok = dict()
    Wrong = dict()
    Sum = dict()
    decimal = dict()
    data = pd.read_csv(path_to_results, index_col='verdict')
    data_taskid = pd.read_csv(path_to_ids)
    for i, row in data_taskid.iterrows():
        task_id = row['id']
        data1 = data[data.task_id == task_id]
        ok = len(data1.loc["ok"])
        wrong = len(data1.loc["wrong"])
        Ok[row['task_no']] = ok
        Wrong[row['task_no']] = wrong
        Sum[row['task_no']] = ok + wrong
        decimal[row['task_no']] = ok / (ok + wrong)

    task_to_varient = dict()
    for key in decimal:
        split = key.split("-")
        task_no = split[0]
        varient_no = split[1]
        if task_no in task_to_varient:
            task_to_varient[task_no].append(
                (varient_no, decimal[key], Sum[key]))
        else:
            task_to_varient[task_no] = [(varient_no, decimal[key], Sum[key])]
    # print(task_to_varient)
    data = dict()

    for task in task_to_varient:
        varients = task_to_varient[task]
        Marks = -1
        Varient_ = None
        for varient in varients:
            var = varient[1]
            if var > Marks:
                Marks = var
                Varient_ = varient
        Lsum = Varient_[2]
        min_Marks = 100
        min_varient_ = None
        for min_varient in varients:
            min_var = varient[1]
            if min_var < min_Marks:
                min_Marks = min_var
                min_varient_ = min_varient
        Ssum = min_varient_[2]
        prob = check_varients(Marks, Lsum, min_Marks, Ssum)
        if prob < 0.05:
            data[task] = 1
        else:
            data[task] = 0
    # print(data)

    json_result = {
        'title': 'Check In Data',
        'data_type': 'value_for_each_task_number',
        'render_type': 'color-gradient-asc',
        'data': data
    }
    with open(out_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)