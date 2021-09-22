# Author: Richard Burgo
# Description: Kuba game that two players get to play and follows the typical Kuba game rules

class KubaGame:

    def __init__(self, player_a, player_b):
        """ Constructor for the KubaGame class. """

        self.__player_a_name = player_a[0]
        self.__player_b_name = player_b[0]
        self.__player_a_color = player_a[1]
        self.__player_b_color = player_b[1]
        self.__black_marble_count = 8
        self.__white_marble_count = 8
        self.__red_marble_count = 13
        self.__player_a_captured = 0
        self.__player_b_captured = 0
        self.__next_players_turn = None
        self.__current_players_turn = None

        # creating the 7x7 game board
        self.__board = [[0 for i in range(7)] for j in range(7)]
        self.__player_a_start_board = None
        self.__player_b_start_board = None

        # populate the board with all required rows

        # row 1
        self.__board[0][0] = "W"
        self.__board[0][1] = "W"
        self.__board[0][5] = "B"
        self.__board[0][6] = "B"

        # row 2
        self.__board[1][0] = "W"
        self.__board[1][1] = "W"
        self.__board[1][3] = "R"
        self.__board[1][5] = "B"
        self.__board[1][6] = "B"

        # row 3
        self.__board[2][2] = "R"
        self.__board[2][3] = "R"
        self.__board[2][4] = "R"

        # row 4
        self.__board[3][1] = "R"
        self.__board[3][2] = "R"
        self.__board[3][3] = "R"
        self.__board[3][4] = "R"
        self.__board[3][5] = "R"

        # row 5
        self.__board[4][2] = "R"
        self.__board[4][3] = "R"
        self.__board[4][4] = "R"

        # row 6
        self.__board[5][0] = "B"
        self.__board[5][1] = "B"
        self.__board[5][3] = "R"
        self.__board[5][5] = "W"
        self.__board[5][6] = "W"

        # row 7
        self.__board[6][0] = "B"
        self.__board[6][1] = "B"
        self.__board[6][5] = "W"
        self.__board[6][6] = "W"

    def print_board(self):
        """ Prints the current board """

        for i in range(len(self.__board)):
            for j in range(len(self.__board[i])):
                print(self.__board[i][j], end=' ')
            print()
        print(" ")

    def set_next_turn(self, player):
        """ Set the player who has the next turn. """

        self.__next_players_turn = player

    def get_next_turn(self):
        """ Returns the name of the player whose turn it is. If the game hasn't started return None. """

        return self.__next_players_turn

    def set_current_turn(self, player):
        """ Sets which player has the current turn. """

        self.__current_players_turn = player

    def get_current_player_turn(self):
        """ Returns the player that has the next turn. """

        return self.__current_players_turn

    def make_move(self, player_name, coordinates, direction):
        """ Moves the player Forward, Back, Right or Left. """

        other_player_color = ""
        other_player = ""

        # checking for correct player
        if self.get_current_player_turn() != player_name and self.get_current_player_turn() is not None:
            return False
        # ensuring coordinates are on the board
        elif 0 > coordinates[0] > 6 or 0 > coordinates[1] > 6:
            return False

        # checking which player is making the move
        elif player_name == self.__player_a_name:
            self.__player_a_start_board = self.__board
            other_player_color = self.__player_b_color
            other_player = self.__player_b_name
            self.__next_players_turn = self.__player_b_name
        else:
            self.__player_b_start_board = self.__board
            other_player_color = self.__player_a_color
            other_player = self.__player_a_name
            self.__next_players_turn = self.__player_a_name

        # making sure the marble is theirs
        if self.legal_move(coordinates, other_player_color):
            # set start board
            self.start_board(player_name, other_player_color)

            if direction == "F":
                # moving forward
                self.forward(player_name, coordinates, other_player_color)
            elif direction == "B":
                # moving backward
                self.back(player_name, coordinates, other_player_color)
            elif direction == "R":
                # moving right
                self.right(player_name, coordinates, other_player_color)
            else:
                # moving left
                self.left(player_name, coordinates, other_player_color)

            # setting final board
            self.end_board(player_name)

            # changing player turns
            self.set_current_turn(other_player)
            self.set_next_turn(player_name)

        else:
            print("This is an illegal move")
            move = False

    def get_winner(self):
        """ Returns only the name of the player who has won. If no one has won return None. """

        # whichever player captures 7 or more red marbles wins
        if self.__player_a_captured >= 7:
            return self.__player_a_name
        elif self.__player_b_captured >= 7:
            return self.__player_b_name
        else:
            return None

    def get_captured(self, player_name):
        """ Returns the number of marbles that the player has captured. """

        if player_name == self.__player_a_name:
            return self.__player_a_captured
        else:
            return self.__player_b_captured

    def get_marble(self, coordinates):
        """ tuple of the coordinates to check which marble is there. If no marble is there return "X". """

        if self.__board[coordinates[0]][coordinates[1]] == 0:
            return 'X'
        else:
            return self.__board[coordinates[0]][coordinates[1]]

    def get_marble_count(self):
        """ the number of marbles still on the board with in a tuple in order of (W,B,R). """

        temp_marble_count = (self.__white_marble_count, self.__black_marble_count, self.__red_marble_count)
        return temp_marble_count

    def legal_move(self, coordinates, other_player):
        """ Ensures that the move the player is trying to make is a legal move. """

        if (self.__board[coordinates[0]][coordinates[1]] != other_player and
                self.__board[coordinates[0]][coordinates[1]] != 'R' and
                self.__board[coordinates[0]][coordinates[1]] != 0):

            return True

        else:
            return False

    def forward(self, player_name, coordinates, other_player):
        """ Moves the marble forward on space. """

        move = True
        i = 1

        while move:

            # checking to see if the coordinates are the bottom row or if there is a marble behind it
            if coordinates[0] == 6 or self.__board[coordinates[0] + 1][coordinates[1]] == 0:
                # checking if another marble is in front of this one
                if (self.__board[coordinates[0] - i][coordinates[1]] != 0) and coordinates[0] - i > 0:
                    i += 1
                    pass
                # if this is the empty space to move into
                elif self.__board[coordinates[0] - i][coordinates[1]] == 0 or self.__board[coordinates[0] - i][
                    coordinates[1]] == other_player or self.__board[coordinates[0] - i][coordinates[1]] == 'R':

                    start = coordinates[0] - i
                    stop = coordinates[0]

                    # checking if a marble was pushed off the board and it's red
                    if coordinates[0] - i == 0 and self.__board[coordinates[0] - i][coordinates[1]] == 'R':
                        if player_name == self.__player_a_name:
                            self.__player_a_captured += 1
                            self.__red_marble_count -= 1
                        else:
                            self.__player_b_captured += 1
                            self.__red_marble_count -= 1

                    elif coordinates[0] - i == 0 and self.__board[coordinates[0] - i][coordinates[1]] == 'B':
                        self.__black_marble_count -= 1

                    elif coordinates[0] - i == 0 and self.__board[coordinates[0] - i][coordinates[1]] == 'W':
                        self.__white_marble_count -= 1

                    # moving the marbles
                    for j in range(start, stop, 1):
                        self.__board[coordinates[0] - i][coordinates[1]] = self.__board[coordinates[0] - i + 1][
                            coordinates[1]]
                        i -= 1

                    # making the original spot empty
                    self.__board[coordinates[0]][coordinates[1]] = 0

                    # Leave the loop
                    move = False
                    return True

            else:
                print("This is an illegal move")
                move = False

    def back(self, player_name, coordinates, other_player):
        """ Moves the marble backwards one space. """

        move = True
        i = 1

        while move:
            # checking to see if the coordinates are the top row or if there is a marble behind it
            if coordinates[0] == 0 or self.__board[coordinates[0] - 1][coordinates[1]] == 0:
                # checking if another marble is in front of this one
                if (self.__board[coordinates[0] + i][coordinates[1]] != 0) and coordinates[0] + i < 6:
                    i += 1
                    pass
                # if this is the empty space to move into
                elif self.__board[coordinates[0] + i][coordinates[1]] == 0 or self.__board[coordinates[0] + i][
                    coordinates[1]] == other_player or self.__board[coordinates[0] + i][coordinates[1]] == 'R':
                    start = coordinates[0] + i
                    stop = coordinates[0]

                    # checking if a marble was pushed off the board
                    if coordinates[0] + i == 6 and self.__board[coordinates[0] + i][coordinates[1]] == 'R':
                        if player_name == self.__player_a_name:
                            self.__player_a_captured += 1
                        else:
                            self.__player_b_captured += 1

                    elif coordinates[0] + i == 6 and self.__board[coordinates[0] + i][coordinates[1]] == 'B':
                        self.__black_marble_count -= 1

                    elif coordinates[0] + i == 6 and self.__board[coordinates[0] + i][coordinates[1]] == 'W':
                        self.__white_marble_count -= 1

                    # moving the marbles
                    for j in range(start, stop, -1):
                        self.__board[coordinates[0] + i][coordinates[1]] = self.__board[coordinates[0] + i - 1][
                            coordinates[1]]
                        i -= 1

                    # making the original spot empty
                    self.__board[coordinates[0]][coordinates[1]] = 0

                    # Leave the loop
                    move = False
                    return True

            else:
                print("This is an illegal move")
                move = False

    def right(self, player_name, coordinates, other_player):
        """ Moves the player right one space. """

        move = True
        i = 1

        while move:

            # checking to see if the coordinates are the left column or if there is a marble behind it
            if coordinates[1] == 0 or self.__board[coordinates[0]][coordinates[1] - 1] == 0:
                # checking if another marble is in front of this one
                if (self.__board[coordinates[0]][coordinates[1] + i] != 0) and coordinates[1] + i < 6:
                    i += 1
                    pass
                # if this is the empty space to move into
                elif self.__board[coordinates[0]][coordinates[1] + i] == 0 or self.__board[coordinates[0]][
                    coordinates[1] + i] == other_player or self.__board[coordinates[0]][
                    coordinates[1] + i] == 'R':

                    start = coordinates[1] + i
                    stop = coordinates[1]

                    # checking if a marble was pushed off the board and it's red
                    if coordinates[1] + i == 6 and self.__board[coordinates[0]][coordinates[1] + i] == 'R':
                        if player_name == self.__player_a_name:
                            self.__player_a_captured += 1
                        else:
                            self.__player_b_captured += 1

                    elif coordinates[1] + i == 6 and self.__board[coordinates[0]][coordinates[1] + i] == 'B':
                        self.__black_marble_count -= 1

                    elif coordinates[1] + i == 6 and self.__board[coordinates[0]][coordinates[1] + i] == 'W':
                        self.__white_marble_count -= 1

                    # moving the marbles
                    for j in range(start, stop, -1):
                        self.__board[coordinates[0]][coordinates[1] + i] = self.__board[coordinates[0]][
                            coordinates[1] + i - 1]
                        i -= 1

                    # making the original spot empty
                    self.__board[coordinates[0]][coordinates[1]] = 0

                    # Leave the loop
                    move = False
                    return True

            else:
                print("This is an illegal move")
                move = False

    def left(self, player_name, coordinates, other_player):
        """ Moves the player left one space. """

        move = True
        i = 1

        while move:

            # checking to see if the coordinates are the right column or if there is a marble behind it
            if coordinates[1] == 6 or self.__board[coordinates[0]][coordinates[1] + 1] == 0:
                # checking if another marble is in front of this one
                if (self.__board[coordinates[0]][coordinates[1] - i] != 0) and coordinates[1] - i > 0:
                    i += 1
                    pass
                # if this is the empty space to move into
                elif self.__board[coordinates[0]][coordinates[1] - i] == 0 or self.__board[coordinates[0]][
                    coordinates[1] - i] == other_player or self.__board[coordinates[0]][
                    coordinates[1] - i] == 'R':

                    start = coordinates[1] - i
                    stop = coordinates[1]

                    # checking if a marble was pushed off the board and it's red
                    if coordinates[1] - i == 0 and self.__board[coordinates[0]][coordinates[1] - i] == 'R':
                        if player_name == self.__player_a_name:
                            self.__player_a_captured += 1
                        else:
                            self.__player_b_captured += 1

                    elif coordinates[1] - i == 0 and self.__board[coordinates[0]][coordinates[1] - i] == 'B':
                        self.__black_marble_count -= 1

                    elif coordinates[1] - i == 0 and self.__board[coordinates[0]][coordinates[1] - i] == 'W':
                        self.__white_marble_count -= 1

                    # moving the marbles
                    for j in range(start, stop, 1):
                        self.__board[coordinates[0]][coordinates[1] - i] = self.__board[coordinates[0]][
                            coordinates[1] - i + 1]
                        i -= 1

                    # making the original spot empty
                    self.__board[coordinates[0]][coordinates[1]] = 0

                    # Leave the loop
                    move = False
                    return True

            else:
                move = False
                return False

        else:
            print("This is an illegal move")
            move = False

    def start_board(self, player_name, other_player):
        """ Captures the board at the start of the turn. """

        if player_name == self.__player_a_name:
            self.__player_a_start_board = self.__board
            other_player = self.__player_b_color
            self.__next_players_turn = self.__player_b_name
        else:
            self.__player_b_start_board = self.__board
            other_player = self.__player_a_color
            self.__next_players_turn = self.__player_a_name

    def end_board(self, player_name):
        """ Captures the board at the end of the turn. """
        if player_name == self.__player_a_name:
            if self.__board == self.__player_b_start_board:
                self.__board = self.__player_a_start_board
        else:
            if self.__board == self.__player_a_start_board:
                self.__board = self.__player_b_start_board


def main():
    playerA = input('Let\'s play Kuba! Player 1 enter your name ')
    playerB = input('Hello {}, who is your opponent '.format(playerA))
    print('\n{} will be White or "W" and {} will be Black or "B"\n'.format(playerA, playerB))
    game = KubaGame((playerA, 'W'), (playerB, 'B'))
    user_input = ""
    while game.get_winner() is None:

        current_player = None

        if game.get_next_turn() is None:
            game.set_current_turn(playerA)
            game.set_next_turn(playerB)
            game.print_board()
            current_player = game.get_current_player_turn()
            print('{} it\'s your turn \nfor a list of available commands type "options"'.format(current_player))
            user_input = input()
        else:
            game.print_board()
            current_player = game.get_current_player_turn()
            print('{} it\'s your turn \nfor a list of available commands type "options"'.format(current_player))
            user_input = input()
        if user_input == 'options':
            print('make move\nget marble count\nget captured\nget winner\n')
        elif user_input == 'make move':
            coordinates = input('enter the coordinates of the marble you\'d like to move separated by a "," \n')
            coordinates = coordinates.split(',')
            coordinates = [i.strip() for i in coordinates]
            coordinates = [int(i) for i in coordinates]
            coordinates = (coordinates[0], coordinates[1])
            direction = input('Enter either "F,B,R or L" for the direction you would like to move ')
            direction = direction.upper()
            game.make_move(current_player, coordinates, direction)

        elif user_input == 'get winner':
            print(game.get_winner())

        elif user_input == 'get marble count':
            print(game.get_marble_count())

        elif user_input == 'get captured':
            print(game.get_marble_count())

        elif user_input == 'get winner':
            print(game.get_winner())

        else:
            print('Invalid entry')


if __name__ == "__main__":
    main()
