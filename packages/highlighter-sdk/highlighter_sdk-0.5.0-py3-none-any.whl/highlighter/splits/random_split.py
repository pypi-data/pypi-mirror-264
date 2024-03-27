from typing import List, Dict, Tuple
import numpy as np
from highlighter.datasets import Dataset

__all__ = ["random_split"]

"""
split fn to return Dataset and dict(heading, str)
"""

def random_split(
        dataset: Dataset,
        seed: int = 42,
        fracs: List[float] = [0.8, 0.2],
        names: List[str] = ["train", "test"],
        ) -> Tuple[Dataset, Dict[str, str]]:
    if sum(fracs) < 0.999999:
        raise ValueError(f"Split fracs must sum to 1.0, got: {fracs}")

    if len(names) > len(set(names)):
        raise ValueError(f"Split names must be unique, got: {names}")

    data_file_ids = dataset.data_files_df.data_file_id.unique()
    np.random.seed(seed=seed)
    np.random.shuffle(data_file_ids)

    slice_start = 0
    dataset.data_files_df.split = names[0]
    for frac, name in zip(fracs[1:], names[1:]):
        slice_end = round(data_file_ids.shape[0] * frac) + slice_start
        split_ids = data_file_ids[slice_start:slice_end]
        dataset.data_files_df.loc[
                dataset.data_files_df.data_file_id.isin(split_ids), "split"] = name
        slice_start = slice_end

    return dataset.data_files_df, dataset.annotations_df
