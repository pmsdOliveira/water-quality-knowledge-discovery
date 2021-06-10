BALANCED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_balanced.arff'
NORMALIZED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_normalized.arff'

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


def min_max_attributes(data: list) -> (float, float):
    mins, maxs = [], []
    for attIdx in range(N_ATTRIBUTES - 1):
        values = [float(inst[attIdx]) for inst in data]
        mins.append(min(values))
        maxs.append(max(values))
    return mins, maxs


def normalize(data: list) -> list:
    normalized_data = data
    mins, maxs = min_max_attributes(data)

    for instIdx, inst in enumerate(data):
        for attIdx, att in enumerate(inst[:-1]):
            val = str((float(att) - mins[attIdx]) / (maxs[attIdx] - mins[attIdx]))
            normalized_data[instIdx][attIdx] = val
    return normalized_data


def write_arff(path: str, headers: list, data: list) -> None:
    with open(path, 'w') as fp:
        for h in headers:
            fp.write(h + '\n')
        for inst in data:
            for attIdx, att in enumerate(inst):
                fp.write("%s," % att if attIdx + 1 < N_ATTRIBUTES else "%s\n" % att)


if __name__ == '__main__':
    headers, data = read_arff(BALANCED)
    normalized_data = normalize(data)
    write_arff(NORMALIZED, headers, normalized_data)
