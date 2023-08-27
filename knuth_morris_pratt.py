"""Implementation of the Knuth-Morris-Pratt substring algorithm and underlying structure."""

NO_FALLBACK_FOUND = -1


class KnuthMorrisPratt:
    def __init__(self, w: str):
        self.string = w
        # List matching each prefix p1 to the next longest prefix/fallback p2 that is
        # a suffix of p1.
        self._fallback_length_by_prefix_length = build_fallback_structure(w)

    def contained_by(self, s: str) -> bool:
        """Check if self.string is a substring of superstring."""
        current_matched_prefix_length = 0
        for superstring_char in s:
            while current_matched_prefix_length != NO_FALLBACK_FOUND:
                next_string_char = self.string[current_matched_prefix_length]
                if next_string_char == superstring_char:
                    current_matched_prefix_length += 1
                    break

                # Fall back to the next longest prefix that is a suffix of the current prefix.
                current_matched_prefix_length = self._fallback_length_by_prefix_length[
                    current_matched_prefix_length
                ]
            else:
                current_matched_prefix_length = 0

            if current_matched_prefix_length == len(self.string):
                return True

        return False


def build_fallback_structure(w):
    fallback_length_by_prefix_length = [NO_FALLBACK_FOUND] * len(w)
    # The only suffix of a string of length 1 is a string of length 0.
    fallback_length_by_prefix_length[1] = 0

    for current_prefix_length in range(2, len(w)):
        char = w[current_prefix_length - 1]
        previous_prefix_length = current_prefix_length - 1
        fallback_prefix_length = fallback_length_by_prefix_length[
            previous_prefix_length
        ]

        while fallback_prefix_length != NO_FALLBACK_FOUND:
            char_after_fallback_prefix = w[fallback_prefix_length]
            if char_after_fallback_prefix == char:
                fallback_length_by_prefix_length[current_prefix_length] = (
                    fallback_prefix_length + 1
                )
                break
            fallback_prefix_length = fallback_length_by_prefix_length[
                fallback_prefix_length
            ]
        else:
            # If we fail to fall back to any prefix, we can use the prefix "", which
            # essentially represents starting from scratch again on the search.
            fallback_length_by_prefix_length[current_prefix_length] = 0

    return fallback_length_by_prefix_length
