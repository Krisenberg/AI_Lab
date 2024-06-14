import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from collections import Counter
import os

CURRENT_FILE_PATH = Path(__file__).resolve().parent

def plot5Dcharts():
    filePath = os.path.join(CURRENT_FILE_PATH.parent, 'Data', 't-shirts.csv')
    data = pd.read_csv(filePath, sep=',')

    size_mapping = {'XS': 1, 'S': 2, 'M': 3, 'L': 4, 'XL': 5, 'XXL': 6, '3XL': 7}
    sleeves_mapping = {'short': 1, 'long': 2}
    demand_mapping = {'low': 1, 'medium': 2, 'high': 3}
    material_mapping = {material: idx for idx, material in enumerate(data['material'].unique())}
    color_mapping = {color: idx for idx, color in enumerate(data['color'].unique())}

    data['size_numeric'] = data['size'].map(size_mapping)
    data['sleeves_numeric'] = data['sleeves'].map(sleeves_mapping)
    data['demand_numeric'] = data['demand'].map(demand_mapping)
    data['material_numeric'] = data['material'].map(material_mapping)
    data['color_numeric'] = data['color'].map(color_mapping)

    demand_types = ['low', 'medium', 'high']

    cmap = plt.cm.get_cmap('viridis')

    for demand in demand_types:
        fig = plt.figure(figsize=(10, 8))
        fig.subplots_adjust(left=0.01, right=0.80, bottom=0.10, top=0.95)
        fig.suptitle(f'T-shirt demand ({demand} demand)', fontsize=12, y=0.98)

        subset = data[data['demand'] == demand]
        counts = Counter(zip(subset['color_numeric'], subset['sleeves_numeric'], subset['material_numeric']))

        ax = fig.add_subplot(111, projection='3d')

        xs, ys, zs, sizes, colors = [], [], [], [], []

        for (color, sleeves, material), count in counts.items():
            xs.append(color)
            ys.append(sleeves)
            zs.append(count)
            sizes.append(subset[subset['color_numeric'] == color]['size_numeric'].iloc[0] * 200)
            colors.append(material)

        sc = ax.scatter(xs, ys, zs, c=colors, cmap=cmap, alpha=0.6, edgecolors='w', s=sizes)

        ax.set_xlabel('Color', labelpad=20)
        ax.set_xticks(list(color_mapping.values()))
        ax.set_xticklabels(list(color_mapping.keys()), rotation=90)

        ax.set_ylabel('Sleeves', labelpad=10)
        ax.set_yticks([1, 2])
        ax.set_yticklabels(['short', 'long'])

        for tick in ax.get_yticklabels():
            tick.set_verticalalignment('center')
            tick.set_horizontalalignment('right')

        ax.set_zlabel('Count')

        ax.view_init(elev=33, azim=-53)

        cbar = fig.colorbar(sc, ax=ax, orientation='vertical', shrink=0.6, aspect=20, pad=0.1)  # Adjusted colorbar padding
        cbar.set_label('Material')
        cbar.set_ticks(list(material_mapping.values()))
        cbar.set_ticklabels(list(material_mapping.keys()))

        chartFilePath = os.path.join(CURRENT_FILE_PATH.parent, 'charts', 'eda', f'tshirt_demand_{demand}.png')
        if os.path.isfile(chartFilePath):
            os.remove(chartFilePath)
        plt.savefig(chartFilePath, dpi=300)
        plt.show()

if __name__ == '__main__':
    plot5Dcharts()
