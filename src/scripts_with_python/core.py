from __future__ import annotations

from typing import Dict, Hashable, Iterator, Optional


class Bag:
    """A multiset: an unordered collection that tracks element multiplicity.

    Only hashable elements may be stored, because multiplicities are kept in a
    dict keyed by element.  This mirrors the constraint of
    :class:`collections.Counter` and keeps insert / remove / count at O(1).

    Counts are always non-negative integers.  Removing more copies of an
    element than are present is a :class:`ValueError`, not a silent clamp to
    zero — a multiset is not a ledger that tolerates negative balances.
    """

    __slots__ = ("_counts",)

    def __init__(self, iterable: Optional[Iterator[Hashable]] = None) -> None:
        self._counts: Dict[Hashable, int] = {}
        if iterable is not None:
            for element in iterable:
                self.insert(element)

    # ------------------------------------------------------------------ #
    # Core operations                                                    #
    # ------------------------------------------------------------------ #

    def insert(self, element: Hashable, times: int = 1) -> None:
        """Add ``times`` copies of ``element`` to the bag.

        ``times`` must be a non-negative integer.  ``insert(x, 0)`` is legal
        and does nothing — useful when the count comes from arithmetic that
        can legitimately produce zero.
        """
        if not isinstance(times, int) or isinstance(times, bool):
            raise TypeError("times must be an int, not bool")
        if times < 0:
            raise ValueError("times must be non-negative")
        if times == 0:
            return
        self._counts[element] = self._counts.get(element, 0) + times

    def remove(self, element: Hashable, times: int = 1) -> None:
        """Remove ``times`` copies of ``element``.

        Raises :class:`ValueError` when more copies are removed than exist.
        If the count reaches zero the key is deleted so that ``element in bag``
        becomes ``False``.
        """
        if not isinstance(times, int) or isinstance(times, bool):
            raise TypeError("times must be an int, not bool")
        if times < 0:
            raise ValueError("times must be non-negative")
        if times == 0:
            return
        current = self._counts.get(element, 0)
        if times > current:
            raise ValueError(
                f"cannot remove {times} of {element!r}: only {current} present"
            )
        remaining = current - times
        if remaining == 0:
            del self._counts[element]
        else:
            self._counts[element] = remaining

    def count(self, element: Hashable) -> int:
        """Return the multiplicity of ``element`` (0 if absent)."""
        return self._counts.get(element, 0)

    # ------------------------------------------------------------------ #
    # Convenience / dunder                                              #
    # ------------------------------------------------------------------ #

    def __contains__(self, element: Hashable) -> bool:
        return element in self._counts

    def __len__(self) -> int:
        """Total number of elements counted with multiplicity."""
        return sum(self._counts.values())

    def __iter__(self) -> Iterator[Hashable]:
        """Iterate each element once per copy it contributes."""
        for element, n in self._counts.items():
            for _ in range(n):
                yield element

    def __repr__(self) -> str:
        return f"Bag({dict(self._counts)!r})"

    def __eq__(self, other: object) -> bool:
        """Two bags are equal iff every element has the same multiplicity."""
        if not isinstance(other, Bag):
            return NotImplemented
        return self._counts == other._counts
