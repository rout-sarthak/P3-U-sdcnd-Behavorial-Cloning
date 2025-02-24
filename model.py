import tensorflow as tf
from keras.layers import Dense, Flatten, Lambda, Activation, MaxPooling2D
from keras.layers.convolutional import Convolution2D
from keras.models import Sequential
from keras.optimizers import Adam
import helper


epochs = 8
epoch_samples = 20032
learning_rate = 1e-4
validation_set = 6400
activate_relu = 'relu'
tf.python.control_flow_ops = tf

# NVIDIA's "End to End Learning for Self-Driving Cars" paper was used for developing this model https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf
model = Sequential()

model.add(Lambda(lambda x: x / 127.5 - 1.0, input_shape=(64, 64, 3)))

# The first five convolutional and maxpooling layers
model.add(Convolution2D(24, 5, 5, border_mode='same', subsample=(2, 2)))
model.add(Activation(activate_relu))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))

model.add(Convolution2D(36, 5, 5, border_mode='same', subsample=(2, 2)))
model.add(Activation(activate_relu))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))

model.add(Convolution2D(48, 5, 5, border_mode='same', subsample=(2, 2)))
model.add(Activation(activate_relu))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))

model.add(Convolution2D(64, 3, 3, border_mode='same', subsample=(1, 1)))
model.add(Activation(activate_relu))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))

model.add(Convolution2D(64, 3, 3, border_mode='same', subsample=(1, 1)))
model.add(Activation(activate_relu))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))

model.add(Flatten())

# Next, five fully connected layers
model.add(Dense(1164))
model.add(Activation(activate_relu))

model.add(Dense(100))
model.add(Activation(activate_relu))

model.add(Dense(50))
model.add(Activation(activate_relu))

model.add(Dense(10))
model.add(Activation(activate_relu))

model.add(Dense(1))

model.summary()

model.compile(optimizer=Adam(learning_rate), loss="mse", )

# separate generators for training and validation
train_gen = helper.generate_next_batch()
validation_gen = helper.generate_next_batch()

history = model.fit_generator(train_gen,
                              samples_per_epoch=epoch_samples,
                              nb_epoch=epochs,
                              validation_data=validation_gen,
                              nb_val_samples=validation_set,
                              verbose=1)

helper.save_model(model) #saving model and weights

