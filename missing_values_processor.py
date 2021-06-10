from math import sqrt
from time import time
from random import uniform as random


ORIGINAL = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability.arff'
PROCESSED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_processed.arff'

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


def missing_valid_split(data: list) -> list:
    missing, valid = [], []
    for inst in data:
        if '?' in inst:
            missing.append(inst)
        else:
            valid.append(inst)
    return missing, valid


def euclidean_distance(x: list, y: list) -> float:
    if len(x) != len(y):
        return None

    distance = 0.0
    for att in range(len(x)):
        if x[att] != '?' and y[att] != '?':
            distance += pow((float(x[att]) - float(y[att])), 2)
    return sqrt(distance)


def nearest_neighbour(point: list, neighbours: list) -> list:
    distances = [euclidean_distance(point, neighbour) for neighbour in neighbours]
    nearest = min(distances)

    for idx, distance in enumerate(distances):
        if distance == nearest:
            return neighbours[idx]  # copy closest neighbour's values
    return None


def apply_noise(inst: list, percent: float) -> list:
    noisy_inst = inst[:-1]  # ignore class on noise application

    for attIdx, att in enumerate(noisy_inst):
        noise = float(att) * percent
        noisy_inst[attIdx] = str(float(att) + random(-noise, noise))
    noisy_inst.append(inst[-1])  # append class back to instance

    return noisy_inst


def replace_missing_nearest_noisy_valid(missing: list, valid: list) -> list:
    replaced = missing

    for idx, inst in enumerate(replaced):
        replaced[idx] = apply_noise(nearest_neighbour(inst, valid), NOISE)
    return replaced


def write_arff(path: str, headers: list, data: list) -> None:
    with open(path, 'w') as fp:
        for h in headers:
            fp.write(h + '\n')
        for inst in data:
            for attIdx, att in enumerate(inst):
                fp.write("%s," % att if attIdx + 1 < N_ATTRIBUTES else "%s\n" % att)


if __name__ == '__main__':
    begin = time()

    headers, data = read_arff(ORIGINAL)
    missing_values, valid_values = missing_valid_split(data)
    replaced_values = replace_missing_nearest_noisy_valid(missing_values, valid_values)
    write_arff(PROCESSED, headers, valid_values + replaced_values)

    print("Done in %s\n" % (time() - begin))
