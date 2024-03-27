import logging
import numpy as np
from numpy.typing import NDArray
from typing import Optional

from .errors import ConstraintSizeError, MaximumConstraintLimitError
from .numpy_util import convert_to_float32, is_ndarray_binary

log = logging.getLogger("TitanQ")

class Constraints:
    def __init__(self, variable_size: int) -> None:
        self._variable_size = variable_size
        self._constraint_weights = None
        self._constraint_bounds = None


    def add_constraint(self, constraint_mask: NDArray, cardinalities: Optional[np.ndarray]):
        """
        Add a constraint to the existing ones

        :param constraint_mask: constraint mask used to create constraint weights and constraint bounds
        :param cardinalities: Optional, if provided will multiply the constraint bounds

        :raises ValueError: _description_
        :raises MaximumConstraintLimitError: _description_
        :raises ValueError: _description_
        """
        if constraint_mask.shape[1] != self._variable_size:
            raise ConstraintSizeError(
                "Constraint mask shape does not match the variable size. " \
                f"Constraint size: {constraint_mask.shape[1]}, Variable size: {self._variable_size}")

        if self._constraints_rows() + constraint_mask.shape[0] > self._variable_size:
            raise MaximumConstraintLimitError(
                "Cannot add additional constraints. The limit of constraints have been reached. " \
                f"Number of constraints: {self._constraints_rows()}, Variable size: {self._variable_size}"
            )

        # if the supplied constraint mask is not binary
        if not is_ndarray_binary(constraint_mask):
            raise ValueError(f"Cannot add a constraint if the values are not in binary.")

        constraint_mask = convert_to_float32(constraint_mask)

        self._constraint_weights = self._append_constraint_weights(constraint_mask)

        constraint_bounds = self._create_constraint_bounds(constraint_mask, cardinalities)
        self._constraint_bounds = self._append_constraint_bounds(constraint_bounds)


    def weights(self):
        """
        :return: The weights constraints.
        """
        return self._constraint_weights


    def bounds(self):
        """
        :return: The bounds constraints.
        """
        return self._constraint_bounds


    def _append_constraint_weights(self, constraint_weights_to_add: NDArray[np.float32]) -> NDArray[np.float32]:
        """
        Appends ``constraint_weights_to_add`` to the existing one.
        If constriant weights is set to None, it will return itself

        :return: The new constraint weights matrix
        """
        if self._constraint_weights is None:
            return constraint_weights_to_add
        return np.append(self._constraint_weights, constraint_weights_to_add, axis=0)


    def _append_constraint_bounds(self, constraint_bounds_to_add: NDArray[np.float32]) -> NDArray[np.float32]:
        """
        Appends ``constraint_bounds_to_add`` to the existing one.
        If constriant bounds is set to None, it will return itself

        :return: The new constraint weights matrix
        """
        if self._constraint_bounds is None:
            return constraint_bounds_to_add
        return np.append(self._constraint_bounds, constraint_bounds_to_add, axis=0)


    def _constraints_rows(self) -> int:
        """
        :return: The number of constraints (row) already set, 0 if never set
        """
        if self._constraint_weights is None:
            return 0
        return self._constraint_weights.shape[0]


    def _create_constraint_bounds(self, array: np.ndarray, cardinalities: Optional[np.ndarray] = None) -> NDArray[np.float32]:
        """
        Creates constraint bounds from given array of (M, 2).

        :param array: input constraint mask of shape (M, N).
        :type array: a NumPy 2-D dense ndarray.

        :param cardinalities: The constraint_rhs vector of shape (M,) where M is the number of constraints.
        :type cardinalities:  a NumPy 1-D ndarray (must be unsigned integer).

        :return: Array of type float32
        :rtype: np.NDArray[np.float32]
        """
        if cardinalities is not None:
            if cardinalities.shape[0] != array.shape[0]:
                raise ValueError(
                    f"Cannot set constraints if cardinalities shape is not the same as the expected shape of this model." \
                    f" Got cardinalities shape: {cardinalities.shape[1]}, constraint mask shape: {array.size()}.")

            # cardinalities should be a NumPy 2-D dense ndarray
            if cardinalities.ndim != 1:
                raise ValueError(f"Cannot set constraints if cardinalities is not a NumPy 2-D dense ndarray")

            # all cardinalities should be integers
            if not np.issubdtype(cardinalities.dtype, np.integer):
                raise ValueError("Found cardinalities data types not integer")

            # all cardinalities should be positive
            if not np.all(cardinalities > 0):
                raise ValueError("Found cardinalities data types not unsigned integer")

        constraint_bounds = np.ones((array.shape[0],2), dtype=np.float32)

        # if cardinalities are provided, multiply the values with for each constraint bound
        if cardinalities is not None:
            reshaped_cardinalities = np.repeat(cardinalities, 2).reshape(-1, 2)
            constraint_bounds = np.multiply(constraint_bounds, reshaped_cardinalities).astype(np.float32)
            self._validate_cardinalities(array, constraint_bounds)

        return constraint_bounds


    def _validate_cardinalities(self, array: np.ndarray, cardinalities_constraint_bounds: np.ndarray):
        """
        Validates each row's sum of a binary array against corresponding values in a cardinalities array.
        It prints warnings if the sum is equal to the cardinality and raises an error if the sum is less than the cardinality.

        :param array: input constraint mask of shape (M, N).
        :type array: a NumPy 2-D dense ndarray.

        :param cardinalities: The constraint_rhs vector of shape (M,2) where M is the number of constraints.
        :type cardinalities:  a NumPy 2-D ndarray (must be unsigned integer).
        """
        binary_sums = np.sum(array, axis=1)
        cardinalities = cardinalities_constraint_bounds[:, 0]

        equal_indices = np.where(binary_sums == cardinalities)[0]
        less_indices = np.where(binary_sums < cardinalities)[0]

        if equal_indices.size > 0:
            log.warning(f" The sum of rows {', '.join(map(str, equal_indices))} in the binary array equals its corresponding cardinality.")

        if less_indices.size > 0:
            raise ValueError(f"The sum of rows {', '.join(map(str, less_indices))} in the binary array is less than its corresponding cardinality.")


    def set_constraint_matrices(
        self,
        constraint_weights: np.ndarray,
        constraint_bounds: np.ndarray
    ) -> None:
        """
        Overides add_constraint and manually set the constraint weights and the constraint bounds

        NOTE: Should be removed when equality and inequality constraints are added

        :param constraint_weights: already formed constraint weights
        :param constraint_bounds: already formed constraint bounds
        """
        weights_shape = constraint_weights.shape
        bounds_shape = constraint_bounds.shape

        # validate shapes
        if len(weights_shape) != 2:
            raise ValueError(f"constraint_weights should be a 2d matrix. Got something with shape: {weights_shape}")

        if len(bounds_shape) != 2:
            raise ValueError(f"constraint_bounds should be a 2d matrix. Got something with shape: {bounds_shape}")

        if weights_shape[1] != self._variable_size:
            raise ValueError(f"constraint_weights shape does not match variable size. Expected (M, {self._variable_size}) where M is the number of constraints")
        n_constraints = weights_shape[0]

        if n_constraints == 0:
            raise ValueError("Need at least 1 constraints")

        if bounds_shape[0] != n_constraints:
            raise ValueError(f"constraint_bounds shape does not match constraint_weights size. Expected ({n_constraints}, 2)")

        if bounds_shape[1] != 2:
            raise ValueError(f"constraint_bounds shape is expected to be ({n_constraints}, 2)")

        if constraint_weights.dtype != np.float32:
            raise ValueError(f"Weights constraints vector dtype should be np.float32")

        if constraint_bounds.dtype != np.float32:
            raise ValueError(f"Bounds constraints vector dtype should be np.float32")

        self._constraint_weights = constraint_weights
        self._constraint_bounds = constraint_bounds
