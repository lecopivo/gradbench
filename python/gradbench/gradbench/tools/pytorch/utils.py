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

# https://github.com/microsoft/ADBench/blob/38cb7931303a830c3700ca36ba9520868327ac87/src/python/modules/PyTorch/utils.py

import torch


def to_torch_tensor(param, grad_req=False, dtype=torch.float64):
    """Converts given single parameter to torch tensors. Note that parameter
    can be an ndarray-like object.

    Args:
        param (ndarray-like): parameter to convert.
        grad_req (bool, optional): defines flag for calculating tensor
            jacobian for created torch tensor. Defaults to False.
        dtype (type, optional): defines a type of tensor elements. Defaults to
            torch.float64.

    Returns:
        torch tensor
    """

    return torch.tensor(param, dtype=dtype, requires_grad=grad_req)


def to_torch_tensors(params, grad_req=False, dtype=torch.float64):
    """Converts given multiple parameters to torch tensors. Note that
    parameters can be ndarray-lake objects.

    Args:
        params (enumerable of ndarray-like): parameters to convert.
        grad_req (bool, optional): defines flag for calculating tensor
            jacobian for created torch tensors. Defaults to False.
        dtype (type, optional): defines a type of tensor elements. Defaults to
            torch.float64.

    Returns:
        tuple of torch tensors
    """

    return tuple(
        torch.tensor(param, dtype=dtype, requires_grad=grad_req) for param in params
    )


def torch_jacobian(func, inputs, params=None, flatten=True):
    """Calculates jacobian and return value of the given function that uses
    torch tensors.

    Args:
        func (callable): function which jacobian is calculating.
        inputs (tuple of torch tensors): function inputs by which it is
            differentiated.
        params (tuple of torch tensors, optional): function inputs by which it
            is not differentiated. Defaults to None.
        flatten (bool, optional): if True then jacobian will be written in
            1D array row-major. Defaults to True.

    Returns:
        torch tensor, torch tensor: function result and function jacobian.
    """

    def recurse_backwards(output, inputs, J, flatten):
        """Recursively calls .backward on multi-dimensional output."""

        def get_grad(tensor, flatten):
            """Returns tensor gradient flatten representation. Added for
            performing concatenation of scalar tensors gradients."""

            if tensor.dim() > 0:
                if flatten:
                    return tensor.grad.flatten()
                else:
                    return tensor.grad
            else:
                return tensor.grad.view(1)

        if output.dim() > 0:
            for item in output:
                recurse_backwards(item, inputs, J, flatten)
        else:
            for inp in inputs:
                inp.grad = None

            output.backward(retain_graph=True)

            J.append(torch.cat(list(get_grad(inp, flatten) for inp in inputs)))

    if params is not None:
        res = func(*inputs, *params)
    else:
        res = func(*inputs)

    J = []
    recurse_backwards(res, inputs, J, flatten)

    J = torch.stack(J)
    if flatten:
        J = J.t().flatten()

    return res, J
