"""Implementation of the Aho–Corasick algorithm and underlying structure."""


from typing import Collection


class _ACNode:
    def __init__(self, value: str | None = None):
        self.value = value
        self.children: dict[str, _ACNode] = {}
        self.suffix_link: _ACNode | None = None


class AhoCorasick:
    """
    Structure used to check a known set of strings is contained in an arbitrary superstring.

    Based on the Aho-Corasick algorithm (https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm),
    this structure can be computed in O(N) time for a set of strings "SubstringsSet" of total length N. It can
    then be used to efficiently check which strings in "SubstringsSet" are in a larger string "superstring"
    using the `find_substrings_in_superstring(superstring)` method.
    """

    def __init__(self, strings: Collection[str]):
        if isinstance(strings, str):
            raise ValueError(
                f"'`strings` should be a collection of strings but was passed a single string '{strings}'."
            )
        self.strings = strings
        self._root = _ACNode()
        if "" in strings:
            self._root.value = ""

        current_nodes_by_string = {string: self._root for string in strings}

        current_char_index = 0
        while any(current_nodes_by_string):
            strings_shorter_than_current_char_index = []
            for string, current_node in current_nodes_by_string.items():
                if current_char_index >= len(string):
                    strings_shorter_than_current_char_index.append(string)
                    continue

                current_char = string[current_char_index]

                # Add a new child node if it does not already exist.
                if current_char not in current_node.children:
                    child_node = _ACNode()
                    current_node.children[current_char] = child_node
                    child_node.suffix_link, _ = self._move_forward_from_node(
                        node=current_node.suffix_link,
                        char=current_char,
                    )
                else:
                    child_node = current_node.children[current_char]

                # Set the value of the child node to the current string if
                # we have reached the end of the string.
                at_last_char_of_string = current_char_index == len(string) - 1
                if at_last_char_of_string:
                    child_node.value = string

                current_nodes_by_string[string] = child_node

            for (
                string_shorter_than_current_char_index
            ) in strings_shorter_than_current_char_index:
                current_nodes_by_string.pop(string_shorter_than_current_char_index)
            current_char_index += 1

    def _move_forward_from_node(
        self, node: _ACNode | None, char: str
    ) -> tuple[_ACNode, set[str]]:
        """
        Move forward from node using char, traveling along suffix links where necessary.
        Return a tuple of the node we arrive at, as well the values of any nodes we traveled along
        on the way via suffix links for use during substring search.
        """
        traversed_substrings = set()

        while node != None:
            if node.value is not None:
                traversed_substrings.add(node.value)

            if char in node.children:
                return node.children[char], traversed_substrings
            node = node.suffix_link

        # We have failed every recursive check, landing at the 'None'
        # suffix link of the root node.
        return self._root, traversed_substrings

    def find_substrings_in_superstring(self, superstring: str) -> set[str]:
        """Find which of `self.strings` occurs in `superstring`."""
        # Add a terminating character to the superstring we don't expect to be in any of the substrings.
        # This way, when we try to match this character, we will be forced to travel along suffix links to the roots,
        # as traveling along nodes is how we find and add found substrings.
        superstring += "🍁"

        found_substrings = set()
        if self._root.value is not None:
            found_substrings.add("")

        current_node = self._root
        for char in superstring:
            current_node, traversed_substrings = self._move_forward_from_node(
                current_node, char
            )
            found_substrings |= traversed_substrings

        return found_substrings

    def __str__(self) -> str:
        return f"AhoCorasick(strings={self.strings})"

    def __repr__(self) -> str:
        return self.__str__()
