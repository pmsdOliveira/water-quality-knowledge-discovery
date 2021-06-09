import plotly.express as px
import pandas as pd


NORMALIZED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_normalized.arff'

N_ATTRIBUTES = 10
NOISE = 0.05


def min_max_attributes(data: list) -> (float, float):
    mins, maxs = [], []
    for attIdx in range(N_ATTRIBUTES - 1):
        values = [float(inst[attIdx]) for inst in data]
        mins.append(min(values))
        maxs.append(max(values))
    return mins, maxs


def normalize(data: list) -> list:
    mins, maxs = min_max_attributes(data)

    normalized_data = data
    for instIdx, inst in enumerate(data):
        for attIdx, att in enumerate(inst[:-1]):
            val = str((float(att) - mins[attIdx]) / (maxs[attIdx] - mins[attIdx]))
            normalized_data[instIdx][attIdx] = val
    return normalized_data


if __name__ == '__main__':
    data = []

    with open(NORMALIZED, 'r') as fp:
        lines = [line.rstrip('\n') for line in fp.readlines()]
        headers = lines[:N_ATTRIBUTES + 2]
        instances = lines[N_ATTRIBUTES + 2:]
        for inst in instances:
            data.append([inst.split(',')[att] for att in range(N_ATTRIBUTES)])

    df = pd.DataFrame(data, columns=['pH', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity',
                                     'Organic_carbon', 'Trihalomethanes', 'Turbidity', 'Potability'])

    colors = ["#f7f3de", "#fff3b0", "#e09f3e", "#9e2a2b", "#540b0e"][::-1]
    correlation = df.astype(float).corr()
    print(correlation)
    fig = px.imshow(correlation, height=800, width=800, color_continuous_scale=colors, template='plotly_white')
    fig.show()
