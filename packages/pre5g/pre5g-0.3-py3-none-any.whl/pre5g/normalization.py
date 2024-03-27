# normalization.py
def normalize_all(data):
    """
    Normalize all columns in the dataset.
    """
    normalized_data = []
    for column in data:
        min_val = min(column)
        max_val = max(column)
        normalized_column = [(x - min_val) / (max_val - min_val) for x in column]
        normalized_data.append(normalized_column)
    return normalized_data

def normalize_selected_columns(data, selected_columns):
    """
    Normalize the selected columns in the data.
    
    Args:
    - data (list of lists): The data containing columns to normalize.
    - selected_columns (list of int): The indices of the columns to normalize.
    
    Returns:
    - normalized_data (list of lists): The normalized data.
    """
    # Transpose the data to work on columns
    data_transposed = list(map(list, zip(*data)))
    normalized_data_transposed = []
    
    if selected_columns:  # Check if selected_columns is not empty
        for i, column in enumerate(data_transposed):
            if i in selected_columns:
                min_val = min(column)
                max_val = max(column)
                normalized_column = [(x - min_val) / (max_val - min_val) for x in column]
                normalized_data_transposed.append(normalized_column)
            else:
                normalized_data_transposed.append(column)
    else:
        normalized_data_transposed = data_transposed
    
    # Transpose the normalized data back to its original orientation
    normalized_data = list(map(list, zip(*normalized_data_transposed)))
    
    return normalized_data
