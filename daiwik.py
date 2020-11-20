import csv

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

        all_students = generate_all_students(10000,
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

    task_id_to_cnt = {}
    task_id_to_ok_cnt = {}

    with open(src_path + '/results.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row['verdict'] == 'none':
                continue
            task_id = int(row['task_id'])
            cnt = task_id_to_cnt.get(task_id, 0)
            task_id_to_cnt[task_id] = cnt + 1
            if row['verdict'] == 'ok':
                cnt_ok = task_id_to_ok_cnt.get(task_id, 0)
                task_id_to_ok_cnt[task_id] = cnt_ok + 1

    task_id_to_num = {}
    with open(src_path + '/task_ids.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            task_id = int(row['id'])
            task_id_to_num[task_id] = row['task_no']

    task_to_varient = dict()
    for key in task_id_to_cnt:
        [task_no, varient_no] = task_id_to_num[key].split("-")
        ok_cnt = task_id_to_ok_cnt.get(key, 0)
        if task_no in task_to_varient:
            task_to_varient[task_no].append(
                (varient_no, ok_cnt / task_id_to_cnt[key],
                 task_id_to_cnt[key]))
        else:
            task_to_varient[task_no] = [(varient_no, ok_cnt /
                                         task_id_to_cnt[key],
                                         task_id_to_cnt[key])]
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
        print(f'Modelling {task}/{len(task_to_varient)}', flush=True)
        prob = check_varients(Marks, Lsum, min_Marks, Ssum)
        if prob < 0.05:
            data[task] = 1
        else:
            data[task] = 0
    print(data)

    json_result = {
        'title': 'Check In Data',
        'data_type': 'value_for_each_task_number',
        'render_type': 'color-gradient-asc',
        'data': data
    }
    with open(out_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)


def bad_tasks(src_dir, out_file_path):
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

        all_students = generate_all_students(10000,
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

    task_id_to_cnt = {}
    task_id_to_ok_cnt = {}
    with open(src_dir + '/results.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row['verdict'] == 'none':
                continue
            task_id = int(row['task_id'])
            cnt = task_id_to_cnt.get(task_id, 0)
            task_id_to_cnt[task_id] = cnt + 1
            if row['verdict'] == 'ok':
                cnt_ok = task_id_to_ok_cnt.get(task_id, 0)
                task_id_to_ok_cnt[task_id] = cnt_ok + 1

    task_id_to_num = {}
    with open(src_dir + '/task_ids.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            task_id = int(row['id'])
            task_id_to_num[task_id] = row['task_no']
    result_by_task_num = {}
    for task_id, cnt in task_id_to_cnt.items():
        cnt_ok = task_id_to_ok_cnt.get(task_id, 0)

        [num, variant] = task_id_to_num[task_id].split('-')
        (cur_cnt, cur_cnt_ok) = result_by_task_num.get(num, (0, 0))
        result_by_task_num[num] = (cur_cnt + cnt, cur_cnt_ok + cnt_ok)
    data = {}
    for task_num, (cnt, cnt_ok) in result_by_task_num.items():
        fraction = cnt_ok / cnt if cnt != 0 else 0
        data[task_num] = round(fraction, 2)

    result = dict()
    print(data)
    pre_value = -1
    for task in result_by_task_num:
        (cur_cnt, cur_cnt_ok) = result_by_task_num[task]
        min_fraction = cur_cnt_ok / cur_cnt
        min_task = task
        for task_ in result_by_task_num:
            if task_ == task:
                break
            if data[task_] < min_fraction:
                min_fraction = data[task_]
                min_task = task_
        large = cur_cnt_ok / cur_cnt
        Lsum = cur_cnt
        small = result_by_task_num[min_task][1] / result_by_task_num[min_task][
            0]
        Ssum = result_by_task_num[min_task][0]

        print(f'Modelling {task}/{len(result_by_task_num)}', flush=True)

        p = check_varients(large, Lsum, small, Ssum)
        print(p, task, min_task)

        if p < 0.05:
            result[task] = 1
        else:
            result[task] = 0

    json_result2 = {
        'title': 'Tasks with wrong difficulties',
        'data_type': 'value_for_each_task_number',
        'render_type': 'color-gradient-asc',
        'data': result
    }
    with open(out_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_result2, f, ensure_ascii=False, indent=4)
