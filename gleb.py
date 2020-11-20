import csv
from functools import reduce


def getOlympiadScores(inputPath, outputPath):
    import pandas as pd
    import json
    df = pd.read_csv(inputPath + '/results.csv')
    del df['users_answer']
    del df['submission_time']
    del df['verdict']
    df['score'] = df['score'].fillna(0)
    df = df.dropna()
    import numpy as np
    import random
    actwinners10 = int(len(pd.unique(df['session_id'])) * 0.10)
    actprizers15 = int(len(pd.unique(df['session_id'])) * 0.15)

    task_num_to_task_ids = {}
    task_id_to_task_num = {}

    with open(inputPath + '/task_ids.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            task_id = int(row['id'])
            key = int(row['task_no'].split("-")[0])

            if key not in task_num_to_task_ids:
                task_num_to_task_ids[key] = []

            task_num_to_task_ids[key].append(task_id)
            task_id_to_task_num[task_id] = key

    def mape(actual, pred):
        actual, pred = np.array(actual), np.array(pred)
        return np.mean(np.abs((actual - pred) / actual)) * 100

    diff = []
    for task_num in task_num_to_task_ids:
        match = [df.loc[df['task_id'] == x] for x in task_num_to_task_ids[task_num]]
        task1 = reduce(lambda x, y: x + y, match)
        diff.append([task_num, mape(task1['max_score'], task1['score'])])
        # nummaxmape[0].append(i)
        # nummaxmape[1].append(mape(task1['max_score'], task1['score']))

    diff.sort(key=lambda x: x[1])
    for i in range(len(diff)):
        diff[i][1] = i + 1
    basicd = []
    for i in range(len(diff)):
        basicd.append(diff[i][0])
    print(basicd)
    diff.sort()
    print(diff)

    scores = df[['session_id', 'task_id', 'score', 'max_score']]
    users = scores.groupby('session_id')
    users.head()

    multiplier = 0.25

    def f(sc):
        nummaxmape = sc
        scores = []
        for ids, data in users:
            data = data.to_numpy()
            total = 0.0

            for i in range(len(data)):
                total += data[i][2] / data[i][3] * nummaxmape[task_id_to_task_num[data[i][1]] - 1][1]
            scores.append([ids, total])

        scores.sort(key=lambda x: x[1])
        scores.reverse()
        scores = np.around(scores)
        scores = scores.astype(int)
        df = pd.DataFrame(data=scores, columns=["session_id", "score"])
        x = 10
        y = 25
        x = df['score'].quantile((100 - x) / 100)
        rowswin = df.loc[df['score'] > x]
        rowswin = rowswin.shape[0]

        y = df['score'].quantile((100 - y) / 100)
        rowsprize = df.loc[(df['score'] < x) & (df['score'] > y)]
        rowsprize = rowsprize.shape[0]

        combin = int(rowswin - (np.sum(sc, axis=0)[1] * multiplier)) + int(
            rowsprize)
        # (rowswin - (np.sum(sc, axis=0)[1]*multiplier) + (rowsp*0.1)

        return rowswin, rowsprize, combin

    maxw, maxp, maximum = f(diff)

    basic = diff.copy()

    i = 0

    while i < 30:
        randomtask = random.choice(basic)
        a = int(random.random())
        if a == 1:
            randomtask[1] += 1
        elif randomtask[1] > 1:
            randomtask[1] -= 1
        check = basic.copy()
        check[randomtask[0] - 1][1] = randomtask[1]

        if basicd.index(randomtask[0]) != (len(basicd) - 1) and basicd.index(
                randomtask[0]) != 0 and check[randomtask[0] - 1][1] <= \
                check[basicd[basicd.index(randomtask[0]) + 1] - 1][1] and \
                check[randomtask[0] - 1][1] >= \
                check[basicd[basicd.index(randomtask[0]) - 1] - 1][1]:
            reswin, resprize, res = f(check)
            if res > maximum:
                maximum = res
                basic = check.copy()
                maxw = reswin
                maxp = resprize
                print(maximum)
                print(basic)
                i = 0
        elif basicd.index(randomtask[0]) == (len(basicd) - 1) and \
                check[randomtask[0] - 1][1] >= \
                check[basicd[basicd.index(randomtask[0]) - 1] - 1][1]:
            reswin, resprize, res = f(check)
            if res > maximum:
                maximum = res
                basic = check.copy()
                maxw = reswin
                maxp = resprize
                print(maximum)
                print(basic)
                i = 0
        elif basicd.index(randomtask[0]) == 0 and check[randomtask[0] - 1][
            1] <= check[basicd[basicd.index(randomtask[0]) + 1] - 1][1]:
            reswin, resprize, res = f(check)
            if res > maximum:
                maximum = res
                basic = check.copy()
                maxw = reswin
                maxp = resprize
                print(maximum)
                print(basic)
                i = 0
        i += 1

    print(maximum)
    print(basic)
    print(maxw, 'winners')
    print(maxp, 'prizegetters')

    output2 = {}

    output2['10% winners'] = maxw

    output2['real 10%'] = actwinners10

    output2['15% prizers'] = maxp

    output2['real 15%'] = actprizers15

    output2
    json_result2 = {'title': 'actual25_optimal25',
                    'data_type': 'text_to_value',
                    'render_type': 'color-gradient-asc',
                    'data': output2}
    with open(outputPath + 'act_opt.json', 'w', encoding='utf-8') as f:
        json.dump(json_result2, f, ensure_ascii=False, indent=4)

    output = {}
    for i in basic:
        output[str(i[0])] = i[1]
    json_result = {'title': 'best_scores_for_tasks',
                   'data_type': 'value_for_each_task_number',
                   'render_type': 'color-gradient-asc',
                   'data': output}
    print(json_result)
    with open(outputPath + 'scores.json', 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)
