#!/usr/bin/env python3
"""
Monoprocessor scheduling solver using Bratley’s algorithm

Part of the assignment for Combinatorial optimization class at FEE CTU.

Author: Jan Fajfer
Sources: https://cw.fel.cvut.cz/b192/_media/courses/ko/11_bratley_handout.pdf
"""

# Imports
import sys

# Classes
class CTask:
    """
    Stores the parametes of a scheduling task.
    """
    def __init__(self, n: int, p: list, r: list, d: list):
        """
        Initializes the class and stores values.
        :param n: number of tasks
        :param p: processing times
        :param r: release times
        :param d: deadlines
        """
        self.n = n
        self.p = p
        self.r = r
        self.d = d
        self.best_solution = []
        self.UB = None

    def schedule(self):
        """
        Returns the final schedule - the optimal start time of each task.

        :return: list of start times
        """
        if len(self.best_solution) == 0:
            return [-1]
        c = 0
        schedule = [0 for i in range(self.n)]
        for i in self.best_solution:
            scheduled_time = max(c, self.r[i])
            schedule[i] = scheduled_time
            c = scheduled_time + self.p[i]
        return schedule

# Functions
def load_input(filename):
    """
    Loads the specification of the task.

    :param filename:
    :return: n: number of tasks, p: list of processing times,
             r: list of release times, d: list of deadlines
    """
    with open(sys.argv[1]) as f:
        n = int(f.readline())
        p = [0 for i in range(n)]
        r = [0 for i in range(n)]
        d = [0 for i in range(n)]
        for i in range(n):
            p[i], r[i], d[i] = [int(x) for x in f.readline().split()]
    return n, p, r, d

def branch_n_bounds(S: list, T: list, c: int, task: CTask) -> bool:
    """
    Branch and bounds algorithm for a scheduling task 1 | r,d | Cmax.

    It goes through all possible permutations of tasks and cuts the tree
    when possible using three rules: Missed deadline, Bound solution and Decomposiotion.

    :param S: scheduled tasks
    :param T: tasks to be scheduled
    :param c: length of the partial schedule S
    :param task: class with the task parameters
    :return: True if optimal solution found, False otherwise
    """

    # Missed deadline - make sure all unassigned tasks won't miss their deadline if assigned
    for j in T:
        if max(c, task.r[j]) + task.p[j] > task.d[j]:
            return False

    # Bound on the solution
    if len(T) == 0:
        if task.UB is None or c < task.UB:
            task.UB = c
            task.best_solution = S
        return False
    else:
        LB = max(c, min(task.r[j] for j in T)) + sum(task.p[j] for j in T)
        if task.UB is None:
            UB = max(task.d[j] for j in T)
            if LB > UB:
                return False
        else:
            if LB >= task.UB:
                return False

    # Decomposition
    optimal_partial_solution = False
    if c <= min(task.r[j] for j in T):
        task.best_solution = task.best_solution + S
        optimal_partial_solution = True

    # Branch
    for i in range(len(T)):
        if branch_n_bounds(S + [T[i]], T[:i] + T[i+1:], max(c, task.r[T[i]]) + task.p[T[i]], task):
            return True

    return optimal_partial_solution

def main():
    """
    Calls all the necessary functions.
    :return:
    """
    task_num, proc_times, release_times, deadlines = load_input(sys.argv[1])
    task = CTask(task_num, proc_times, release_times, deadlines)

    # Branch and Bounds
    # DFS through the solution Tree
    scheduled_tasks = []
    not_scheduled_tasks = [i for i in range(task_num)]
    branch_n_bounds(scheduled_tasks, not_scheduled_tasks, 0, task)

    # write solution to a file ----------------------------------------
    with open(sys.argv[2], "w") as f:
        for s in task.schedule():
            f.write(str(s) + "\n")

if __name__ == "__main__":
    main()
