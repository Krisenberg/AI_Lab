import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from collections import Counter
import os

CURRENT_FILE_PATH = Path(__file__).resolve().parent

# def plot5Dcharts():
#     filePath = os.path.join(CURRENT_FILE_PATH.parent, 'Data', 't-shirts.csv')
#     data = pd.read_csv(filePath, sep=',')

#     # Mapping attributes to numerical values
#     size_mapping = {'XS': 1, 'S': 2, 'M': 3, 'L': 4, 'XL': 5, 'XXL': 6, '3XL': 7}
#     sleeves_mapping = {'short': 1, 'long': 2}
#     demand_mapping = {'low': 1, 'medium': 2, 'high': 3}
#     material_mapping = {material: idx for idx, material in enumerate(data['material'].unique())}
#     color_mapping = {color: idx for idx, color in enumerate(data['color'].unique())}

#     data['size_numeric'] = data['size'].map(size_mapping)
#     data['sleeves_numeric'] = data['sleeves'].map(sleeves_mapping)
#     data['demand_numeric'] = data['demand'].map(demand_mapping)
#     data['material_numeric'] = data['material'].map(material_mapping)
#     data['color_numeric'] = data['color'].map(color_mapping)

#     demand_types = ['low', 'medium', 'high']

#     for demand in demand_types:
#         subset = data[data['demand'] == demand]

#         counts = Counter(zip(subset['color_numeric'], subset['sleeves_numeric'], subset['material_numeric']))

#         fig = plt.figure(figsize=(10, 10))
#         fig.subplots_adjust(left=0.01, right=0.9, bottom=0.05, top=0.95)
#         ax = fig.add_subplot(111, projection='3d')
#         fig.suptitle(f'T-shirt demand ({demand} demand)', fontsize=12, y=0.9)

#         xs, ys, zs, sizes, colors = [], [], [], [], []

#         for (color, sleeves, material), count in counts.items():
#             xs.append(color)
#             ys.append(sleeves)
#             zs.append(count)
#             sizes.append(subset[subset['color_numeric'] == color]['size_numeric'].iloc[0] * 200)
#             colors.append(material)

#         cmap = plt.cm.get_cmap('viridis', len(material_mapping))
#         sc = ax.scatter(xs, ys, zs, c=colors, cmap=cmap, alpha=0.6, edgecolors='w', s=sizes)

#         cbar = plt.colorbar(sc)
#         cax = cbar.ax
#         cax_pos = cax.get_position()
#         cax.set_position([cax_pos.x0+0.1, cax_pos.y0+0.1, cax_pos.width * 0.6, cax_pos.height * 0.6])

#         ax.set_xlabel('Color')
#         ax.set_xticks(list(color_mapping.values()))
#         ax.set_xticklabels(list(color_mapping.keys()))

#         ax.set_ylabel('Sleeves')
#         ax.set_yticks([1, 2])
#         ax.set_yticklabels(['short', 'long'])

#         for tick in ax.get_yticklabels():
#             tick.set_verticalalignment('center')
#             tick.set_horizontalalignment('right')

#         ax.set_zlabel('Count')

#         cbar.set_label('Material')
#         cbar.set_ticks(list(material_mapping.values()))
#         cbar.set_ticklabels(list(material_mapping.keys()))

#         chartFilePath = os.path.join(CURRENT_FILE_PATH.parent, 'Charts', f'tshirt_demand_{demand}.png')
#         if os.path.isfile(chartFilePath):
#             os.remove(chartFilePath)

#         plt.savefig(chartFilePath, dpi=300)
#         plt.show()

def plot5Dcharts():
    filePath = os.path.join(CURRENT_FILE_PATH.parent, 'Data', 't-shirts.csv')
    data = pd.read_csv(filePath, sep=',')

    # Mapping attributes to numerical values
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

    fig = plt.figure(figsize=(14, 12))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1])
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.3, hspace=0.4)
    fig.suptitle('T-shirt demand based on the attributes', fontsize=16, y=0.98)

    cmap = plt.colormaps['viridis']

    # Plot top two charts
    for i, demand in enumerate(demand_types[:2]):
        subset = data[data['demand'] == demand]
        if subset.empty:
            continue

        counts = Counter(zip(subset['color_numeric'], subset['sleeves_numeric'], subset['material_numeric']))

        ax = fig.add_subplot(gs[0, i], projection='3d')
        ax.set_title(f'Demand: {demand}', fontsize=12, y=1.0)

        xs, ys, zs, sizes, colors = [], [], [], [], []

        for (color, sleeves, material), count in counts.items():
            xs.append(color)
            ys.append(sleeves)
            zs.append(count)
            sizes.append(subset[subset['color_numeric'] == color]['size_numeric'].iloc[0] * 200)
            colors.append(material)

        sc = ax.scatter(xs, ys, zs, c=colors, cmap=cmap, alpha=0.6, edgecolors='w', s=sizes)

        ax.set_xlabel('Color')
        ax.set_xticks(list(color_mapping.values()))
        ax.set_xticklabels(list(color_mapping.keys()), rotation=90)

        ax.set_ylabel('Sleeves')
        ax.set_yticks([1, 2])
        ax.set_yticklabels(['short', 'long'])

        for tick in ax.get_yticklabels():
            tick.set_verticalalignment('center')
            tick.set_horizontalalignment('right')

        ax.set_zlabel('Count')

    # Plot bottom chart
    demand = demand_types[2]
    subset = data[data['demand'] == demand]
    if not subset.empty:
        counts = Counter(zip(subset['color_numeric'], subset['sleeves_numeric'], subset['material_numeric']))

        ax = fig.add_subplot(gs[1, :], projection='3d')
        ax.set_title(f'Demand: {demand}', fontsize=12, y=1.0)

        xs, ys, zs, sizes, colors = [], [], [], [], []

        for (color, sleeves, material), count in counts.items():
            xs.append(color)
            ys.append(sleeves)
            zs.append(count)
            sizes.append(subset[subset['color_numeric'] == color]['size_numeric'].iloc[0] * 200)
            colors.append(material)

        sc = ax.scatter(xs, ys, zs, c=colors, cmap=cmap, alpha=0.6, edgecolors='w', s=sizes)

        ax.set_xlabel('Color')
        ax.set_xticks(list(color_mapping.values()))
        ax.set_xticklabels(list(color_mapping.keys()), rotation=90)

        ax.set_ylabel('Sleeves')
        ax.set_yticks([1, 2])
        ax.set_yticklabels(['short', 'long'])

        for tick in ax.get_yticklabels():
            tick.set_verticalalignment('center')
            tick.set_horizontalalignment('right')

        ax.set_zlabel('Count')

    cbar = fig.colorbar(sc, ax=fig.axes, orientation='vertical', shrink=0.6, aspect=20)
    cbar.set_label('Material')
    cbar.set_ticks(list(material_mapping.values()))
    cbar.set_ticklabels(list(material_mapping.keys()))

    # chartFilePath = os.path.join(CURRENT_FILE_PATH.parent, 'Charts', 'combined_tshirt_demand.png')
    # if os.path.isfile(chartFilePath):
    #     os.remove(chartFilePath)

    # plt.savefig(chartFilePath, dpi=300)
    plt.show()


# def plot5Dcharts():
#     filePath = os.path.join(CURRENT_FILE_PATH.parent, 'Data', 't-shirts.csv')
#     data = pd.read_csv(filePath, sep=',')

#     # Mapping attributes to numerical values
#     size_mapping = {'XS': 1, 'S': 2, 'M': 3, 'L': 4, 'XL': 5, 'XXL': 6, '3XL': 7}
#     sleeves_mapping = {'short': 1, 'long': 2}
#     demand_mapping = {'low': 1, 'medium': 2, 'high': 3}
#     material_mapping = {material: idx for idx, material in enumerate(data['material'].unique())}
#     color_mapping = {color: idx for idx, color in enumerate(data['color'].unique())}

#     data['size_numeric'] = data['size'].map(size_mapping)
#     data['sleeves_numeric'] = data['sleeves'].map(sleeves_mapping)
#     data['demand_numeric'] = data['demand'].map(demand_mapping)
#     data['material_numeric'] = data['material'].map(material_mapping)
#     data['color_numeric'] = data['color'].map(color_mapping)

#     demand_types = ['low', 'medium', 'high']

#     fig = plt.figure(figsize=(14, 12))
#     gs = gridspec.GridSpec(2, 3, height_ratios=[1, 1], width_ratios=[1, 1, 1])
#     fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9, wspace=0.3, hspace=0.4)
#     fig.suptitle('T-shirt demand based on the attributes', fontsize=20, y=0.98)

#     cmap = plt.cm.get_cmap('viridis', len(material_mapping))

#     # Plot top two charts
#     for i, demand in enumerate(demand_types[:2]):
#         subset = data[data['demand'] == demand]
#         if subset.empty:
#             continue

#         counts = Counter(zip(subset['color_numeric'], subset['sleeves_numeric'], subset['material_numeric']))

#         ax = fig.add_subplot(gs[0, i*2], projection='3d')
#         ax.set_title(f'Demand: {demand}', fontsize=16, y=1.0)

#         xs, ys, zs, sizes, colors = [], [], [], [], []

#         for (color, sleeves, material), count in counts.items():
#             xs.append(color)
#             ys.append(sleeves)
#             zs.append(count)
#             sizes.append(subset[subset['color_numeric'] == color]['size_numeric'].iloc[0] * 200)
#             colors.append(material)

#         sc = ax.scatter(xs, ys, zs, c=colors, cmap=cmap, alpha=0.6, edgecolors='w', s=sizes)

#         ax.set_xlabel('Color', fontsize=12)
#         ax.set_xticks(list(color_mapping.values()))
#         ax.set_xticklabels(list(color_mapping.keys()), rotation=90)

#         ax.set_ylabel('Sleeves', fontsize=12)
#         ax.set_yticks([1, 2])
#         ax.set_yticklabels(['short', 'long'])

#         for tick in ax.get_yticklabels():
#             tick.set_verticalalignment('center')
#             tick.set_horizontalalignment('right')

#         ax.set_zlabel('Count', fontsize=12)

#     # Plot bottom chart centered
#     demand = demand_types[2]
#     subset = data[data['demand'] == demand]
#     if not subset.empty:
#         counts = Counter(zip(subset['color_numeric'], subset['sleeves_numeric'], subset['material_numeric']))

#         ax = fig.add_subplot(gs[1, 1], projection='3d')  # Centered at second column in third row
#         ax.set_title(f'Demand: {demand}', fontsize=16, y=1.0)

#         xs, ys, zs, sizes, colors = [], [], [], [], []

#         for (color, sleeves, material), count in counts.items():
#             xs.append(color)
#             ys.append(sleeves)
#             zs.append(count)
#             sizes.append(subset[subset['color_numeric'] == color]['size_numeric'].iloc[0] * 200)
#             colors.append(material)

#         sc = ax.scatter(xs, ys, zs, c=colors, cmap=cmap, alpha=0.6, edgecolors='w', s=sizes)

#         ax.set_xlabel('Color', fontsize=12)
#         ax.set_xticks(list(color_mapping.values()))
#         ax.set_xticklabels(list(color_mapping.keys()), rotation=90)

#         ax.set_ylabel('Sleeves', fontsize=12)
#         ax.set_yticks([1, 2])
#         ax.set_yticklabels(['short', 'long'])

#         for tick in ax.get_yticklabels():
#             tick.set_verticalalignment('center')
#             tick.set_horizontalalignment('right')

#         ax.set_zlabel('Count', fontsize=12)

#     cbar = fig.colorbar(sc, ax=fig.axes, orientation='vertical', shrink=0.6, aspect=20)
#     cbar.set_label('Material', fontsize=12)
#     cbar.set_ticks(list(material_mapping.values()))
#     cbar.set_ticklabels(list(material_mapping.keys()))

#     chartFilePath = os.path.join(CURRENT_FILE_PATH.parent, 'Charts', 'combined_tshirt_demand.png')
#     # remove_file_if_exists(chartFilePath)
#     # plt.savefig(chartFilePath, dpi=300)
#     plt.show()



if __name__ == '__main__':
    plot5Dcharts()
