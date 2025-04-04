# Copyright (c) Microsoft Corporation.

# MIT License

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# https://github.com/microsoft/ADBench/blob/38cb7931303a830c3700ca36ba9520868327ac87/src/python/modules/TensorflowCommon/ba_objective.py


import tensorflow as tf
from gradbench.adbench.defs import C_IDX, F_IDX, RAD_IDX, ROT_IDX, X0_IDX


def rodrigues_rotate_point(rot, X):
    def rotate():
        theta = tf.math.sqrt(sqtheta)
        costheta = tf.math.cos(theta)
        sintheta = tf.math.sin(theta)

        w = rot / theta
        w_cross_X = tf.linalg.cross(w, X)
        tmp = tf.tensordot(w, X, 1) * (1.0 - costheta)

        return X * costheta + w_cross_X * sintheta + w * tmp

    sqtheta = tf.reduce_sum(rot**2)
    return tf.cond(
        tf.not_equal(sqtheta, 0.0), rotate, lambda: X + tf.linalg.cross(rot, X)
    )


def radial_distort(rad_params, proj):
    rsq = tf.reduce_sum(proj**2)
    L = 1.0 + rad_params[0] * rsq + rad_params[1] * rsq * rsq
    return proj * L


def project(cam, X):
    Xcam = rodrigues_rotate_point(
        cam[ROT_IDX : ROT_IDX + 3], X - cam[C_IDX : C_IDX + 3]
    )

    distorted = radial_distort(cam[RAD_IDX : RAD_IDX + 2], Xcam[0:2] / Xcam[2])
    return distorted * cam[F_IDX] + cam[X0_IDX : X0_IDX + 2]


def compute_reproj_err(cam, X, w, feat):
    return w * (project(cam, X) - feat)


def compute_w_err(w):
    return 1.0 - w**2
