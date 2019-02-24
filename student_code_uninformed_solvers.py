
from solver import *

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
                newst = self.gm.getGameState()
                if curr.parent and newst is curr.parent.state:
                    self.gm.reverseMove(m)
                else:
                    this = GameState(newst, curr.depth+1, m)
                    this.parent = curr
                    curr.children.append(this)
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
                    self.solveOneStep()

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
