# -*- coding: utf-8 -*-


"""
Utility functions for manipulating lists and NumPy arrays.
"""


# External libraries
from math import gcd
from typing import TypeVar

import numpy as np
from numpy.typing import NDArray


# Internal libraries


T = TypeVar("T")
U = TypeVar("U")


# =============================================================================
# General data functions
# =============================================================================


def sort_data(
    primary: list[T] | NDArray,
    secondary: list[U] | NDArray | None = None,
) -> list[T] | NDArray | tuple[list[T], list[U]] | tuple[NDArray, NDArray]:
    """Sort data according to the values in a primary sequence.

    If only ``primary`` is provided, its values are sorted directly.
    If ``secondary`` is provided, both sequences are reordered according
    to the sorting order of ``primary``.

    Parameters
    ----------
    primary : list or numpy.ndarray
        Values used for sorting.
    secondary : list or numpy.ndarray, optional
        Values associated with ``primary``. If provided, the sequence must
        have the same length and type as ``primary``.

    Returns
    -------
    list, numpy.ndarray, or tuple
        Sorted primary data if ``secondary`` is not provided.
        Otherwise, a tuple containing the sorted primary and corresponding
        secondary data.

    Raises
    ------
    TypeError
        If ``primary`` or ``secondary`` is not a supported type, or if their
        types differ.
    ValueError
        If ``primary`` and ``secondary`` do not have the same length.
    """
    if not isinstance(primary, (list, np.ndarray)):
        raise TypeError(
            "'primary' must be a list or a NumPy array."
        )

    if secondary is None:
        if isinstance(primary, np.ndarray):
            return np.sort(primary)

        return sorted(primary)

    if not isinstance(secondary, (list, np.ndarray)):
        raise TypeError(
            "'secondary' must be a list or a NumPy array."
        )

    if type(primary) is not type(secondary):
        raise TypeError(
            "'primary' and 'secondary' must have the same type."
        )

    if len(primary) != len(secondary):
        raise ValueError(
            "'primary' and 'secondary' must have the same length."
        )

    if isinstance(primary, np.ndarray):
        sorted_indices = np.argsort(primary)
        return primary[sorted_indices], secondary[sorted_indices]

    paired_values = sorted(zip(primary, secondary), key=lambda pair: pair[0])
    sorted_primary, sorted_secondary = zip(*paired_values)

    return list(sorted_primary), list(sorted_secondary)


# =============================================================================
# List functions
# =============================================================================


def find_first_max_pair(
    primary: list[T],
    secondary: list[U],
) -> tuple[T, U]:
    """Return the first maximum value and its associated value.

    The maximum value is searched for in ``primary``. The value at the same
    index in ``secondary`` is returned together with the maximum.

    Parameters
    ----------
    primary : list
        List in which the maximum value is searched.
    secondary : list
        List containing values associated with ``primary``.

    Returns
    -------
    tuple
        A tuple ``(maximum_value, associated_value)``.

    Raises
    ------
    TypeError
        If either argument is not a list.
    ValueError
        If either list is empty or if the lists have different lengths.
    """
    if not isinstance(primary, list) or not isinstance(secondary, list):
        raise TypeError(
            "'primary' and 'secondary' must both be lists."
        )

    if not primary or not secondary:
        raise ValueError(
            "'primary' and 'secondary' must not be empty."
        )

    if len(primary) != len(secondary):
        raise ValueError(
            "'primary' and 'secondary' must have the same length."
        )

    max_index = primary.index(max(primary))

    return primary[max_index], secondary[max_index]


def multiply_list(
    value: int | float,
    values: list[int | float],
) -> list[int | float]:
    """Multiply every element of a list by a scalar value.

    Parameters
    ----------
    value : int or float
        Multiplication factor.
    values : list of int or float
        Values to multiply.

    Returns
    -------
    list of int or float
        Result of the element-wise multiplication.
    """
    return [value * item for item in values]


def sum_lists(
    lists: list[list[int | float]],
) -> list[int | float]:
    """Compute the element-wise sum of multiple lists.

    Parameters
    ----------
    lists : list of list of int or float
        Lists containing the values to sum.

    Returns
    -------
    list of int or float
        Element-wise sum of the input lists.

    Raises
    ------
    ValueError
        If the input lists do not all have the same length.
    """
    if not lists:
        return []

    lengths = {len(values) for values in lists}

    if len(lengths) != 1:
        raise ValueError(
            "All lists must have the same length."
        )

    return [sum(values) for values in zip(*lists)]


def list_gcd(values: list[int | float]) -> int:
    """Calculate the greatest common divisor of a list of values.

    Non-integer values are rounded to the nearest integer before the
    greatest common divisor is calculated.

    Parameters
    ----------
    values : list of int or float
        Values for which the greatest common divisor is calculated.

    Returns
    -------
    int
        Greatest common divisor of the values.

    Raises
    ------
    ValueError
        If ``values`` is empty.
    """
    if not values:
        raise ValueError("'values' must not be empty.")

    integer_values = [int(round(value)) for value in values]

    return gcd(*integer_values)


# =============================================================================
# Vector functions
# =============================================================================


def select_value(
    vector: NDArray,
    value: int | float,
    absolute_tolerance: float = 1e-6,
    first_only: bool = False,
) -> tuple[NDArray, NDArray] | tuple[np.generic, np.integer]:
    """Select values approximately equal to a target value.

    Parameters
    ----------
    vector : numpy.ndarray
        One-dimensional array in which values are searched.
    value : int or float
        Target value.
    absolute_tolerance : float, optional
        Absolute tolerance used for the comparison. The default is ``1e-6``.
    first_only : bool, optional
        If ``True``, return only the first matching value and its index.
        The default is ``False``.

    Returns
    -------
    tuple
        Selected values and their indices. If ``first_only`` is ``True``,
        scalar values are returned instead of arrays.

    Raises
    ------
    ValueError
        If ``first_only`` is ``True`` and no matching value is found.
    """
    indices = np.where(
        np.isclose(vector, value, atol=absolute_tolerance)
    )[0]

    selected_values = vector[indices]

    if first_only:
        if indices.size == 0:
            raise ValueError(
                f"No value matching {value} was found."
            )

        return selected_values[0], indices[0]

    return selected_values, indices


def select_closest_value(
    vector: NDArray,
    value: int | float,
) -> tuple[np.generic, np.integer]:
    """Select the value closest to a target value.

    Parameters
    ----------
    vector : numpy.ndarray
        One-dimensional array in which the closest value is searched.
    value : int or float
        Target value.

    Returns
    -------
    tuple
        Closest value and its index.

    Raises
    ------
    ValueError
        If ``vector`` is empty.
    """
    if vector.size == 0:
        raise ValueError("'vector' must not be empty.")

    index = np.argmin(np.abs(vector - value))

    return vector[index], index


def select_values_in_range(
    vector: NDArray,
    min_value: int | float,
    max_value: int | float,
    step: int = 1,
    number: int | None = None,
) -> tuple[NDArray, NDArray[np.integer]]:
    """Select values contained within a specified range.

    Values are selected inclusively between ``min_value`` and ``max_value``.

    By default, every matching value is returned. ``step`` can be used to
    select one value every given number of indices. Alternatively, ``number``
    can be provided to select approximately evenly spaced values over the
    selected range.

    Parameters
    ----------
    vector : numpy.ndarray
        One-dimensional array containing the values.
    min_value : int or float
        Minimum value of the selection range.
    max_value : int or float
        Maximum value of the selection range.
    step : int, optional
        Select one value every ``step`` matching values. The default is 1.
        Ignored when ``number`` is provided.
    number : int, optional
        Number of approximately evenly spaced values to select. If the
        requested number is greater than the available number of values,
        all matching values are returned.

    Returns
    -------
    tuple of numpy.ndarray
        Selected values and their corresponding indices.

    Raises
    ------
    ValueError
        If ``min_value`` is greater than ``max_value``, ``step`` is less
        than 1, or ``number`` is not positive.
    """
    if min_value > max_value:
        raise ValueError(
            "'min_value' must be less than or equal to 'max_value'."
        )

    indices = np.where(
        (vector >= min_value) & (vector <= max_value)
    )[0]

    if indices.size == 0:
        return np.array([]), np.array([], dtype=int)

    if number is not None:
        if number <= 0:
            raise ValueError("'number' must be greater than 0.")

        if number < indices.size:
            positions = np.linspace(
                0,
                indices.size - 1,
                number,
                dtype=int,
            )

            indices = indices[positions]

    else:
        if step < 1:
            raise ValueError("'step' must be greater than or equal to 1.")

        indices = indices[::step]

    return vector[indices], indices


# =============================================================================
# Matrix functions
# =============================================================================


def select_row_or_column(
    matrix: NDArray,
    index: int,
    axis: int = 0,
) -> NDArray:
    """Select a row or column from a two-dimensional NumPy array.

    Parameters
    ----------
    matrix : numpy.ndarray
        Two-dimensional array.
    index : int
        Index of the row or column to select.
    axis : {0, 1}, optional
        Axis to select. ``0`` selects a row and ``1`` selects a column.
        The default is ``0``.

    Returns
    -------
    numpy.ndarray
        Selected row or column.

    Raises
    ------
    ValueError
        If ``matrix`` is not two-dimensional or ``axis`` is not 0 or 1.
    IndexError
        If ``index`` is outside the selected axis.
    """
    if matrix.ndim != 2:
        raise ValueError("'matrix' must be a two-dimensional array.")

    if axis not in (0, 1):
        raise ValueError("'axis' must be either 0 or 1.")

    if index < 0:
        raise IndexError("'index' must be non-negative.")

    if index >= matrix.shape[axis]:
        raise IndexError(
            f"Index {index} is out of bounds for axis {axis} "
            f"with size {matrix.shape[axis]}."
        )

    if axis == 0:
        return matrix[index, :]

    return matrix[:, index]