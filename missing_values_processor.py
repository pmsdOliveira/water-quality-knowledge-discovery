from math import sqrt
from time import time
from random import uniform as random


ORIGINAL = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability.arff'
PROCESSED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_processed.arff'

N_ATTRIBUTES = 10
NOISE = 0.05


# O(1)
def has_missing(inst: list) -> list:
    return True if '?' in inst else False


# O(n)
def missing_valid_split(data: list) -> list:
    missing, valid = [], []
    for inst in data:
        if has_missing(inst):
            missing.append(inst)
        else:
            valid.append(inst)
    return missing, valid


# O(n)
def euclidian_distance(x: list, y: list) -> float:
    if len(x) != len(y):
        return None

    distance = 0.0
    for att in range(len(x)):
        if x[att] != '?' and y[att] != '?':
            distance += pow((float(x[att]) - float(y[att])), 2)

    return sqrt(distance)

# O(n)
def apply_noise(inst: list) -> list:
    noisy_inst = inst[:-1] # ignore class
    for attIdx, att in enumerate(noisy_inst):
        noise = float(att) * NOISE
        noisy_inst[attIdx] = str(float(att) + random(-noise, noise))
    noisy_inst.append(inst[-1])
    return noisy_inst


# O(n^2)
def nearest_neighbour(point: list, neighbours: list) -> list:
    distances = [euclidian_distance(point, neighbour) for neighbour in neighbours]
    nearest = min(distances)

    for idx, distance in enumerate(distances):
        if distance == nearest:
            return apply_noise(neighbours[idx])
    return None


if __name__ == '__main__':
    begin = time()

    data = []
    with open(ORIGINAL, 'r') as fp:
        lines = [line.rstrip('\n') for line in fp.readlines()]
        headers = lines[:N_ATTRIBUTES + 2]
        instances = lines[N_ATTRIBUTES + 2:]
        for inst in instances:
            data.append([inst.split(',')[att] for att in range(N_ATTRIBUTES)])

    missing, valids = missing_valid_split(data)

    for idx, inst in enumerate(missing):
        missing[idx] = nearest_neighbour(inst, valids)

    with open(PROCESSED, 'w') as fp:
        for h in headers:
            fp.write(h + '\n')
        for v in valids:
            for attIdx, att in enumerate(v):
                fp.write("%s," % att if attIdx + 1 < N_ATTRIBUTES else "%s\n" % att)
        for m in missing:
            for attIdx, att in enumerate(m):
                fp.write("%s," % att if attIdx + 1 < N_ATTRIBUTES else "%s\n" % att)

    print("Done in %s\n" % (time() - begin))
