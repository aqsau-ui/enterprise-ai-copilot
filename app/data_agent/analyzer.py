import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.
    """

    dataframe = pd.read_csv(file_path)

    return dataframe


def get_dataset_info(
    dataframe: pd.DataFrame
) -> dict:
    """
    Return basic information about the dataset.
    """

    return {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "column_names": dataframe.columns.tolist(),
        "missing_values": dataframe.isnull()
        .sum()
        .to_dict(),
        "data_types": dataframe.dtypes.astype(str)
        .to_dict(),
    }