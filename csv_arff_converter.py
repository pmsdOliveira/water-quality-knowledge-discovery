CSV = 'C:\\Users\\Utilizador\\Desktop\\data\\water_potability.csv'
ARFF = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability.arff'

RELATION = 'water_potability'
ATTRIBUTES = [
        "pH numeric",
        "Hardness numeric",
        "Solids numeric",
        "Chloramines numeric",
        "Sulfate numeric",
        "Conductivity numeric",
        "Organic_carbon numeric",
        "Trihalomethanes numeric",
        "Turbidity numeric",
        "Potability {0, 1}"
]


def missing_value(val: str) -> str:
    return val if len(val) > 0 else '?'


def read_csv(path: str) -> list:
    data = []
    with open(path, 'r') as fp:
        lines = [line.rstrip('\n').replace(';', ',') for line in fp.readlines()][1:]  # ignore csv column names
        for line in lines:
            data.append([missing_value(line.split(',')[attIdx]) for attIdx in range(len(ATTRIBUTES))])
    return data


def write_arff(path: str, data: list) -> None:
    with open(path, 'w') as fp:
        fp.write("@relation " + RELATION + '\n')

        for attribute in ATTRIBUTES:
            fp.write("@attribute %s\n" % attribute)

        fp.write('@data\n')
        for inst in data:
            for attIdx, att in enumerate(inst):
                fp.write("%s," % att if attIdx + 1 < len(ATTRIBUTES) else "%s\n" % att)


if __name__ == '__main__':
    data = read_csv(CSV)
    write_arff(ARFF, data)
