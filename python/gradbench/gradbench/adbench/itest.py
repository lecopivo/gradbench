# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

# https://github.com/microsoft/ADBench/blob/38cb7931303a830c3700ca36ba9520868327ac87/src/python/shared/ITest.py

# Changes made: removed 'times' parameter and 'output' method.

from abc import ABC, abstractmethod


class ITest(ABC):
    # This function must be called before any other function.
    @abstractmethod
    def prepare(self, input):
        pass

    @abstractmethod
    def calculate_objective(self):
        pass

    @abstractmethod
    def calculate_jacobian(self):
        pass
