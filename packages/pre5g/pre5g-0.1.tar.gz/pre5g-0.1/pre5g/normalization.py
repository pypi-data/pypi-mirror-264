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
    normalized_data = []
    
    if isinstance(selected_columns, int):
        selected_columns = [selected_columns]  # Convert single index to a list
        
    for i, column in enumerate(data):
        if i in selected_columns:
            min_val = min(column)
            max_val = max(column)
            normalized_column = [(x - min_val) / (max_val - min_val) for x in column]
            normalized_data.append(normalized_column)
        else:
            normalized_data.append(column)
    
    return normalized_data
