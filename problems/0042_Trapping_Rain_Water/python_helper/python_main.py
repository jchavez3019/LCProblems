from typing import List, Tuple, Union, Optional

class Solution:
    def trap(self, height: List[int]) -> int:

        curr_list = []  # used as a stack to hold "nodes"
        wu = 0  # number of water units we can hold

        for i in range(1, len(height)):
            # iterate through the depth list, skipping the first idx

            h = height[i]  # height at our current idx
            p_h = height[i - 1]  # height at the previous idx

            if h < p_h:
                # Our height is smaller than the previous height, so we can form a new node and push it onto the stack
                # so that it can be processed later if it can hold water
                new_node = (h, i, p_h)  # (current height, current idx, previous height)
                curr_list.append(new_node)
            elif h > p_h:
                # We are ascending, so we should be able to hold some water. We need to pop nodes that can be processed
                while len(curr_list) > 0:
                    curr_node = curr_list.pop()
                    ch, ci, c_ph = curr_node  # height, idx, prior height of this node in the stack
                    if ch >= h:
                        # The height is not tall enough to process this node, we need to push the node back
                        # and break from processing the stack
                        curr_list.append(curr_node)
                        break

                    # These 2 if statements make it clear that we are only "fully" processing a node if it is a rectangle.
                    # If it is not a rectangle, we only "partially" process the portion of the node that is a rectangle,
                    # and then we push a new node to the stack.
                    if c_ph > h:
                        # We can "partially" process this node because it can hold some water, but the height is not
                        # taller than the previous height. Therefore, we must update our rectangle area calculation
                        # and form a new node to be pushed onto the stack.
                        wu += (i - ci) * (h - ch)
                        new_node = (h, ci, c_ph)
                        curr_list.append(new_node)
                    else:
                        # This node and its previous height is smaller than the current height. It is simply a rectangle
                        # whose area can be easily calculated. This node is now "completely" processed.
                        wu += (i - ci) * (c_ph - ch)
        return wu

def main():
    input_height = [0,1,0,2,1,0,1,3,2,1,2,1]
    # input_height = [4,2,0,3,2,5]

    sol_obj = Solution()
    ret = sol_obj.trap(input_height)
    print(f"Input: \n{input_height}")
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()