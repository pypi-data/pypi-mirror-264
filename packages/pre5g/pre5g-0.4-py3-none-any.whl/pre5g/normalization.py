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
    # Initialize an empty list to store normalized data
    normalized_data = []
    
    # Iterate over each row in the data
    for row in data:
        # Initialize an empty list to store normalized values for the row
        normalized_row = []
        # Iterate over each column index
        for i, val in enumerate(row):
            # Check if the current column index is in the selected columns list
            if i in selected_columns:
                # Normalize the value and append it to the normalized row
                min_val = min(data[:, i])
                max_val = max(data[:, i])
                normalized_val = (val - min_val) / (max_val - min_val)
                normalized_row.append(normalized_val)
            else:
                # If the column is not selected, append the original value to the normalized row
                normalized_row.append(val)
        # Append the normalized row to the list of normalized data
        normalized_data.append(normalized_row)
    
    return normalized_data
