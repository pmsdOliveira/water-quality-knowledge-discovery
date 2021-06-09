from random import uniform as random
from random import randint


PROCESSED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_processed.arff'
BALANCED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_balanced.arff'

N_ATTRIBUTES = 10
NOISE = 0.05


def yes_no_split(data: list) -> (list, list):
    yes, no = [], []
    for inst in data:
        if inst[-1] == '1':
            yes.append(inst)
        else:
            no.append(inst)
    return yes, no


def apply_noise(inst: list) -> list:
    noisy_inst = inst[:-1] # ignore class
    for attIdx, att in enumerate(noisy_inst):
        noise = float(att) * NOISE
        noisy_inst[attIdx] = str(float(att) + random(-noise, noise))
    noisy_inst.append(inst[-1])
    return noisy_inst


def balance_classes(data: list, diff: int) -> list:
    idxs = [randint(0, len(data)) for _ in range(diff)]
    return [apply_noise(data[i]) for i in idxs]


if __name__ == '__main__':
    data = []

    with open(PROCESSED, 'r') as fp:
        lines = [line.rstrip('\n') for line in fp.readlines()]
        headers = lines[:N_ATTRIBUTES + 2]
        instances = lines[N_ATTRIBUTES + 2:]
        for inst in instances:
            data.append([inst.split(',')[att] for att in range(N_ATTRIBUTES)])

    yes, no = yes_no_split(data)
    diff = abs(len(yes) - len(no))

    new_insts = balance_classes(yes, diff)
    for inst in new_insts:
        yes.append(inst)

    with open(BALANCED, 'w') as fp:
        for h in headers:
            fp.write(h + '\n')
        for y in yes:
            for attIdx, att in enumerate(y):
                fp.write("%s," % att if attIdx + 1 < N_ATTRIBUTES else "%s\n" % att)
        for n in no:
            for attIdx, att in enumerate(n):
                fp.write("%s," % att if attIdx + 1 < N_ATTRIBUTES else "%s\n" % att)
