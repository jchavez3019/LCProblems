from typing import *
from copy import deepcopy

class Node:
    def __init__(self, character: str, is_terminal: bool):
        self.character = character
        self.is_terminal = is_terminal
        # a node can only have 26 children since there are only 26 lowercase letters
        self.children = [None] * 26

class Trie:
    def __init__(self):
        self.root = Node("", False)

    def insert_word(self, word: str):
        curr_node = self.root
        for i, c in enumerate(word):
            is_terminal = i == len(word) - 1
            child_idx = ord(c) - ord('a')
            if curr_node.children[child_idx] is None:
                next_node = Node(c, is_terminal)
                curr_node.children[child_idx] = next_node
            else:
                next_node = curr_node.children[child_idx]
                next_node.is_terminal |= is_terminal
            curr_node = next_node

    def find_prefix(self, prefix: str, start_node: Node) -> Optional[Node]:
        if start_node is not None:
            curr_node = start_node
        else:
            curr_node = self.root

        for i, c in enumerate(prefix):
            child_idx = ord(c) - ord('a')
            if curr_node.children[child_idx] is None:
                # this prefix does not exist in the trie
                return None
            curr_node = curr_node.children[child_idx]

        # the prefix existed in the Trie and we can return its node
        return curr_node

class Solution:
    def findWords(self, board: List[List[str]], words: List[str], verbose: bool = False) -> List[str]:
        m = len(board)
        n = len(board[0])
        # result is the set of words we have found on the board
        trie = Trie()
        word_idx: Dict[str, int] = {}
        word_found = [False] * len(words)
        for i, word in enumerate(words):
            # insert the word into the trie
            trie.insert_word(word)
            word_idx[word] = i

        # returns the 2D adjacent neighbors of some idx (i, j)
        get_neighbors = lambda i, j : ((i,j-1), (i,j+1), (i-1,j), (i+1,j))
        # returns True if (i, j) is out of range on the board
        out_of_range = lambda i, j : i < 0 or i >= m or j < 0 or j >= n

        def _slide(idx: Tuple[int, int], prefix: str, path: set, trie_node: Node):
            i, j = idx

            if trie_node.is_terminal:
                # this is a complete word we have found
                word_found[word_idx[prefix]] = True

            for a, b in get_neighbors(i, j):
                if out_of_range(a, b) or (a,b) in path:
                    # continue if we are out of range or
                    # this index was already visited in the path
                    continue
                next_node = trie.find_prefix(board[a][b], trie_node)
                if next_node is not None:
                    # next position (a, b) still forms a valid prefix, explore it and add it
                    # to the path
                    new_path = path.copy()
                    new_path.add((a,b))
                    _slide((a,b), prefix + board[a][b], new_path, next_node)

        for i in range(m):
            for j in range(n):
                # iterate through the board to start our prefix from different positions
                start_idx = (i, j)
                start_node = trie.find_prefix(board[i][j], None)
                if start_node is not None:
                    _slide(start_idx, board[i][j], set(((i,j),)), start_node)

        return [word for i, word in enumerate(words) if word_found[i]]

def main():
    test_cases = {
        "1": {
            "board": [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]],
            "words": ["oath","pea","eat","rain"],
            "expected": ["oath","eat"],
        },
        "2": {
            "board": [["a","b"],["c","d"]],
            "words": ["abcb"],
            "expected": [],
        },
        "3": {
            "board": [["a","a"]],
            "words": ["aaa"],
            "expected": [],
        },
        "4": {
            "board": [["a","a"],["a","a"]],
            "words": ["aaaaa"],
            "expected": [],
        },
        "5": {
            "board": [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]],
            "words": ["oath","pea","eat","rain","hklf", "hf"],
            "expected": ["oath","eat","hklf","hf"],
        },
    }

    solution = Solution()

    for tk, targs in test_cases.items():
        expected = targs.pop("expected", None)
        ret = solution.findWords(**targs, verbose=True)
        if expected is not None:
            passed = ret == expected
        else:
            passed = None
        print(f"test case {tk}: {targs}\nReturned: {ret}, Expected: {expected}\nPassed:{passed}\n")

if __name__ == "__main__":
    main()