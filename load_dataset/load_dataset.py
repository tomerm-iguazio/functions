# Copyright 2018 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd
from mlrun.execution import MLClientCtx


def get_toy_data(
        context: MLClientCtx,
        dataset: str,
        format: str = 'pq',
        name: str = '',
        params: dict = {}
) -> None:
    """Loads a scikit-learn toy dataset for classification or regression

    The following datasets are available ('name' : desription):

        'iris'     : iris dataset (classification)
        'diabetes' : diabetes dataset (regression)
        'wine'     : wine dataset (classification)

    The scikit-learn functions return a data bunch including the following items:
    - data              the features matrix
    - target            the ground truth labels
    - DESCR             a description of the dataset
    - feature_names     header for data

    The features (and their names) are stored with the target labels in a DataFrame.

    For further details see https://scikit-learn.org/stable/datasets/index.html#toy-datasets

    :param context:    function execution context
    :param dataset:    name of the dataset to load
    :param format:     output format: pq or csv
    :param name:       artifact name (defaults to dataset)
    :param params:     params of the sklearn load_data method
    """

    # reach into module and import the appropriate load_xxx function
    pkg_module = 'sklearn.datasets'
    fname = f'load_{dataset}'

    pkg_module = __import__(pkg_module, fromlist=[fname])
    load_data_fn = getattr(pkg_module, fname)

    data = load_data_fn(**params)
    feature_names = data['feature_names']

    # create the toy dataset
    xy = np.concatenate([data['data'], data['target'].reshape(-1, 1)], axis=1)
    feature_names.append('labels')
    df = pd.DataFrame(data=xy, columns=feature_names)

    # log and upload the dataset
    context.log_dataset(name or dataset, df=df, format=format, index=False)