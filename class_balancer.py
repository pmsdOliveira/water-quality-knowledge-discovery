from random import uniform as random
from random import randint


PROCESSED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_processed.arff'
BALANCED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_balanced.arff'

N_ATTRIBUTES = 10
NOISE = 0.05


def read_arff(path: str) -> (list, list):
    headers, data = [], []

    with open(path, 'r') as fp:
        lines = [line.rstrip('\n') for line in fp.readlines()]
        headers = lines[:N_ATTRIBUTES + 2]
        instances = lines[N_ATTRIBUTES + 2:]
        for inst in instances:
            data.append([inst.split(',')[att] for att in range(N_ATTRIBUTES)])
    return headers, data


def yes_no_split(data: list) -> (list, list):
    yes, no = [], []
    for inst in data:
        if inst[-1] == '1':
            yes.append(inst)
        else:
            no.append(inst)
    return yes, no


def apply_noise(inst: list, percent: float) -> list:
    noisy_inst = inst[:-1]  # ignore class on noise application

    for attIdx, att in enumerate(noisy_inst):
        noise = float(att) * percent
        noisy_inst[attIdx] = str(float(att) + random(-noise, noise))
    noisy_inst.append(inst[-1])  # append class back to instance

    return noisy_inst


def create_missing_instances(data: list, n: int) -> list:
    idxs = [randint(0, len(data)) for _ in range(n)]
    return [apply_noise(data[idx], NOISE) for idx in idxs]


def write_arff(path: str, headers: list, data: list) -> None:
    with open(path, 'w') as fp:
        for h in headers:
            fp.write(h + '\n')
        for inst in data:
            for attIdx, att in enumerate(inst):
                fp.write("%s," % att if attIdx + 1 < N_ATTRIBUTES else "%s\n" % att)


if __name__ == '__main__':
    headers, data = read_arff(PROCESSED)
    yes, no = yes_no_split(data)
    diff = abs(len(yes) - len(no))

    new_insts = create_missing_instances(yes, diff)
    for inst in new_insts:
        yes.append(inst)  # appending to "yes" because it had less instances than "no"

    write_arff(BALANCED, headers, yes + no)
