import numpy as np

from src.net import Network

import theano.tensor as T

from src.utils import get_one_hot

from src import mnist_loader

from src.model_tests import run_test

from src.utils import display_tsne

(train_images, train_labels, test_images, test_labels) = mnist_loader.load_mnist()

display_tsne(train_images[:1000], train_labels[:1000])

train_labels = get_one_hot(train_labels)

train_images = np.reshape(train_images, (train_images.shape[0], 28, 28))
test_images = np.reshape(test_images, (test_images.shape[0], 28, 28))

input_var = T.tensor4('input')
y = T.fmatrix('truth')

network_conv_config = {
    'mode': 'conv',
    'filters': [10, 5],
    'filter_size': [[3, 3], [5, 5]],
    'stride': [[1, 1], [1, 1]],
    'pool': {
        'mode': 'max',
        'stride': [[2, 2], [2, 2]]
    }
}

conv_net = Network(
    name='conv_test',
    dimensions=[None, 1] + list(train_images.shape[1:]),
    input_var=input_var,
    y=y,
    config=network_conv_config,
    input_network=None,
    num_classes=10,
    activation='rectify',
    pred_activation='softmax',
    optimizer='adam')

train_images = np.expand_dims(train_images, axis=1)
test_images = np.expand_dims(test_images, axis=1)
# # Use to load model from disk
# # dense_net = Network.load_model('models/20170704194033_3_dense_test.network')
conv_net.train(
    epochs=2,
    train_x=train_images[:50000],
    train_y=train_labels[:50000],
    val_x=train_images[50000:60000],
    val_y=train_labels[50000:60000],
    batch_ratio=0.05,
    plot=True
)

conv_net.save_record()

run_test(conv_net, test_x=train_images[50000:60000], test_y=train_labels[50000:60000])
conv_net.save_model()
