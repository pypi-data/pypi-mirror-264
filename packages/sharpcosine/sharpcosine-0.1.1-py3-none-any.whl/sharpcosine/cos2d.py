import tensorflow as tf

class CosSimConv2D(tf.keras.layers.Layer):
    def __init__(self, units=32):
        super(CosSimConv2D, self).__init__()
        self.units = units
        self.kernel_size = 3

    def build(self, input_shape):
        self.in_shape = input_shape

        self.flat_size = self.in_shape[1] * self.in_shape[2]
        self.channels = self.in_shape[3]

        self.w = self.add_weight(
            shape=(1, self.channels * tf.square(self.kernel_size), self.units),
            initializer="glorot_uniform",
            trainable=True,
        )

        self.p = self.add_weight(
            shape=(self.units,), initializer='zeros', trainable=True)

        self.q = self.add_weight(
            shape=(1,), initializer='zeros', trainable=True)

    def l2_normal(self, x, axis=None, epsilon=1e-12):
        square_sum = tf.reduce_sum(tf.square(x), axis, keepdims=True)
        x_inv_norm = tf.sqrt(tf.maximum(square_sum, epsilon))
        return x_inv_norm

    def stack3x3(self, image):
        stack = tf.stack(
            [
                tf.pad(image[:, :-1, :-1, :], tf.constant([[0,0], [1,0], [1,0], [0,0]])),   # top row
                tf.pad(image[:, :-1, :, :],   tf.constant([[0,0], [1,0], [0,0], [0,0]])),
                tf.pad(image[:, :-1, 1:, :],  tf.constant([[0,0], [1,0], [0,1], [0,0]])),

                tf.pad(image[:, :, :-1, :],   tf.constant([[0,0], [0,0], [1,0], [0,0]])),   # middle row
                image,
                tf.pad(image[:, :, 1:, :],    tf.constant([[0,0], [0,0], [0,1], [0,0]])),

                tf.pad(image[:, 1:, :-1, :],  tf.constant([[0,0], [0,1], [1,0], [0,0]])),    # bottom row
                tf.pad(image[:, 1:, :, :],    tf.constant([[0,0], [0,1], [0,0], [0,0]])),
                tf.pad(image[:, 1:, 1:, :],   tf.constant([[0,0], [0,1], [0,1], [0,0]]))
            ], axis=3)
        return stack

    def call(self, inputs, training=None):
        x = self.stack3x3(inputs)
        x = tf.reshape(x, (-1, self.flat_size, self.channels * tf.square(self.kernel_size)))
        q = tf.square(self.q) / 10
        x_norm = self.l2_normal(x, axis=2) + q
        w_norm = self.l2_normal(self.w, axis=1) + q
        sign = tf.sign(tf.matmul(x, self.w))
        x = tf.matmul(x / x_norm, self.w / w_norm)
        x = tf.abs(x) + 1e-12
        x = tf.pow(x, tf.nn.softmax(self.p))
        x = sign * x
        x = tf.reshape(x, (-1, self.in_shape[1], self.in_shape[2], self.units))
        return x