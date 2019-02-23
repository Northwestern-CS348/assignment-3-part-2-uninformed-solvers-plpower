
from solver import *

class SolverDFS(UninformedSolver):

    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.populate()

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

        curr = self.currentState
        self.visited[curr] = True
        if curr.state == self.victoryCondition:
            return True
        print("POPULATED _____________ first")

        while curr.nextChildToVisit < len(curr.children):
            ns = curr.children[curr.nextChildToVisit]
            curr.nextChildToVisit += 1
            if ns not in self.visited:
                self.visited[ns] = False
                self.gm.makeMove(ns.requiredMovable)
                self.currentState = ns
                # populate children again (kinda like recursion)
                movables = self.gm.getMovables()
                # print(self.currentState.state)
                print("here are my movables for this move:")
                print(movables)
                for m in movables:
                    self.gm.makeMove(m)
                    child = GameState(self.gm.getGameState, self.currentState.depth + 1, m)
                    if child in self.visited:
                        self.gm.reverseMove(m)
                    self.currentState.children.append(child)
                    child.parent = self.currentState
                    self.gm.reverseMove(m)
                    print("POPULATED _____________ NOW")
                return False
        if curr.requiredMovable:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            print('walk back up')
        return False

    def populate(self):
        movables = self.gm.getMovables()
        print(movables)
        for m in movables:
            self.gm.makeMove(m)
            child = GameState(self.gm.getGameState, self.currentState.depth + 1, m)
            if child in self.visited:
                self.gm.reverseMove(m)
            self.currentState.children.append(child)
            child.parent = self.currentState
            self.gm.reverseMove(m)

class SolverBFS(UninformedSolver):
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
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        curr = self.currentState
        if self.currentState.state == self.victoryCondition:
            return True
        else:
            movables = self.gm.getMovables()
            if movables and not curr.children:
                for m in movables:
                    self.gm.makeMove(m)
                    n_state = GameState(self.gm.getGameState, self.currentState.depth + 1, m)
                    n_state.parent = self.currentState
                    n_state.parent.children.append(n_state)
                    self.gm.reverseMove(m)
            self.unvisit(curr)
            while self.currentState.nextChildToVisit < len(self.currentState.children):
                n_state = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                if n_state not in self.visited:
                    self.visit(n_state)
                    if n_state is self.victoryCondition:
                        return True
                    break
                self.unvisit(n_state)
        return False

    def visit(self, n_state):
        self.currentState = n_state
        self.visited[n_state] = True
        self.gm.makeMove(n_state.requiredMovable)
        return

    def unvisit(self, state):
        while not self.currentState and self.currentState.nextChildToVisit == len(self.currentState.children):
            self.gm.reverseMove(state.requiredMovable)
            state = state.parent
        return
