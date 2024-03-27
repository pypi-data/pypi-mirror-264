import pandas as pd

def standardize_all(data):
    """
    Standardize all columns in the dataset.

    Args:
    - data (list of lists): The data containing columns to standardize.

    Returns:
    - standardized_data (list of lists): The standardized data.
    """
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Standardize all columns
    standardized_df = (df - df.mean()) / df.std()

    # Convert the standardized DataFrame back to a list of lists
    standardized_data = standardized_df.values.tolist()

    return standardized_data



def standardize_selected_columns(data, selected_columns):
    """
    Standardize the selected columns in the data.
    
    Args:
    - data (list of lists): The data containing columns to standardize.
    - selected_columns (list of int): The indices of the columns to standardize.
    
    Returns:
    - standardized_data (list of lists): The standardized data.
    """
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Standardize the selected columns
    for col_index in selected_columns:
        df[col_index] = (df[col_index] - df[col_index].mean()) / df[col_index].std()

    # Convert the standardized DataFrame back to a list of lists
    standardized_data = df.values.tolist()

    return standardized_data
