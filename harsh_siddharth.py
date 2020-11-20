import csv

import numpy as np
import pandas as pd
import sys
import json


# Function to read csv file given name in first cmd option
def read_file(file_name):
    data = pd.read_csv(file_name, delimiter=',')
    return data


def get_json_for_attempt_count(data, id_data):
    data.loc[:, 'attempt_count'] = np.where(data.loc[:, 'verdict'] != 'none',
                                            1, 0)
    level_columns = ['task_no', 'task_id']
    id_data.rename(columns={'task_no': 'task_names', 'id': 'task_id'},
                   inplace=True)
    data = pd.merge(id_data, data, on='task_id', how='inner')
    data[['task_no', 'task_id']] = data.task_names.str.split("-", expand=True)
    avg_data = data.groupby(['task_no', 'task_id']).agg(
        {'attempt_count': ['sum']})
    avg_data.columns = avg_data.columns.droplevel(1)
    avg_data = avg_data.reset_index()
    all_column = ['attempt_count']
    result = dict()
    for row in avg_data.itertuples():
        tmp_result = result
        for i in range(len(level_columns)):
            val = getattr(row, level_columns[i])
            if val not in tmp_result:
                tmp_result[val] = {}
            tmp_result = tmp_result[val]
        for column in all_column:
            if column not in level_columns:
                tmp_result[column] = getattr(row, column)
    return result


def get_json_for_fraction(src_dir):
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

        [num, _] = task_id_to_num[task_id].split('-')
        (cur_cnt, cur_cnt_ok) = result_by_task_num.get(num, (0, 0))
        result_by_task_num[num] = (cur_cnt + cnt, cur_cnt_ok + cnt_ok)

    data = {}
    for task_num, (cnt, cnt_ok) in result_by_task_num.items():
        fraction = cnt_ok / cnt if cnt != 0 else 0
        data[task_num] = round(fraction, 2)

    return data


# Write json to file
def write_json_to_file(json_data, file_name):
    file_object = open(file_name, "w+")
    json.dump(json_data, file_object, indent=4)


def compute_fraction_data(csv_file_dir, json_file_name):
    data = read_file(csv_file_dir + "/results.csv")
    json = get_json_for_fraction(csv_file_dir)
    final_json = {
        'title': 'Fraction of correct answers',
        'data_type': 'value_for_each_task_number',
        'render_type': 'color-gradient-asc',
        'data': json
    }
    write_json_to_file(final_json, json_file_name)


def compute_attempt_count_data(csv_file_dir, json_file_name):
    data = read_file(csv_file_dir + "/results.csv")
    ids = read_file(csv_file_dir + "/task_ids.csv")
    json = get_json_for_attempt_count(data, ids)
    jsonu = dict()
    for task in json:
        variants = json[task]
        for variant in variants:
            if task not in jsonu:
                jsonu[task] = dict()
            jsonu[task][variant] = json[task][variant]['attempt_count']
    final_json = {
        'title': 'Non-empty answers count',
        'data_type': 'value_for_each_task',
        'render_type': 'color-gradient-asc',
        'data': jsonu
    }
    write_json_to_file(final_json, json_file_name)


def make_fraction_for_task_block(src_dir, out_file_path):
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
        result_by_task_num[(num, variant)] = (cnt, cnt_ok)

    data = {}
    for (task_num, task_variant), (cnt, cnt_ok) in result_by_task_num.items():
        fraction = cnt_ok / cnt if cnt != 0 else 0

        if task_num not in data:
            data[task_num] = {}

        data[task_num][task_variant] = round(fraction, 2)

    json_result = {
        'title': 'Fraction of correct answers by task',
        'data_type': 'value_for_each_task',
        'render_type': 'color-gradient-asc',
        'data': data
    }
    with open(out_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)