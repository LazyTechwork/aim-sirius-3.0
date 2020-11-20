import csv

import pandas as pd
import random
import math
import json


def optimization(src_dir, out_file_path):
    data = pd.read_csv(src_dir + '/results.csv')
    partscor = pd.DataFrame()
    partscor['user num'] = data['session_id']
    partscor['points'] = data['score']
    uniq = list(set(partscor['user num']))
    nums = list(partscor['points'])
    uniq.sort()

    task_num_to_task_ids = {}

    with open(src_dir + '/task_ids.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            task_id = int(row['id'])
            key = int(row['task_no'].split("-")[0])

            if key not in task_num_to_task_ids:
                task_num_to_task_ids[key] = []

            task_num_to_task_ids[key].append(task_id)

    n = len(task_num_to_task_ids)
    peop = len(list(set(list(data['session_id']))))
    a = len(nums)
    pp = 25
    dif = [0.5] * n
    res = []
    c = 0.01  # step for changing difficulties
    dist = []
    it = 200  # iterations

    def f(p, num):
        n = math.ceil(len(
            num) * p / 100)  # we count how many participants should receive the diplomas
        # rint(n)
        new_all = num[:n + 1]
        # print(new_all)
        j = new_all[-1]
        while num[n + 1] == num[n]:
            n -= 1
        return n  # no of diplomas

    def g(p, dif, num):
        res = []
        for j in range(num):
            summ = 0
            student = []
            for i in range(n):
                o = round(random.uniform(0, 1), 3)
                if o < dif[i]:
                    student.append(0)
                else:
                    student.append(1)
                    summ += 1
            res.append(summ)
        res.sort(reverse=True)
        return f(p, res)

    def opt(difg):
        for i in range(1):
            for i in range(it):
                print(f'Optimal difficulties. Iteration {i + 1}/{it}', flush=True)
                l = 0
                c = 0.01
                # random.seed(i)
                ind = random.choice(range(0, n, 1))
                # random.seed()
                if difg[ind] >= 1 - c:
                    continue
                old_d = difg
                dif1, dif2 = difg.copy(), difg.copy()
                dif1[ind] = dif1[ind] + c
                dif2[ind] = abs(dif2[ind] - c)
                r1 = g(pp, dif1, peop)
                r2 = g(pp, dif2, peop)
                r0 = g(pp, dif, peop)

                if (r1 >= r2) and (r1 >= r0):
                    difg = dif1
                if (r2 >= r1) and (r2 >= r0):
                    difg = dif2
                else:
                    difg = difg

                if difg == old_d:
                    l += 1
                if (l >= 50) and (difg == old_d):
                    opt_dif = difg
                    break

            # dist.append(g(pp,difg,peop))
            # print(difg)
        return difg

    # return opt(dif)
    rr = {}
    res_opt = opt(dif)
    for i in range(n):
        rr[str(i + 1)] = round(res_opt[i], 2)

    json_result = {
        'title': 'Optimal difficulty for each task',
        'data_type': 'value_for_each_task_number',
        'render_type': 'color-gradient-asc',
        'data': rr
    }
    jj = json.dumps(json_result, indent=4)
    # print (jj)
    f = open(out_file_path, 'w')
    f.write(jj)
    # return jj