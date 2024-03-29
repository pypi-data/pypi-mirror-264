# Qoin provides random number generation using quantum computing.
# Copyright (C) 2024  Amir Ali Malekani Nezhad

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

__all__ = ['QRNG']

from collections.abc import Iterable
from typing import Any
import math

# Import `Qiskit` modules
from qiskit import QuantumCircuit
from qiskit.primitives import BackendSampler
from qiskit_aer.aerprovider import AerSimulator


class QRNG:
    """ `QRNG` class provides random number generation using quantum computing.
    """
    def __init__(self) -> None:
        """ Initialize a `QRNG` instance.
        """
        self._backend = BackendSampler(AerSimulator())

    def randint(self,
                lowerbound: int,
                upperbound: int) -> int:
        """ Generate a random integer from [lowerbound, upperbound).

        Parameters
        ----------
        `lowerbound` (int):
            The lowerbound of the selection.
        `upperbound` (int):
            The upperbound of the selection.

        Returns
        -------
        `random_int` (int): The random number generated from the selection.
        """
        # Define delta (difference between upperbound and lowerbound)
        delta = upperbound - lowerbound

        # Scale delta to the closest power of 2
        scale = delta/2 ** math.ceil(math.log2(delta))
        delta = int(delta/scale)

        # Calculate the number of qubits needed to represent the selection
        num_qubits = math.ceil(math.log2(delta))

        # Define the circuit
        circuit = QuantumCircuit(num_qubits, num_qubits)

        # Create a uniform distribution over all possible integers
        circuit.h(range(num_qubits))

        # Apply measurement
        circuit.measure(range(num_qubits), range(num_qubits))

        # Run the circuit
        result = self._backend.run(circuit, shots=1).result()

        # Extract the quasi-probability distribution from the first result
        quasi_dist = result.quasi_dists[0]

        # Convert the quasi-probability distribution to counts
        counts = {bin(k)[2:].zfill(num_qubits): int(v * 1) for k, v in quasi_dist.items()}

        # Sort the counts by their keys (basis states)
        counts = dict(sorted(counts.items()))

        # Postprocess measurement result
        random_int = int(list(counts.keys())[0], 2)

        # Scale the integer back
        random_int = int(random_int*scale)

        # shift random integer's range from [0;upperbound-lowerbound-1]
        # to [lowerbound;upperbound-1]
        random_int += lowerbound

        # Return random integer
        return random_int

    def randbin(self) -> bool:
        """ Generate a random boolean.

        Returns
        -------
        `random_bin` (bool): The random boolean.
        """
        return bool(self.randint(0, 2))

    def random(self,
               num_digits: int) -> float:
        """ Generate a random float between 0 and 1.

        Parameters
        ----------
        `num_digits` (int):
            The number of bits used to represent the angle divider.

        Returns
        -------
        `random_float`(float): The random generated float.
        """
        # Ensure that the number of digits is valid
        try:
            num_digits > 0
        except ValueError:
            raise ValueError("Number of digits must be greater than 0.")

        # Initialize the digit
        random_float = "0."

        for _ in range(num_digits):
            # Generate a random integer between 0 and 9
            random_float += str(self.randint(0, 9))

        # Return the random float
        return float(random_float)

    def choice(self,
               items: Iterable[Any]) -> Any:
        """ Choose a random element from the list of items.

        Parameters
        ----------
        `items` (Iterable[Any]):
            The list of items.

        Returns
        -------
        (Any): The item selected.
        """
        # Ensure that the items are iterable
        try:
            isinstance(items, Iterable)
        except TypeError:
            raise TypeError("Population must be a sequence or set.")

        return items[self.randint(0, len(items))]

    def choices(self,
                items: Iterable[Any],
                num_selections: int) -> Any | list[Any]:
        """ Choose random element(s) from the list of items.

        Parameters
        ----------
        `items` (Iterable[Any]):
            The list of items.
        `num_selections` (int):
            The number of selections.

        Returns
        -------
        (Any | list[Any]): The item(s) selected.
        """
        # Ensure that the number of selections is valid
        try:
            num_selections > 0
        except ValueError:
            raise ValueError("Sample larger than population or is negative.")

        # Ensure that the items are iterable
        try:
            isinstance(items, Iterable)
        except TypeError:
            raise TypeError("Population must be a sequence or set.")

        # Define indices list
        indices = []

        # If number of selections is 1, run `.choice` instead
        if num_selections == 1:
            return self.choice(items)

        # Generate the random indices
        indices = [self.randint(0, len(items)) for _ in range(num_selections)]

        # Return the selections
        return [items[i] for i in indices]

    def sample(self,
               items: Iterable[Any],
               num_selections: int) -> Any | list[Any]:
        """ Choose random element(s) from the list of items.

        Parameters
        ----------
        `items` (Iterable[Any]):
            The list of items.
        `num_selections` (int):
            The number of selections.

        Returns
        -------
        (Any | list[Any]): The item(s) selected.
        """
        # Ensure that the number of selections is valid
        try:
            num_selections > 0 and num_selections <= len(items)
        except ValueError:
            raise ValueError("Sample larger than population or is negative.")

        # Ensure that the items are iterable
        try:
            isinstance(items, Iterable)
        except TypeError:
            raise TypeError("Population must be a sequence or set.")

        # Define indices list
        indices = []

        # If number of selections is 1, run `.choice` instead
        if num_selections == 1:
            return self.choice(items)

        while True:
            # If the number of selections is met, break the loop
            if len(indices) == num_selections:
                break

            # Generate a random index
            random_index = self.randint(0, len(items))

            # If the random index generated is not unique, do not append it
            if random_index not in indices:
                indices.append(random_index)

        # Return the selections
        return [items[i] for i in indices]

    def shuffle(self,
                items: Iterable[Any]) -> list[Any]:
        """ Shuffle the list of items.

        Parameters
        ----------
        `items` (list[Any]):
            The list of items to shuffle.

        Returns
        -------
        None
        """
        # Ensure that the items are a list
        try:
            isinstance(items, Iterable)
        except TypeError:
            raise TypeError("The items must be a list.")

        return self.sample(items, len(items))