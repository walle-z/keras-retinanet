"""
Copyright 2018 vidosits (https://github.com/vidosits/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import warnings
import pytest
import numpy as np
import keras
from keras_retinanet import losses
from keras_retinanet.models.densenet import densenet_retinanet

parameters = ['densenet121']


@pytest.mark.parametrize("backbone", parameters)
def test_backbone(backbone):
    # ignore warnings in this test
    warnings.simplefilter('ignore')

    num_classes = 10

    # inputs = np.zeros((1, 224, 224, 3), dtype=np.float32)
    # targets = [np.zeros((1, 9441, 5), dtype=np.float32), np.zeros((1, 9441, num_classes))]

    inputs = np.zeros((1, 200, 400, 3), dtype=np.float32)
    targets = [np.zeros((1, 15318, 5), dtype=np.float32), np.zeros((1, 15318, num_classes))]

    inp = keras.layers.Input(inputs[0].shape)

    training_model = densenet_retinanet(num_classes=num_classes, backbone='{}'.format(backbone), inputs=inp)
    # training_model.summary()

    # compile model
    training_model.compile(
        loss={
            'regression': losses.smooth_l1(),
            'classification': losses.focal()
        },
        optimizer=keras.optimizers.adam(lr=1e-5, clipnorm=0.001))

    training_model.fit(inputs, targets, batch_size=1)
