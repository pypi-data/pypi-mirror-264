#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import numpy as np

from bigdl.orca.learn.utils import get_latest_checkpoint
from bigdl.dllib.utils.log4Error import invalidInputError

from typing import TYPE_CHECKING, Dict, Union, Callable, Optional, Any
if TYPE_CHECKING:
    from bigdl.orca.learn.tf2.ray_estimator import TensorFlow2Estimator
    from bigdl.orca.learn.tf2.pyspark_estimator import SparkTFEstimator

logger = logging.getLogger(__name__)


class Estimator(object):
    @staticmethod
    def from_keras(*,
                   model_creator: Optional[Callable]=None,
                   config: Optional[Dict]=None,
                   verbose: bool=False,
                   workers_per_node: int=1,
                   compile_args_creator: Optional[Callable]=None,
                   backend: str="ray",
                   cpu_binding: bool=False,
                   log_to_driver: bool=True,
                   model_dir: Optional[str]=None,
                   **kwargs
                   ) -> Union["TensorFlow2Estimator", "SparkTFEstimator", None]:
        """
        Create an Estimator for tensorflow 2.

        :param model_creator: (dict -> Model) This function takes in the `config`
               dict and returns a compiled TF model.
        :param config: (dict) configuration passed to 'model_creator',
               'data_creator'. Also contains `fit_config`, which is passed
               into `model.fit(data, **fit_config)` and
               `evaluate_config` which is passed into `model.evaluate`.
        :param verbose: (bool) Prints output of one model if true.
        :param workers_per_node: (Int) worker number on each node. default: 1.
        :param compile_args_creator: (dict -> dict of loss, optimizer and metrics) Only used when
               the backend="horovod". This function takes in the `config` dict and returns a
               dictionary like {"optimizer": tf.keras.optimizers.SGD(lr), "loss":
               "mean_squared_error", "metrics": ["mean_squared_error"]}
        :param backend: (string) You can choose "horovod", "ray" or "spark" as backend.
         Default: `ray`.
        :param cpu_binding: (bool) Whether to binds threads to specific CPUs. Default: False
        :param log_to_driver: (bool) Whether display executor log on driver in cluster mode.
         Default: True. This option is only for "spark" backend.
        :param model_dir: (str) The directory to save model states. It is required for "spark"
        backend. For cluster mode, it should be a share filesystem path which can be accessed
        by executors.
        """
        if backend in {"ray", "horovod"}:
            from bigdl.orca.learn.tf2.ray_estimator import TensorFlow2Estimator
            return TensorFlow2Estimator(model_creator=model_creator, config=config,
                                        verbose=verbose, workers_per_node=workers_per_node,
                                        backend=backend, compile_args_creator=compile_args_creator,
                                        cpu_binding=cpu_binding)
        elif backend == "spark":
            if cpu_binding:
                invalidInputError(False,
                                  "cpu_binding should not be True when using spark backend")
            from bigdl.orca.learn.tf2.pyspark_estimator import SparkTFEstimator
            return SparkTFEstimator(model_creator=model_creator,
                                    config=config, verbose=verbose,
                                    compile_args_creator=compile_args_creator,
                                    workers_per_node=workers_per_node,
                                    log_to_driver=log_to_driver,
                                    model_dir=model_dir,
                                    **kwargs)
        else:
            invalidInputError(False,
                              "Only horovod, ray and spark backends are supported"
                              f" for now, got backend: {backend}")
            return None

    @staticmethod
    def latest_checkpoint(checkpoint_dir: str) -> str:
        return get_latest_checkpoint(checkpoint_dir)


def make_data_creator(refs: Any) -> Callable:
    def data_creator(config, batch_size):
        return refs

    return data_creator


def data_length(data):
    x = data["x"]
    if isinstance(x, np.ndarray):
        return x.shape[0]
    else:
        return x[0].shape[0]
