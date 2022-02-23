from collections import Counter, defaultdict
from plistlib import Dict
from typing import Union

import numpy as np
import sklearn.model_selection
from datasets import DatasetDict, load_dataset, ClassLabel

from tld.config import preprocessed_data_dir
from tld.linktypes import Target, linktype_map, non_link_name


def train_test_split(ds, test_size=None, train_size=None, random_state=None, shuffle=True, stratify=None):
    """
    Stratified train test split for huggingface datasets
    """

    train_indices, test_indices = sklearn.model_selection.train_test_split(
        np.arange(len(ds)),
        test_size=test_size,
        train_size=train_size,
        random_state=random_state,
        shuffle=shuffle,
        stratify=None if stratify is None else ds[stratify],
    )

    return DatasetDict({
        'train': ds.select(train_indices),
        'test': ds.select(test_indices),
    })


def get_link_dataset(
        tracker: str,
        target: Target,
        include_non_links: bool,
        linktype_min_portion: float = 0.01,
        test_size: float = 0.2,
        val_size: float = 0.2,
) -> DatasetDict:
    """
    Get a prepared link dataset, stratified by target linktype

    :param tracker: The name of the issue tracker
    :param target: The targeted link granularity
    :param include_non_links: Whether to include non-links
    :param linktype_min_portion: Which portion of all links a linktype has to make up. Links with a type less frequent are discared
    :param test_size: Which portion of the full dataset to use for the testset
    :param val_size: Which portion of the trainval split (i.e. full dataset without test) to use for validation
    :return:
    """

    assert target in ['linktype', 'category']

    ds = load_dataset('csv', data_files=str(preprocessed_data_dir / f'joined_{tracker}.csv'))

    # remove infrequent linktypes
    linktype_ctr = Counter(linktype for linktype in ds['train']['linktype'])
    min_occurrences_per_linktype = linktype_min_portion * sum(linktype_ctr.values())
    included_linktypes = {linktype for linktype, occurrences in linktype_ctr.most_common() if occurrences > min_occurrences_per_linktype}
    ds = ds.filter(lambda ex: ex['linktype'] in included_linktypes)

    ds = train_test_split(ds['train'], test_size=test_size, stratify='linktype', random_state=0)
    trainval_ds = train_test_split(ds['train'], test_size=val_size, stratify='linktype', random_state=0)

    ds = DatasetDict({
        'train': trainval_ds['train'],
        'val': trainval_ds['test'],
        'test': ds['test'],
    })

    full_linktype_map: Dict[str, Union[str, None]] = defaultdict(lambda: None, linktype_map[target])

    if include_non_links:
        full_linktype_map[non_link_name] = non_link_name

    ds = ds.map(lambda ex: {'label': full_linktype_map[ex['linktype']]}) \
        .filter(lambda ex: ex['label'] is not None)

    label_ctr = Counter(label for split in ds.values() for label in split['label'])
    label_names = [label for label, _ in label_ctr.most_common()]
    label_feature = ClassLabel(names=label_names)

    ds = ds.map(lambda ex: {'label': label_feature.str2int(ex['label'])}) \
        .cast_column('label', label_feature)

    return ds
