from typing import Union, Tuple, List, Optional

class Solution:
    def calculate(self, s: str) -> int:
        """
        Evaluates a string composed of integer values and the following operators: +, -, (, ). Multiplication
        and division are not supported. White-spaces are allowed.
        :param s: String to evaluate
        :return:  Final calculation
        """

        # surround the entire expression in parentheses since the last ')' will allow us to perform the final
        # calculation
        s = '(' + s + ')'

        # nest the calculations and operators since expressions inside of parentheses take precedence and must
        # be calculated first
        calculations = []
        operators = []

        # need a flag to track continuous digits found in a string so that we can handle numbers larger than 9
        previously_digit = False

        # the current number we are tracking
        current_num = 0
        # the running calculation of our current expression
        current_calculation = 0
        # the operator to use when we update our current calculation
        current_operator = '+'
        for i in range(len(s)):

            c = s[i]  # current character in the string

            # handle the case where the character is a digit
            digit = ord(c) - ord('0')
            if 0 <= digit <= 9:
                if previously_digit:
                    current_num = current_num * 10 + digit
                else:
                    current_num = digit
                previously_digit = True
                continue


            previously_digit = False  # this character is not a digit
            if c == ' ':
                # blanks can show up but are meaningless
                continue

            elif c == '(':
                # Prepare to enter a nested expression. We must store out current calculation and operator
                # and reset the current calculation, number, and operator.
                # Note by default, we assume EVERY expression has 0+ at the beginning since this does not change
                # the calculation but assuming this makes it easier to perform future calculations as we encounter
                # future numbers and/or expressions.
                calculations.append(current_calculation)
                operators.append(current_operator)
                current_calculation = 0
                current_num = 0
                current_operator = '+'

            elif c == ')':
                # We must finish the calculation of this inner expression
                if current_operator == '+':
                    current_calculation = current_calculation + current_num
                elif current_operator == '-':
                    current_calculation = current_calculation - current_num
                # We must update the calculation of the outer calculation with the final calculation of this
                # inner expression
                prev_calculation = calculations.pop()
                prev_operator = operators.pop()
                if prev_operator == '+':
                    current_calculation = prev_calculation + current_calculation
                elif prev_operator == '-':
                    current_calculation = prev_calculation - current_calculation
                else:
                    raise ValueError("Invalid operator")
                # reset the current number and operator
                current_num = 0
                current_operator = '+'

            elif c in ['+', '-']:
                # Encountered a new operator, update the calculation using the current number and operator.
                if current_operator == '+':
                    current_calculation = current_calculation + current_num
                elif current_operator == '-':
                    current_calculation = current_calculation - current_num
                # Update the current operator to be the new operator and reset the current number back to zero.
                current_operator = c
                current_num = 0

        return current_calculation


def main():
    # s = "1 + 1"
    # s = "1 + 1+32+  6"
    # s = "(1+(4+5+2)-3)+(6+8)"
    # s = "1-(     -2)"
    s = "1-(     -2)+3"
    sol_obj = Solution()
    ret = sol_obj.calculate(s)
    print(f"Input: \n{s}")
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()