import math
import utils
import functools

'''
    Node class
    
    for using search tree and contains state and the action from last move.
    the cost g and f (g + heuristic) are stored as well!

    built for project pA of COMP30024
    Authors: Xinyao Niu (900721), Maoting Zuo (901116)
    Team Name: VanGame
'''
@functools.total_ordering
class Node:

    '''
        constructor
    '''
    def __init__(self, preNode:'node'=None, state: "dict"={}, 
                            fromLastAction="", g=0) -> None:

        # string of the action that get to this state
        self.fromLastAction = fromLastAction
        self.preNode = preNode
        self.g = g
        self.state = state

        # calculate heuristic when initializing the node
        self.f = self.g + self.heuristic(self.state)


    '''
        function overrided for using comparasion operators.
    '''
    def __lt__(self, other):
        return self.f < other.f
    

    def __eq__(self, other):
        return self.f == other.f and \
            self.g == other.g and \
                self.state == other.state


    '''
        heuristic function
    '''
    def heuristic(self, state):

        # sum of all distance/2 from the position of
        # each piece to their closest goal
        # (nearly optimal)
        ovAlHe = 0
        for pc in state["players"]:
            minDist = utils.COST[pc]

            # get a int of heuristic
            if minDist % 2 == 0:
                ovAlHe = ovAlHe + (minDist / 2 + 1)
            else:
                ovAlHe = ovAlHe + ((minDist - 1) /2 +2)  
            # print(Heuri)
        
        return ovAlHe


    ''' 
        private (well..)function for generating new nodes
    '''
    def _newNode(self, oldCoor: tuple, newCoor: tuple=None, fromLastAction=""):
        newState = {}
        newState["players"] = self.state["players"] + []

        # remove old position
        # if exiting then just remove without appending new position
        newState["players"].remove(oldCoor)

        # if the piece being appling action is moving to other place
        # but not exiting then append new position
        if newCoor:
            newState["players"].append(newCoor)
        
        newState["goals"] = self.state["goals"]
        newState["blocks"] = self.state["blocks"]

        newNode = Node(self, newState, g=(self.g + 1), 
                        fromLastAction=fromLastAction)

        return newNode


    """
        this method are tring to find all the possible movement for
        all the avaliable pieces on the board as next possible
        states based on the current position of pieces, and trate
        them like the child of this node.
    """
    def expand(self) -> None:
        
        # delta x and y from any position to its neighbourhood (move)
        nearSix = [
            [0, -1],
            [1, -1],
            [1, 0],
            [0, 1],
            [-1, 1],
            [-1, 0]
        ]

        # delta x and y from any position to its possible move (jump)
        further = [
            [0, -2],
            [2, -2],
            [2, 0],
            [0, 2],
            [-2, 2],
            [-2, 0]
        ]

        allMoveNodes = []
        numOfAllPossible = 6

        for piece in range(len(self.state["players"])):

            # same position but different tuple
            tmpPiece = tuple(self.state["players"][piece] + ())

            # if piece is on the goal then exit
            if tmpPiece in self.state["goals"]:

                theNew = self._newNode(tmpPiece, 
                    fromLastAction="EXIT from " + str(tmpPiece) + ".")
                allMoveNodes.append(theNew)
                continue

            # check position of next possible moves
            # one direction at a time, check both move and jump
            for i in range(numOfAllPossible):

                # by move
                # 1 step position in this direction
                checkingCoordin = (tmpPiece[0] + nearSix[i][0], 
                                        tmpPiece[1] + nearSix[i][1])

                if (not (checkingCoordin in self.state["blocks"] or \
                        checkingCoordin in self.state["players"]))      \
                                and utils.pieceValid(checkingCoordin):

                    # if can reach this direction one step by move
                    # create new node
                    theNew = self._newNode(tmpPiece, checkingCoordin, 
                                    fromLastAction= "MOVE from " + str(tmpPiece)
                                     + 
                                        " to " + str(checkingCoordin) + ".")
                    allMoveNodes.append(theNew)
                else:
                    # by jump (if 1 step move in this direction can not 
                    # be reached)
                    # 2 step position in this direction
                    furtherCoordin = (tmpPiece[0] + further[i][0], 
                                        tmpPiece[1] + further[i][1])

                    if (not (furtherCoordin in self.state["blocks"] or \
                        furtherCoordin in self.state["players"])) and \
                                utils.pieceValid(furtherCoordin):

                        # if can reach this direction one step by jump
                        # create new node
                        theNew = self._newNode(tmpPiece, furtherCoordin, 
                                    fromLastAction="JUMP from " + str(tmpPiece)
                                     + " to " + str(furtherCoordin) + ".")
                        allMoveNodes.append(theNew)

        return allMoveNodes


    """
        determine if the current state is the goal state
    """
    def goal_test(self):
        return self.state["players"] == []


    '''
        to string
    '''
    def __str__(self):
        stateBoard = {

        }
        for p in self.state["players"]:
            stateBoard[p] = "*p*"

        for l in self.state["goals"]:
            if l in stateBoard:
                stateBoard[l] = stateBoard[l]+ "*a*"
            else:
                stateBoard[l] = "*a*"
        
        for o in self.state["blocks"]:
            if o in stateBoard:
                stateBoard[o] = stateBoard[o] + "*o*"
            else:
                stateBoard[o] = "*o*"
        utils.print_board(stateBoard, message=self.fromLastAction + 
                    str(self.heuristic(self.state)), debug=True)
        
        return self.fromLastAction

    __repr__ = __str__


if __name__ == "__main__":
    thatShitNode = Node(state={
        "players": [(0, 2), (2, 1)],
        "goals": [(3, 0), (2, 1), (1, 2), (0, 3)],
        "blocks": [(2, -1)]
    })

    print(thatShitNode.expand())
