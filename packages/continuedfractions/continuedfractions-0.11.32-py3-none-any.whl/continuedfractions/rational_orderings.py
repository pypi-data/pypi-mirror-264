__all__ = [
	'farey_sequence',
]


# -- IMPORTS --

# -- Standard libraries --
import copy
import sys

from itertools import chain, pairwise, starmap, zip_longest
from fractions import Fraction

from pathlib import Path

# -- 3rd party libraries --

# -- Internal libraries --
sys.path.insert(0, str(Path(__file__).parent.parent))

from continuedfractions.continuedfraction import ContinuedFraction


_farey_cache = {1: (Fraction(0, 1), Fraction(1, 1))}


def farey_sequence(n: int) -> tuple[ContinuedFraction]:
	"""Returns a tuple of rational numbers forming the Farey sequence of order :math:`n`.

	The Farey sequence :math:`F_n` of order :math:`n` is an (ordered) sequence
	of rational numbers which is defined recursively as follows:

	.. math::

	   \\begin{align}
	   F_1 &= \\left(\\frac{0}{1}, \\frac{1}{1}\\right) \\\\
	   F_k &= \\left(\\frac{p}{q}\\right) \\text{ s.t. } (p, q) = 1 \\text{ and } q \\leq n,
	          \\hskip{3em} k \\geq 2
	   \\end{align}

	The restriction :math:`(p, q) = 1` (meaning :math:`p` and :math:`q` must
	be coprime) on the numerators and denominators of the fractions in
	:math:`F_n` means it contains exactly one single fraction, and no more, for
	every positive integer :math:`q \\leq n`. 

	This means that the number of elements :math:`N(n)` in :math:`F_n` is given by:

	.. math::

	   N(n) = 1 + \\phi(1) + \\phi(2) + \\cdots + \\phi(n) = 1 + \\sum_{k = 1}^n \\phi(k)

	where :math:`phi(k)` is `Euler's totient function <https://en.wikipedia.org/wiki/Euler%27s_totient_function>`_.

	The first five Farey sequences are:

	.. math::

	   \\begin{align}
	   F_1 &= \\left( \\frac{0}{1}, \\frac{1}{1} \\right) \\\\
	   F_2 &= \\left( \\frac{0}{1}, \\frac{1}{2}, \\frac{1}{1} \\right) \\\\
	   F_3 &= \\left( \\frac{0}{1}, \\frac{1}{3}, \\frac{1}{2}, \\frac{2}{3}, \\frac{1}{1} \\right) \\\\
	   F_4 &= \\left( \\frac{0}{1}, \\frac{1}{4}, \\frac{1}{3}, \\frac{1}{2}, \\frac{2}{3}, \\frac{3}{4}, \\frac{1}{1} \\right) \\\\
	   F_5 &= \\left( \\frac{0}{1}, \\frac{1}{5}, \\frac{1}{4}, \\frac{1}{3}, \\frac{2}{5}, \\frac{1}{2}, \\frac{3}{5}, \\frac{2}{3}, \\frac{3}{4}, \\frac{4}{5}, \\frac{1}{1} \\right)
	   \\end{align}

	Farey sequences have quite interesting properties and relations, as
	described `here <https://en.wikipedia.org/wiki/Farey_sequence>`_.

	Parameters
	----------
	n : int:
		The order of the Farey sequence.

	Returns
	-------
	tuple[ContinuedFraction]
		A tuple of ``ContinuedFraction`` instances representing the elements of
		the Farey sequence.
	"""
	cached = _farey_cache.get(n)

	if cached:
		yield from cached
	else:
		m = max(_farey_cache)
		highest_predecessor = _farey_cache[m]

		this_sequence = copy.copy(highest_predecessor)

		while m < n:
			m += 1
			mediants = starmap(left_mediant, pairwise(this_sequence))
			this_sequence = tuple(filter(
				lambda fraction: fraction is not None and fraction.denominator <= n,
				chain.from_iterable(zip_longest(this_sequence, mediants))
			))
			_farey_cache[m] = this_sequence

		yield from this_sequence
