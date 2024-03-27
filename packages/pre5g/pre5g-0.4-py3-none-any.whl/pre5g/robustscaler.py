import numpy as np

def rs_all(data):
    """
    Apply RobustScaler to all columns in the dataset.

    Args:
    - data (list of lists): The data containing columns to scale.

    Returns:
    - scaled_data (list of lists): The scaled data.
    """
    scaled_data = []
    for column in data:
        median = np.median(column)
        quartile_1 = np.percentile(column, 25)
        quartile_3 = np.percentile(column, 75)
        iqr = quartile_3 - quartile_1
        scaled_column = [(x - median) / iqr for x in column]
        scaled_data.append(scaled_column)
    return scaled_data


def rs_selected_columns(data, selected_columns):
    """
    Apply RobustScaler to the selected columns in the dataset.

    Args:
    - data (list of lists): The data containing columns to scale.
    - selected_columns (list of int): The indices of the columns to scale.

    Returns:
    - scaled_data (list of lists): The scaled data.
    """
    scaled_data = []
    for i, column in enumerate(data):
        if i in selected_columns:
            median = np.median(column)
            quartile_1 = np.percentile(column, 25)
            quartile_3 = np.percentile(column, 75)
            iqr = quartile_3 - quartile_1
            scaled_column = [(x - median) / iqr for x in column]
            scaled_data.append(scaled_column)
        else:
            scaled_data.append(column)
    return scaled_data
