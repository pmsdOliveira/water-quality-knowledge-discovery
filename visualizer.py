import plotly.express as px
import pandas as pd

NORMALIZED = 'C:\\Program Files\\Weka-3-8-5\\data\\water_potability_normalized.arff'

ATTRIBUTES = ['pH',
              'Hardness',
              'Solids',
              'Chloramines',
              'Sulfate',
              'Conductivity',
              'Organic_carbon',
              'Trihalomethanes',
              'Turbidity',
              'Potability'
              ]

HEATMAP_COLORS = ["#540b0e",
          "#9e2a2b",
          "#e09f3e",
          "#fff3b0",
          "#f7f3de"
          ]


def read_arff(path: str) -> list:
    data = []

    with open(path, 'r') as fp:
        lines = [line.rstrip('\n') for line in fp.readlines()]
        instances = lines[len(ATTRIBUTES) + 2:]
        for inst in instances:
            data.append([inst.split(',')[att] for att in range(len(ATTRIBUTES))])
    return data


if __name__ == '__main__':
    data = read_arff(NORMALIZED)
    df = pd.DataFrame(data, columns=ATTRIBUTES)
    correlation = df.astype(float).corr()
    fig = px.imshow(correlation, height=800, width=800, color_continuous_scale=HEATMAP_COLORS, template='plotly_white')
    fig.show()
