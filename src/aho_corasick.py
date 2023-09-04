from typing import Collection


class ACNode:
    def __init__(self, value: str | None = None):
        self.value = value
        self.children: dict[str, ACNode] = {}
        self.suffix_link: ACNode | None = None


class AhoCorasick:
    """Structure used to check a known set of strings is contained in an arbitrary superstring.

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
        self.root = ACNode()
        if "" in strings:
            self.root.value = ""

        current_nodes_by_string = {string: self.root for string in strings}

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
                    child_node = ACNode()
                    current_node.children[current_char] = child_node
                    child_node.suffix_link = self._move_forward_from_node(
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

    def _move_forward_from_node(self, node: ACNode | None, char: str):
        while node != None:
            if char in node.children:
                return node.children[char]
            node = node.suffix_link

        # We have failed every recursive check, landing at the 'None'
        # suffix link of the root node.
        return self.root

    def find_substrings_in_superstring(self, superstring: str):
        found_substrings = set()
        if self.root.value is not None:
            found_substrings.add("")

        current_nodes = {self.root}
        for char in superstring:
            next_nodes = {self.root}
            for node in current_nodes:
                next_node = self._move_forward_from_node(node, char)
                if next_node.value is not None:
                    found_substrings.add(next_node.value)
                next_nodes.add(next_node)
            current_nodes = next_nodes

        return found_substrings
