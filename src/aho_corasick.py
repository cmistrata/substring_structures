class ACNode:
    creation_time_counter = 0

    def __init__(self, value: str | None = None):
        self.value = value
        self.children: dict[str, ACNode] = {}
        self.suffix_link: ACNode | None = None
        self._creation_time = ACNode.creation_time_counter
        ACNode.creation_time_counter += 1

    def __hash__(self) -> int:
        return self._creation_time


class AhoCorasick:
    def __init__(self, strings: list[str]):
        self.root = ACNode()
        current_nodes_by_string_index = [self.root] * len(strings)

        current_char_index = 0
        while any(current_char_index < len(string) for string in strings):
            for string_index, string in enumerate(strings):
                if current_char_index >= len(string):
                    continue
                current_char = string[current_char_index]
                current_node_of_string = current_nodes_by_string_index[string_index]

                # Add a new child node if it does not already exist.
                if current_char not in current_node_of_string.children:
                    child_node = ACNode()
                    current_node_of_string.children[current_char] = child_node
                    child_node.suffix_link = self._move_forward_from_node(
                        node=current_node_of_string.suffix_link,
                        char=current_char,
                    )
                else:
                    child_node = current_node_of_string.children[current_char]

                # Set the value of the child node to the current string if
                # we have reached the end of the string.
                at_last_char_of_string = current_char_index == len(string) - 1
                if at_last_char_of_string:
                    child_node.value = string

                current_nodes_by_string_index[string_index] = child_node

            current_char_index += 1

    def _move_forward_from_node(self, node: ACNode | None, char: str):
        while node != None:
            if char in node.children:
                return node.children[char]
            node = node.suffix_link

        # We have failed every recursive check, landing at the 'None'
        # suffix link of the root node.
        return self.root

    def list_substrings_in_superstring(self, superstring: str):
        found_substrings = set()
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
