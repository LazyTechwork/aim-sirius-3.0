import json

import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Produce basic olympiad analysis')
parser.add_argument('--results', dest='results', action='store',
                    help='Results file', required=True)
parser.add_argument('--tasks', dest='task_ids', action='store',
                    help='File with task ids', required=True)
args = parser.parse_args()

results = pd.read_csv(args.results)
results.set_index('id')
tasks = pd.read_csv(args.task_ids)
tasks.set_index('id')

results = results.groupby(["task_id", "verdict"])["verdict"].count()
results = pd.DataFrame(results)
output = []
js = {}
for idx, data in results.groupby(level=0):
    v = data.get('verdict').values
    output.append({
        'task_id': idx,
        'none': int(v[0]),
        'ok': int(v[1]),
        'wrong': int(v[2])
    })

for data in output:
    task, variant = tasks[tasks.id == data['task_id']].get('task_no').values[0].split('-')
    data['task'], data['variant'] = task, variant
    frac = round(data['ok'] / (data['none'] + data['ok'] + data['wrong']), 2)
    if not task in js:
        js[task] = {variant: frac}
    else:
        js[task][variant] = frac

with open('test.json', 'w+') as file:
    json.dump({'task_difficulty': js, 'subject': 'Mathematics'}, file)
