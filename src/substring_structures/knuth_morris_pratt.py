"""Implementation of the Knuth-Morris-Pratt substring algorithm and underlying structure."""

_NO_FALLBACK_FOUND = -1
_UNSET = -2


class KnuthMorrisPratt:
    """Structure based on the Knuth-Morris-Pratt algorithm for substring search.

    This class will preprocess a string W of length M in O(M) time so that you can check
    if its a substring of another string S of length N in O(N) time using `KnuthMorrisPratt(w).contained_by(s)`.

    It does this by generating a structure of string W that allows you to "fallback" from a longer prefix of
    W to a shorter prefix of W on a character mismatch when searching S. The code here
    is based on descriptions at https://www.charliemistrata.com/posts/knuth-morris-pratt.

    >>> KnuthMorrisPratt("bababooie")
    KnuthMorrisPratt(string='bababooie', calculated fallback structure=[-1, 0, 0, 1, 2, 3, 0, 0, 0])
    # prefix_fallback[0] = -1 # "" has no suffix
    # prefix_fallback[1] = 0 # "b" -> ""
    # prefix_fallback[2] = 0 # "ba" -> ""
    # prefix_fallback[3] = 1 # "bab" -> "b"
    # prefix_fallback[4] = 2 # "baba" -> "ba"
    # prefix_fallback[5] = 3 # "babab" -> "bab"
    # prefix_fallback[6] = 0 # "bababo" -> ""
    # ...

    >>> baba = KnuthMorrisPratt("baba")
    >>> baba.contained_by("ababab")
    True
    >>> baba.contained_by("keke")
    False
    """

    def __init__(self, w: str):
        self.string = w
        if w == "":
            self._fallback_length_by_prefix_length = []
            return
        # List matching each prefix p1 to the next longest prefix/fallback p2 that is
        # a suffix of p1, using the prefix lengths as keys.
        # Using a special variable '_UNSET' is not necessary but is done here
        # is done here to clearly indicate that the initial values are meaningless.
        self._fallback_length_by_prefix_length = [_UNSET] * len(self.string)

        # A string of length 0 ("") will not have any suffix.
        self._fallback_length_by_prefix_length[0] = _NO_FALLBACK_FOUND
        for current_prefix_length in range(1, len(self.string)):
            char = self.string[current_prefix_length - 1]
            previous_prefix_length = current_prefix_length - 1
            fallback_of_previous_prefix_length = self._fallback_length_by_prefix_length[
                previous_prefix_length
            ]
            self._fallback_length_by_prefix_length[
                current_prefix_length
            ] = self._move_forward_from_prefix(fallback_of_previous_prefix_length, char)

    def _move_forward_from_prefix(self, prefix_length: int, char: str):
        """'Move forward' from a prefix with length `prefix_length` using `char`. This involves repeatedly
        falling back to prefixes and seeing if the prefix is followed by `char` until it is or we reach the
        beginning of the string without finding any prefixes followed by `char`.
        """
        while prefix_length != _NO_FALLBACK_FOUND:
            char_after_fallback_prefix = self.string[prefix_length]
            if char_after_fallback_prefix == char:
                return prefix_length + 1
            prefix_length = self._fallback_length_by_prefix_length[prefix_length]
        # If we fail to fall back to any prefix, we can use the prefix "", which
        # essentially represents starting from scratch again on the search.
        return 0

    def contained_by(self, s: str) -> bool:
        """Check if `self.string` is a substring of superstring `s`."""
        if self.string == "":
            return True
        current_matched_prefix_length = 0
        for superstring_char in s:
            current_matched_prefix_length = self._move_forward_from_prefix(
                current_matched_prefix_length, superstring_char
            )
            if current_matched_prefix_length == len(self.string):
                return True

        return False

    def __str__(self):
        return f"KnuthMorrisPratt(string='{self.string}', calculated fallback structure={self._fallback_length_by_prefix_length})"

    def __repr__(self):
        return self.__str__()
