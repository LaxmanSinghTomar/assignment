# Training CNN Model

# Importing Libraries
import tensorflow as tf; print(tf.__version__)
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.optimizers import SGD

import numpy as np

import os

# Setting the Seed
np.random.seed(42)

# Downloading Dataseet i.e. Fashion MNIST
fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# Normalize Images and converting labels to categories
train_images = train_images.reshape((train_images.shape[0], 28, 28, 1))
test_images = test_images.reshape((test_images.shape[0], 28, 28, 1))

train_images, train_labels = train_images / 255.0, to_categorical(train_labels)
test_images, test_labels = test_images / 255.0, to_categorical(test_labels)

def cnn_model():
    """
    This function creates a CNN model.

    Returns:
        A Keras Model Architecture.
    
    """
    model = Sequential()
    model.add(Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)))
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(0.5))
    model.add(Conv2D(128, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(128, activation='relu', kernel_initializer = 'he_uniform'))
    model.add(Dense(10, 'softmax'))
    return model

# Setting up Optimizers, Callbacks
optimizer = 'adam'
model = cnn_model()
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

validation_callback = tf.keras.callbacks.EarlyStopping(
    monitor="val_accuracy",
    verbose=1,
    mode="auto",
    patience = 5,
    baseline=None,
    restore_best_weights=True,
)

# Train the CNN Model
history = model.fit(train_images, train_labels,
                     epochs=50, batch_size=512,
                     verbose=1, callbacks = [validation_callback], validation_split=0.2)


# Save the Model with weights
if not os.path.exists("models/"):
    os.makedirs("models/")
model.save("models/fashion_mnist_cnn")

                