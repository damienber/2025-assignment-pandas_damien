import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def load_data():
    """Load data from the CSV files."""
    referendum = pd.read_csv(
        'data/referendum.csv',
        dtype={'department_code': str}
    )
    regions = pd.read_csv(
        'data/regions.csv',
        dtype={'code': str}
    )
    departments = pd.read_csv(
        'data/departments.csv',
        dtype={'code': str, 'region_code': str}
    )
    return referendum, regions, departments



def merge_regions_and_departments(regions, departments):
    """Merge regions and departments in one DataFrame."""
    merged = pd.merge(
        regions,
        departments,
        left_on='code',
        right_on='region_code',
        suffixes=('_reg', '_dep')
    )

    merged = merged.rename(
        columns={
            'code_reg': 'code_reg',
            'name_reg': 'name_reg',
            'code_dep': 'code_dep',
            'name_dep': 'name_dep'
        }
    )

    return merged[['code_reg', 'name_reg', 'code_dep', 'name_dep']]


def merge_referendum_and_areas(referendum, regions_and_departments):
    """Merge referendum and geographic areas."""
    referendum = referendum[
        ~referendum['department_code'].str.contains('Z')
    ]

    merged = pd.merge(
        referendum,
        regions_and_departments,
        left_on='department_code',
        right_on='code_dep'
    )

    return merged


def compute_referendum_result_by_regions(referendum_and_areas):
    """Aggregate referendum results by region."""
    result = referendum_and_areas.groupby('code_reg').agg(
        name_reg=('name_reg', 'first'),
        Registered=('Registered', 'sum'),
        Abstentions=('Abstentions', 'sum'),
        Null=('Null', 'sum'),
        Choice_A=('Choice A', 'sum'),
        Choice_B=('Choice B', 'sum')
    )

    return result


def plot_referendum_map(referendum_result_by_regions):
    """Plot the referendum results on a map."""
    gdf = gpd.read_file('regions.geojson')

    merged = gdf.merge(
        referendum_result_by_regions,
        left_on='code',
        right_index=True
    )

    merged['ratio'] = (
        merged['Choice_A'] /
        (merged['Choice_A'] + merged['Choice_B'])
    )

    merged.plot(
        column='ratio',
        legend=True,
        figsize=(10, 8)
    )

    return merged


if __name__ == "__main__":
    referendum, df_reg, df_dep = load_data()

    regions_and_departments = merge_regions_and_departments(
        df_reg,
        df_dep
    )

    referendum_and_areas = merge_referendum_and_areas(
        referendum,
        regions_and_departments
    )

    referendum_results = compute_referendum_result_by_regions(
        referendum_and_areas
    )

    print(referendum_results)

    plot_referendum_map(referendum_results)
    plt.show()
