from typing import Any
from numpy.typing import NDArray
import numpy as np


def convert_to_float32(array: np.ndarray) -> NDArray[np.float32]:
    """
    Changes a given array type to np.NDArray[np.float32].

    :param array: input constraint mask of shape (M, N).
    :type array: a NumPy 2-D dense ndarray.

    :return: Array of type float32
    :rtype: NDArray[np.float32]
    """
    return array.astype(np.float32)


def reshape_to_2d(array: np.ndarray) -> NDArray[Any]:
    """
    Reshape a given array to a 2-D array.

    :param array: input constraint mask of shape (N,).
    :type array: a NumPy 1-D dense ndarray.

    :return: Array of type Any
    :rtype: NDArray[np.Any]
    """
    if array.ndim != 1:
        raise ValueError("Input array is not 1-D. Cannot reshape array.")
    return array.reshape(1, -1)


def is_ndarray_binary(array: NDArray) -> bool:
    """
    :return: if all values ares either 1 or 0 (binary)
    """
    return np.all((array == 1) | (array == 0))