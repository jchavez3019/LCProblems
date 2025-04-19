from typing import Union, List, Tuple, Optional

class Solution:

    def getNextBatch(self):
        min_val = self.arrival[self.p_idx]

        for i in range(self.p_idx, len(self.arrival)):
            if self.arrival[i] > min_val:
                break
            state = self.state[i]
            if state == 0:
                self.pwt_enter.append(i)
            else:
                self.pwt_exit.append(i)
            self.p_idx += 1

        self.counter = min_val

    def process(self, process_enter: bool):

        # get the array we want to process
        arr = self.pwt_enter if process_enter else self.pwt_exit
        for i in range(len(arr)):
            # for each index in this array, update the solution with the time
            # we processed it and update the counter
            idx = arr[i]
            self.solution[idx] = self.counter
            self.counter += 1

        # empty the array that was processed
        if process_enter:
            self.pwt_enter = []
        else:
            self.pwt_exit = []

        # we still have people that can potentially be processed
        # with our newly updated counter
        if self.p_idx < len(self.arrival):
            a = self.arrival[self.p_idx]
            appended = False
            while a <= self.counter:
                # take in people whose arrival time is below or
                # at our counter
                state = self.state[self.p_idx]
                if state == 0:
                    self.pwt_enter.append(self.p_idx)
                else:
                    self.pwt_exit.append(self.p_idx)
                self.p_idx += 1
                appended = True
                if self.p_idx >= len(self.arrival):
                    break
                a = self.arrival[self.p_idx]
            if self.priority == 1 and not appended:
                self.priority = 0

    # def timeTaken(self, arrival: List[int], state: List[int]) -> List[int]:
    #
    #     self.arrival = arrival
    #     self.state = state
    #     self.p_idx = 0
    #     self.pwt_enter = []
    #     self.pwt_exit = []
    #     self.counter = 0
    #     self.solution = [-1 for _ in range(len(arrival))]
    #     self.getNextBatch()
    #     self.priority = 0 # 0 := exiting people take priority; 1 := entering people take priority
    #     while self.p_idx < len(arrival) or len(self.pwt_enter) > 0 or len(self.pwt_exit) > 0:
    #
    #         if len(self.pwt_enter) == 0 and len(self.pwt_exit) == 0:
    #             self.getNextBatch()
    #             self.priority = 0
    #
    #         if (self.priority == 0 and len(self.pwt_exit) > 0) or len(self.pwt_enter) == 0:
    #             self.priority = 0
    #             self.process(False)
    #         else:
    #             self.priority = 1
    #             self.process(True)
    #
    #     return self.solution
    def timeTaken(self, arrival: List[int], state: List[int]) -> List[int]:

        def _update_end_pointers():
            """
            This function updates the end pointers for our lists. The end pointer is updated with respect
            to the counter as the counter defines with people we are capable of processing at this point.
            """
            # 'nonlocal' keyword is needed for variables defined in the outer scope that are read AND modified.
            # If read but not modified, the keyword is not needed.
            nonlocal e_enter, e_exit
            while e_enter < len(pwt_enter) and arrival[pwt_enter[e_enter]] <= counter:
                e_enter += 1
            while e_exit < len(pwt_exit) and arrival[pwt_exit[e_exit]] <= counter:
                e_exit += 1

        # pwt_enter(exit) is short for "people want to enter(exit)"
        pwt_enter = [i for i in range(len(state)) if state[i] == 0]
        pwt_exit = [i for i in range(len(state)) if state[i] == 1]
        # Even though the above arrays organize people by their state, we use points into these arrays that are updated
        # depending on the counter. This is because we can only process people in these arrays based on our current
        # time-step.
        s_enter = 0; e_enter = 0; s_exit = 0; e_exit = 0
        # initialize solution array with -1
        solution = [-1 for _ in range(len(arrival))]
        priority = 0 # 0 := exiting people take priority; 1 := entering people take priority
        num_processed = 0
        counter = -1  # we have not started our algorithm

        while num_processed < len(arrival):

            if e_exit - s_exit == 0 and e_enter - s_enter == 0:
                # both arrays are empty

                if s_exit >= len(pwt_exit):
                    # there are no more people for pwt_exit to process, only pwt_enter
                    counter = arrival[pwt_enter[s_enter]]
                elif s_enter >= len(pwt_enter):
                    # there are no more people for pwt_enter to process, only pwt_exit
                    counter = arrival[pwt_exit[s_exit]]
                else:
                    # Both lists have more people to process. The one whose newest person has the smallest
                    # arrival time should be our new counter.
                    counter = min(arrival[pwt_enter[s_enter]], arrival[pwt_exit[s_exit]])

                # Now that our counter has been updated, we need to update our lists to have entries with people
                # that can be processed.
                _update_end_pointers()

                # This case only occurred because we had at least one second where we could not let anyone use the door.
                # By the rules, people "exiting" now have priority.
                priority = 0

            if (priority == 0 and e_exit - s_exit > 0) or e_enter - s_enter == 0:
                # process exit members
                while s_exit < e_exit:
                    solution[pwt_exit[s_exit]] = counter
                    counter += 1
                    s_exit += 1
                    num_processed += 1
                priority = 0  # we just processed exit members, update priority

            elif (priority == 1 and e_enter - s_enter > 0) or e_exit - s_exit == 0:
                # TODO:
                #  We could just use 'else' instead of 'elif' for slightly more efficiency, but we leave the 'elif' to
                #  make it clear in which conditions each case takes place for better algorithmic readability.
                # process enter members
                while s_enter < e_enter:
                    solution[pwt_enter[s_enter]] = counter
                    counter += 1
                    s_enter += 1
                    num_processed += 1
                priority = 1  # we just processed enter members, update priority

            # Our counter has been updated, we need to add more people w.r.t. the new counter if possible
            _update_end_pointers()

        return solution

def main():
    # input_arrival = [0,1,1,2,4]
    # input_state = [0,1,0,0,1]
    # solution = [0,3,1,2,4]
    # input_arrival = [0,0,0]
    # input_state = [1, 0, 1]
    # solution = [0, 2, 1]
    # input_arrival = [0, 1, 1, 1, 1, 4]
    # input_state = [0,0,1,0,0,1]
    # solution = None
    # input_arrival = [1, 1, 1, 1, 1, 3]
    # input_state = [0, 1, 0, 1, 0, 1]
    # solution = None
    input_arrival = [0,5,6,6,7,9,9,9,10,10,10,10,10,15,16,17,17,17]
    input_state = [1,1,1,1,0,0,0,1,1,1,1,1,0,1,1,0,1,0]
    solution = [0,5,6,7,8,9,10,12,13,14,15,16,11,17,18,20,19,21]

    print(f"Input: \n{input_arrival}")
    print(f"State: \n{input_state}")
    print(f"GT Solution: \n{solution}")

    sol_obj = Solution()
    ret = sol_obj.timeTaken(input_arrival, input_state)

    print(f"Solution returned: \n{ret}")

if __name__ == '__main__':
    main()