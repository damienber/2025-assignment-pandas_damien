"""Plotting referendum results in pandas.
In short, we want to make beautiful map to report results of a referendum. In
some way, we would like to depict results with something similar to the maps
that you can find here:
https://github.com/x-datascience-datacamp/datacamp-assignment-pandas/blob/main/example_map.png
To do that, you will load the data as pandas.DataFrame, merge the info and
aggregate them by regions and finally plot them on a map using `geopandas`.
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def load_data():
    """Load data from the CSV files referundum/regions/departments."""
    referendum = pd.DataFrame({})
    regions = pd.DataFrame({})
    departments = pd.DataFrame({})
    referendum = pd.read_csv('data/referendum.csv', sep=';')
    regions = pd.read_csv('data/regions.csv')
    departments = pd.read_csv('data/departments.csv')
    return referendum, regions, departments


def merge_regions_and_departments(regions, departments):
    """Merge regions and departments in one DataFrame."""
    regions = regions.rename(columns={
        'code': 'code_reg',
        'name': 'name_reg'
    })
    departments = departments.rename(columns={
        'region_code': 'code_reg',
        'code': 'code_dep',
        'name': 'name_dep'
    })
    merged = pd.merge(regions, departments, on='code_reg')

    return merged[['code_reg', 'name_reg', 'code_dep', 'name_dep']]


def merge_referendum_and_areas(referendum, regions_and_departments):
    referendum = referendum.copy()
    regions_and_departments = regions_and_departments.copy()

    referendum['code_dep'] = (
        referendum['Department code']
        .astype(str)
        .str.zfill(2)
    )

    regions_and_departments['code_dep'] = (
        regions_and_departments['code_dep']
        .astype(str)
        .str.zfill(2)
    )

    referendum = referendum[
        ~referendum['code_dep'].str.contains('Z')
    ]

    merged = pd.merge(
        referendum,
        regions_and_departments,
        on='code_dep'
    )

    return merged


def compute_referendum_result_by_regions(referendum_and_areas):
    cols = [
        'Registered',
        'Abstentions',
        'Null',
        'Choice A',
        'Choice B'
    ]

    grouped = referendum_and_areas.groupby(
        ['code_reg', 'name_reg']
    )[cols].sum()

    return grouped.reset_index('name_reg')


def plot_referendum_map(referendum_result_by_regions):
    geo_regions = gpd.read_file('data/regions.geojson')

    gdf = geo_regions.merge(
        referendum_result_by_regions,
        left_on='code',
        right_index=True
    )

    gdf['ratio'] = (
        gdf['Choice A'] /
        (gdf['Choice A'] + gdf['Choice B'])
    )

    gdf.plot(
        column='ratio',
        legend=True,
        figsize=(10, 10)
    )

    plt.title("Referendum Results: Choice A Ratio")
    plt.axis('off')

    return gdf


if __name__ == "__main__":
    referendum, df_reg, df_dep = load_data()
    regions_and_departments = merge_regions_and_departments(
        df_reg, df_dep
    )
    referendum_and_areas = merge_referendum_and_areas(
        referendum, regions_and_departments
    )
    referendum_results = compute_referendum_result_by_regions(
        referendum_and_areas
    )
    print(referendum_results)
    plot_referendum_map(referendum_results)

    plt.show()
