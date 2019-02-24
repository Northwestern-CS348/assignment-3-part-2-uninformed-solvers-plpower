from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        ### student code goes here
        f_statement1 = 'fact: (on ?disk peg1)'
        myfact1 = parse_input(f_statement1)
        f_statement2 = 'fact: (on ?disk peg2)'
        myfact2 = parse_input(f_statement2)
        f_statement3 = 'fact: (on ?disk peg3)'
        myfact3 = parse_input(f_statement3)
        ### make a new statement and put that in Fact
        ret_list1 = []
        ret_list2 = []
        ret_list3 = []

        if self.kb.kb_ask(myfact1):
            lb1 = self.kb.kb_ask(myfact1)
            for bindings in lb1:
                for b in bindings.bindings:
                    ret_list1.append(int(b.constant.element[-1]))
                    ret_list1.sort()

        if self.kb.kb_ask(myfact2):
            lb2 = self.kb.kb_ask(myfact2)
            for bindings in lb2:
                for b in bindings.bindings:
                    ret_list2.append(int(b.constant.element[-1]))
                    ret_list2.sort()

        if self.kb.kb_ask(myfact3):
            lb3 = self.kb.kb_ask(myfact3)
            for bindings in lb3:
                for b in bindings.bindings:
                    ret_list3.append(int(b.constant.element[-1]))
                    ret_list3.sort()
        new = (tuple(ret_list1), tuple(ret_list2), tuple(ret_list3))
        return new



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        print(movable_statement)
        disk = str(movable_statement.terms[0])
        from_peg = str(movable_statement.terms[1])
        to_peg = str(movable_statement.terms[2])
        old_on = parse_input('fact: (on ' + disk + ' ' + from_peg + ')')
        new_on = parse_input('fact: (on ' + disk + ' ' + to_peg + ')')
        old_top = parse_input('fact: (topdisk ' + disk + ' ' + from_peg + ')')
        new_top1 = parse_input('fact: (topdisk ' + disk + ' ' + to_peg + ')')
        from_empty = parse_input('fact: (empty ' + from_peg + ')')
        to_empty = parse_input('fact: (empty ' + to_peg + ')')
        # statement that asks if the disk was above anything
        # above_stmt = parse_input('fact: (above ' + disk + ' ?disk)')
        # fact to ask if to_peg has a top_disk
        to_topdisk = parse_input('fact: (topdisk ?disk ' + to_peg + ')')
        tdisk_under = ''

        if to_peg == from_peg:
            return

        if self.isMovableLegal(movable_statement):
            # move the peg first:
            self.kb.kb_retract(old_on)
            self.kb.kb_assert(new_on)
            fact = parse_input("fact: (on ?disk " + from_peg)
            if self.kb.kb_ask(fact):
                anyleft = True
            # find out all disks on the from_peg
            # sort them by size and use that to determine new top peg
                array_of_ons = []
                lb = self.kb.kb_ask(fact)
                for b in lb:
                    array_of_ons.append(b.bindings[0].constant.element)
                array_of_ons.sort()
                top_dog = array_of_ons[0]
                #print(array_of_ons)
            else:
                anyleft = False

            # to_peg: deal with the tops and if the peg is/was empty
            self.kb.kb_retract(to_empty)
            if self.kb.kb_ask(to_topdisk):
                lb = self.kb.kb_ask(to_topdisk)
                tdisk_under = lb[0].bindings[0].constant.element
            t_under = parse_input('fact: (topdisk ' + tdisk_under + ' ' + to_peg + ')')
           # print("Retracting as topdisk")
            self.kb.kb_retract(t_under)
            self.kb.kb_assert(new_top1)

            # from_peg: deal with the tops and if peg is now empty
            self.kb.kb_retract(old_top)
            if not anyleft:
                self.kb.kb_assert(from_empty)
            else:
                new_top2 = parse_input('fact: (topdisk ' + top_dog + ' ' + from_peg + ')')
                self.kb.kb_assert(new_top2)
            #print("DONE")
        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        print("REVERSING")
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))
        print("that was reversed")

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        one = parse_input('fact: (posn ?x pos1 pos1')
        two = parse_input('fact: (posn ?x pos2 pos1')
        three = parse_input('fact: (posn ?x pos3 pos1')
        four = parse_input('fact: (posn ?x pos1 pos2')
        five = parse_input('fact: (posn ?x pos2 pos2')
        six = parse_input('fact: (posn ?x pos3 pos2')
        seven = parse_input('fact: (posn ?x pos1 pos3')
        eight = parse_input('fact: (posn ?x pos2 pos3')
        nine = parse_input('fact: (posn ?x pos3 pos3')
        list1 = [one, two, three]
        list2 = [four, five, six]
        list3 = [seven, eight, nine]
        ret_list1 = []
        ret_list2 = []
        ret_list3 = []

        for x in list1:
            if self.kb.kb_ask(x):
                lb1 = self.kb.kb_ask(x)
                for bindings in lb1:
                    for b in bindings.bindings:
                        if b.constant.element[-1] == 'y':
                            ret_list1.append(-1)
                        else:
                            ret_list1.append(int(b.constant.element[-1]))
        for x in list2:
            if self.kb.kb_ask(x):
                lb2 = self.kb.kb_ask(x)
                for bindings in lb2:
                    for b in bindings.bindings:
                        if b.constant.element[-1] == 'y':
                            ret_list2.append(-1)
                        else:
                            ret_list2.append(int(b.constant.element[-1]))
        for x in list3:
            if self.kb.kb_ask(x):
                lb3 = self.kb.kb_ask(x)
                for bindings in lb3:
                    for b in bindings.bindings:
                        if b.constant.element[-1] == 'y':
                            ret_list3.append(-1)
                        else:
                            ret_list3.append(int(b.constant.element[-1]))
        new = (tuple(ret_list1), tuple(ret_list2), tuple(ret_list3))
        return new


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)


        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = str(movable_statement.terms[0])
        tile_x = str(movable_statement.terms[1])
        tile_y = str(movable_statement.terms[2])
        empty_x = str(movable_statement.terms[3])
        empty_y = str(movable_statement.terms[4])
        old_pos_x = parse_input('fact: (posn ' + tile + ' ' + tile_x + ' ' + tile_y + ')')
        old_pos_e = parse_input('fact: (posn empty ' + empty_x + ' ' + empty_y + ')')
        new_pos_e = parse_input('fact: (posn empty ' + tile_x + ' ' + tile_y + ')')
        new_pos_x = parse_input('fact: (posn ' + tile + ' ' + empty_x + ' ' + empty_y + ')')

        if self.isMovableLegal(movable_statement):
            self.kb.kb_retract(old_pos_x)
            self.kb.kb_retract(old_pos_e)
            self.kb.kb_assert(new_pos_x)
            self.kb.kb_assert(new_pos_e)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
