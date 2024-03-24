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
import torch

from bigdl.nano.pytorch.lightning import LightningModule
from bigdl.nano.utils.common import invalidInputError
from bigdl.nano.utils.common import AcceleratedModel
import numpy as np
from typing import Sequence


class AcceleratedLightningModule(AcceleratedModel, LightningModule):
    def __init__(self, model):
        super().__init__(model)
        self.model = model
        self.train(False)

    def forward(self, *inputs, **kwargs):
        inputs = self.on_forward_start(inputs)
        kwargs = self.on_forward_start_kwargs(**kwargs)
        outputs = self.forward_step(*inputs, **kwargs)
        return self.on_forward_end(outputs)

    def on_train_start(self) -> None:
        invalidInputError(False, errMsg="This model is not trainable!")

    def train(self, mode=False):
        if mode:
            invalidInputError(False, "This model is not trainable!")
        super().train(mode)

    def forward_step(self, *inputs, **kwargs):
        return self.model(*inputs, **kwargs)

    def on_forward_start_kwargs(self, **kwargs):
        return kwargs

    @staticmethod
    def tensors_to_numpy(tensors):
        # TODO: add more type transformation here
        def to_numpy(ts):
            result = []
            for x in ts:
                if isinstance(x, torch.Tensor):
                    result.append(x.cpu().detach().numpy())
                elif isinstance(x, np.ndarray):
                    result.append(x)
                elif np.isscalar(x):
                    # convert scalar to numpy
                    result.append(np.array(x))
                elif isinstance(x, Sequence):
                    result.append(to_numpy(x))
                else:
                    invalidInputError(False, f"Unexpected Type: {x}")
            return tuple(result)
        return to_numpy(tensors)

    @staticmethod
    def numpy_to_tensors(np_arrays):
        tensors = tuple(map(lambda x: torch.from_numpy(x), np_arrays))
        if len(tensors) == 1:
            tensors = tensors[0]
        return tensors

    @staticmethod
    def cope_with_keyword_arguments(kwargs):
        # inplace convert kwargs
        for k in kwargs.keys():
            if isinstance(kwargs[k], tuple):
                kwargs[k] = numpy_to_tensors(kwargs[k])
            if isinstance(kwargs[k], torch.Tensor):
                kwargs[k] = kwargs[k].cpu().detach().numpy()
            if np.isscalar(kwargs[k]):
                kwargs[k] = np.array(kwargs[k])
