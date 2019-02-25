from solver import *
from collections import deque


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # Student code goes here
        curr = self.currentState
        if curr.state == self.victoryCondition:
            return True
        if self.gm.getMovables() and not self.currentState.children:
            movables = self.gm.getMovables()
            for m in movables:
                self.gm.makeMove(m)
                child = GameState(self.gm.getGameState(), curr.depth + 1, m)
                if curr.parent and child.state is curr.parent.state:
                    self.gm.reverseMove(m)
                    continue
                child.parent = curr
                curr.children.append(child)
                self.gm.reverseMove(m)
        while curr.nextChildToVisit < len(curr.children):
            cnext = curr.children[curr.nextChildToVisit]
            curr.nextChildToVisit += 1
            if cnext not in self.visited:
                self.gm.makeMove(cnext.requiredMovable)
                self.currentState = cnext
                self.visited[self.currentState] = True
                if curr.state == self.victoryCondition:
                    return True
                    break
                elif curr.state != self.victoryCondition:
                    return False
                    break
                else:
                    self.gm.reverseMove(curr.requiredMovable)
                    curr = curr.parent


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        self.queue = deque()
        self.trail = []
        self.times = 0
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # initial check of v state
        self.trail = []
        curr = self.currentState
        if curr.state == self.victoryCondition:
            return True
        # append yourself if you're not in the queue
        if curr not in self.queue:
            self.queue.append(curr)
        self.visited[self.currentState] = True
        # filling all the children in the .children list AND the queue
        if self.gm.getMovables and not curr.children:
            movables = self.gm.getMovables()
            # print(movables)
            for m in movables:
                self.gm.makeMove(m)
                child = GameState(self.gm.getGameState(), curr.depth + 1, m)
                curr.children.append(child)
                if child not in self.visited:
                    self.visited[child] = False
                    if child not in self.queue:
                        self.queue.append(child)
                        print("added! to! the! queue! wooo")
                self.gm.reverseMove(m)
                child.parent = curr
        # pop off the leftmost child (aka the next one we want to visit)
        # fill the moves that would walk you back up into self.trail
        self.queue.popleft()
        my_first = self.queue[0]
        thereis = True
        while thereis:
            self.trail.append(my_first.requiredMovable)
            my_first = my_first.parent
            if not my_first.parent:
                thereis = False
                print("made it in")
        while curr.parent:
            self.gm.reverseMove(curr.requiredMovable)
            curr = curr.parent
        # actually finally take the walk of moves back up
        for x in reversed(self.trail):
            self.gm.makeMove(x)
        # reset your state to the next child in the queue
        self.currentState = self.queue[0]
        self.times = self.times + 1
        print(self.times)
        return False


