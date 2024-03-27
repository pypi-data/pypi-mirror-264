import json
import subprocess

import numpy as np
import pandas as pd


def get_closest_metric(data,
                       current_epoch: int,
                       metric_col="metric",
                       epoch_col="epoch") -> float:
    """
    This function takes a pandas DataFrame, a current epoch value,
    and column names for metric and epoch as input.
    It returns the value of the "metric" column for the row that
      has the closest epoch to the current epoch.

    Args:
        data (pd.DataFrame): The pandas DataFrame containing the data.
        current_epoch (int): The current epoch value.
        metric_col (str, optional): The name of the column containing
                                    the metric values. Defaults to "metric".
        epoch_col (str, optional): The name of the column containing the epoch
                                 values. Defaults to "epoch".

    Returns:
        float: The value of the "metric" column for
               the row with the closest epoch.
    """

    # Ensure numerical data types for epoch
    data[epoch_col] = pd.to_numeric(data[epoch_col], errors='coerce')

    # Handle potential missing values in epoch column
    if data[epoch_col].isnull().any():
        raise ValueError("Epoch column contains missing values")

    # Calculate absolute differences between current epoch and all epochs
    epoch_diffs = np.abs(data[epoch_col] - current_epoch)

    # Find the index of the row with the closest epoch
    closest_epoch_idx = epoch_diffs.idxmin()

    # Return the corresponding metric value
    return data.loc[closest_epoch_idx, metric_col]


def execute_linux_command(command):
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, errors = process.communicate()
    return output.decode(), errors.decode()


def read_json_from_filename(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data
