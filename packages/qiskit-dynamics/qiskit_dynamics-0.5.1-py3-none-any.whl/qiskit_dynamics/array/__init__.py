# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
===========================================
Array Module (:mod:`qiskit_dynamics.array`)
===========================================

.. currentmodule:: qiskit_dynamics.array


.. warning::

    The ``array`` and ``dispatch`` submodules of Qiskit Dynamics have been deprecated as of version
    0.5.0. The use of the ``Array`` class is no longer required to work with different array
    libraries in Qiskit Dynamics, and is broken in some cases. Refer to the :ref:`user guide entry
    on using different array libraries with Qiskit Dynamics <how-to use different array libraries>`.
    Users can now work directly with the supported array type of their choice, without the need to
    wrap them to enable dispatching. The ``array`` and ``dispatch`` submodules will be removed in
    version 0.6.0.

This module contains an :class:`Array` class that wraps N-dimensional array objects from different
libraries. It enables working with different array libraries through a common NumPy-based interface,
along with other functionality for writing array-library agnostic code.


Array Class
===========

The :class:`Array` class provides a NumPy compatible wrapper to supported Python array libraries.
NumPy functions applied to an :class:`Array` class instance will be dispatched to the corresponding
function for the current Array backend, if a compatible function has been specified in the
:mod:`qiskit_dynamics.dispatch` system.

The following array libraries have built in support for the
:mod:`qiskit_dynamics.dispatch` module:

* `NumPy <https://numpy.org/>`_
* `JAX <https://github.com/google/jax>`_

Basic Usage
-----------

.. jupyter-execute::
    :hide-code:
    
    # suppress deprecation warnings
    import warnings
    warnings.simplefilter('ignore', category=DeprecationWarning)

When using the default ``numpy`` backend :class:`Array`, objects can be used interchangably with
``numpy.ndarray``. When ``numpy`` functions are applied to an :class:`Array` object the return type
will be an :class:`Array` instead of an ``numpy.ndarray``.

.. jupyter-execute::

    from qiskit_dynamics.array import Array
    import numpy as np

    # Initialize an Array
    a = Array(np.arange(10))

    # Apply numpy ufuncs
    np.cos(a) + 1j * np.sin(a)

For the JAX Array backend, only Numpy functions that have a corresponding function in the ``jax``
library that have been registered with the dispatch module can be applied to the functions. Trying
to apply an unsupported ``numpy`` function to these arrays will raise an exception.

Default Backend
---------------

When initializing a new :class:`Array`, the ``backend`` kwarg is used to specify which array backend
to use. This will convert the input data to an array of this backend if required. If
``backend=None``, the default backend will be used. The initial default backend is always set to
``"numpy"``.

The current default backend can be viewed by using the class method :meth:`Array.default_backend`. A
different default backend can be set for all :meth:`Array` instances by using the
:meth:`Array.set_default_backend` class method.

Attributes and Methods
----------------------

The :class:`Array` class exposes the same methods and attributes of the wrapped array class and adds
two additional attributes:

* :attr:`~Array.data` which returns the wrapped array object
* :attr:`~Array.backend` which returns the backend string of the wrapped array.

All other attributes and methods of the wrapped array are accessible through this class, but with
any array return types wrapped into :class:`Array` objects. For example:

.. jupyter-execute::

    # Call an numpy.ndarray method
    a.reshape((2, 5))


Array Initialization
--------------------

An :class:`Array` object can be initialized as ``Array(data)`` from any ``data`` that is:

1. An ``array`` object of one of the supported backends.
2. An object that can be used to initialize the backend array.
3. An object of a class that defines a ``__qiskit_array__`` method with the
   following signature:

    .. code-block:: python

        def __qiskit_array__(self,
                             dtype: Optional[any] = None,
                             backend: Optional[str]=None) -> Array:
            # conversion from class to Array

The :meth:`Array.__init__` method has optional kwargs:

* ``dtype`` (``any``): Equivalent to the ``numpy.array`` ``dtype`` kwarg. For other array backends,
  the specified ``dtype`` must be supported. If not specified, the ``dtype`` will
  be inferred from the input data.
* ``order`` (``str``): Equivalent to the ``numpy.array`` ``order`` kwarg. For other array
  backends, the specified order value must be supported.
* ``backend`` (``str``): The array backend to use. If not specified this will be inferred from the
  input data type if it is a backend array instance, otherwise it will be the
  :func:`default_backend`.


Using Arrays with other Libraries
=================================

The :class:`Array` class is intended to be used with array functions in
Python libraries that work with any of the supported Array backends.

Wrapping Functions
------------------

Functions from other libraries can be wrapped to work with Array objects using
the :func:`wrap` function as

.. code-block:: python

    from qiskit_dynamics.array import Array, wrap

    # Some 3rd-party library
    import library

    # Wrap library function f
    f = wrap(library.f)

    # Apply f to an Array
    a = Array([0, 1, 2, 4])
    b = f(a)

The wrapped function will automatically unwrap any :class:`Array` args and kwargs
for calling the wrapped function. If the result of the function is a backend array
or an instance of a class that defines a ``__qiskit_array__`` method, the wrapped
function will return this as an Array object. Similarly, if the result is a tuple
this conversion will be applied to each element of the tuple where appropriate.

Wrapping Decorators
-------------------

The :func:`wrap` function can also be used to wrap function decorators by setting
the ``decorator=True`` kwarg.

For example, to wrap autograd and jit decorators from the JAX library to work with
Array functions, we can do the following

.. code-block:: python

    import jax

    jit = wrap(jax.jit, decorator=True)
    grad = wrap(jax.grad, decorator=True)
    value_and_grad = wrap(jax.value_and_grad, decorator=True)

    f = jit(obj)
    g = grad(obj)
    h = value_and_grad(obj)

.. note:

    Setting ``decorator=True`` when calling :func:`wrap` requires that the
    signature of the function being wrapped is
    ``func(f: Callable, ...) -> Callable``. Using it is equivalent to nested
    wrapping

    .. code-block:: python

        f_wrapped = wrap(func, decorator=True)(f)

    is equivalent to

    .. code-block:: python

        f_wrapped = wrap(wrap(func)(f))


Array Class
===========

.. autosummary::
    :toctree: ../stubs/

    Array

Array Functions
===============

.. autosummary::
    :toctree: ../stubs/

    wrap
"""


# Import Array
from .array import Array

# Import wrapper function
from .wrap import wrap

# Monkey patch quantum info
# pylint: disable= wrong-import-position
from .patch_qi import *
