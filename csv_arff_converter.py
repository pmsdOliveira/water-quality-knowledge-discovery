def checkMissingValue(val: str) -> str:
    return val if len(val) > 0 else '?'

def processField(idx: int, data: list) -> list:
    return [checkMissingValue(line.split(',')[idx]) for line in data]

if __name__ == '__main__':
    csv_path = 'C:\\Users\\Utilizador\\Desktop\\data\\water_potability.csv'
    arff_path = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability.arff'

    relation = "water_potability"
    attributes = [
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
    data = []

    with open(csv_path, 'r') as fp:
        lines = [line.rstrip('\n').replace(';', ',') for line in fp.readlines()][1:]
        for idx in range(len(attributes)):
            data.append(processField(idx, lines))

    with open(arff_path, 'w') as fp:
        fp.write("@relation " + relation + '\n')

        for attribute in attributes:
            fp.write("@attribute %s\n" % attribute)

        fp.write('@data\n')
        for idx in range(len(data[0])):
            for att in range(len(data)):
                fp.write("%s," % data[att][idx] if att + 1 < len(data) else "%s\n" % data[att][idx])
