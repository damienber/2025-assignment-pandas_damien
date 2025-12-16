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
