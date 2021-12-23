
#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
import heapq
from QuintrisGame import QuintrisGame
import copy
from random import uniform

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()


# Simple quintris program! v0.2
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    #def get_moves(self, quintris, weight_list):
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        #Included the following functions from SimpleQuintris with few tweaks according to my usage.
        def check_collision(board, piece, row, col):
            return col + len(piece[0]) > quintris.BOARD_WIDTH or row + len(piece) > quintris.BOARD_HEIGHT \
                   or any([any([(c != " " and board[i_r + row][col + i_c] != " ") for (i_c, c) in enumerate(r)]) for (i_r, r) in enumerate(piece)])

        def combine(str1, str2):
            return "".join([c if c != " " else str2[i] for (i, c) in enumerate(str1)])

        def place_piece(board, piece, row, col):
            return (board[0:row] + \
                    [(board[i + row][0:col] + combine(r, board[i + row][col:col + len(r)]) + board[i + row][col + len(r):]) for (i, r) in enumerate(piece)] + \
                    board[row + len(piece):])

        def move_n(col_offset, piece, curr_piece, board, index):
            #new_col = max(0,min(15-len(piece[0]), piece[2]-index+col_offset))
            new_col = max(0, min(quintris.BOARD_WIDTH - len(piece[0]), piece[2] + (index*col_offset)))
            (just_piece, col) = (curr_piece, new_col) if not check_collision(board,curr_piece,piece[1],new_col) else (piece[0], piece[2])
            return just_piece,col

        def rotate_piece(piece, rotation):
            rotated_90 = ["".join([str[i] for str in piece[::-1]]) for i in range(0, len(piece[0]))]
            return {0: piece, 90: rotated_90, 180: [str[::-1] for str in piece[::-1]],
                    270: [str[::-1] for str in rotated_90[::-1]]}[rotation]

        def hflip_piece(piece):
            return [str[::-1] for str in piece]

        def down(curr_piece, board_t, piece, new_col_val):
            row = piece[1]
            while not check_collision(board_t, curr_piece, row, new_col_val):
                row += 1
            new_board_t = place_piece(board_t, curr_piece, row-1, new_col_val)
            return new_board_t

        def print_state(board, score):
            print("\n" * 3 + ("Score: %d \n" % score) + "|\n".join(board) + "|\n" + "-" * QuintrisGame.BOARD_WIDTH)
        #Piece details
        piece = quintris.get_piece()
        curr_piece = piece[0]
        #print(piece)
        #print(curr_piece)

        #Board Details
        board = quintris.get_board()
        board_t = copy.deepcopy(board)

        #all_possible_pieces = [piece]
        all_possible_pieces = {}
        for i in [0, 90, 180, 270]:
            k = int(i / 90)
            if rotate_piece(curr_piece, i) not in all_possible_pieces.values():
                all_possible_pieces['n' * k] = rotate_piece(curr_piece, i)
        # flip
        if hflip_piece(curr_piece) not in all_possible_pieces.values():
            all_possible_pieces['h'] = hflip_piece(curr_piece)
            for i in [0,90,180,270]:
                k = int(i/90)
                if rotate_piece(hflip_piece(curr_piece), i) not in all_possible_pieces.values():
                    all_possible_pieces['h'+('n' * k)] = rotate_piece(hflip_piece(curr_piece), i)

        for key, value in all_possible_pieces.items():
            all_possible_pieces[key] = (value, piece[1], piece[2])

        #print(all_possible_pieces)
        successor_list = []
        previous_succ = None

        #for piece in all_possible_pieces:
        for key,piece in all_possible_pieces.items():
            curr_piece = piece[0]
            #print(piece[2],"actual_col")
            #Left Movement
            #print("Left Movement starts")
            index = 1
            #while index < piece[2] + 1:
            while index < quintris.BOARD_WIDTH:
                #print(index,"index")
                left_movement, new_col_val = move_n(-1, piece, curr_piece, board_t, index)
                #new_col_val = max((piece[2] - index), 0)
                #print(new_col_val,"new_col_val")
                if piece[2] > new_col_val >= 0:
                    new_board_t = down(left_movement, board_t, piece, new_col_val)
                    #new_board_t = down(curr_piece, board_t, piece, new_col_val)
                    if previous_succ!= new_board_t:
                        successor_list.append([new_board_t, [key + "b"*(index)]])
                        #successor_list.append([new_board_t, ["b" * (index)]])
                        previous_succ = new_board_t
                index += 1

            #Right Movement
            #print("Right movement starts")
            index = 1
            #while index < 16 - piece[2]:
            while index < quintris.BOARD_WIDTH:
                #print(index,"index")
                #print(piece[2])

                if not check_collision(board_t,curr_piece,piece[1],min((piece[2]+index),quintris.BOARD_WIDTH-1)):
                    new_col_val = min((piece[2]+index),quintris.BOARD_WIDTH-1)
                    #print(new_col_val,"new_col_val")
                    right_movement = curr_piece
                    if piece[2] < new_col_val < quintris.BOARD_WIDTH:
                        new_board_t = down(right_movement, board_t, piece, new_col_val)
                        if previous_succ!= new_board_t:
                            successor_list.append([new_board_t, [key+"m"*(index)]])
                            #successor_list.append([new_board_t, ["m" * (index)]])
                            previous_succ = new_board_t
                index += 1

        # for board in successor_list:
        #     print(board[0])
        #     print(board[1])

        # Next piece - Iteration

        next_piece = quintris.get_next_piece()
        #print(npiece)

        all_possible_next_pieces = {}
        for i in [0, 90, 180, 270]:
            k = int(i / 90)
            if rotate_piece(next_piece, i) not in all_possible_next_pieces.values():
                all_possible_next_pieces['n' * k] = rotate_piece(next_piece, i)
        # flip
        if hflip_piece(next_piece) not in all_possible_next_pieces.values():
            all_possible_next_pieces['h'] = hflip_piece(next_piece)
            for i in [0, 90, 180, 270]:
                k = int(i / 90)
                if rotate_piece(hflip_piece(next_piece), i) not in all_possible_next_pieces.values():
                    all_possible_next_pieces['h' + ('n' * k)] = rotate_piece(hflip_piece(next_piece), i)

        for key, value in all_possible_next_pieces.items():
            all_possible_next_pieces[key] = (value, 0, 0)

        #print(all_possible_next_pieces)
        # #print(all_possible_next_pieces)
        nsuccessor_list = []
        for s in successor_list:
            cur_board = s[0]
            cur_board_dup = copy.deepcopy(cur_board)
            previous_succ = None

            for key, value in all_possible_next_pieces.items():
                np = value
                cu_n_piece = np[0]

            #Left Movement
                # index = 1
                # # while index < piece[2] + 1:
                # while index < quintris.BOARD_WIDTH:
                #     # print(index,"index")
                #     left_movement, new_col_val = move_n(-1, np, cu_n_piece, cur_board_dup, index)
                #     # new_col_val = max((piece[2] - index), 0)
                #     # print(new_col_val,"new_col_val")
                #     if piece[2] > new_col_val >= 0:
                #         new_board_t = down(left_movement, cur_board_dup, np, new_col_val)
                #         # new_board_t = down(curr_piece, board_t, piece, new_col_val)
                #         if previous_succ != new_board_t:
                #             successor_list.append([new_board_t, s[1]])
                #             # successor_list.append([new_board_t, ["b" * (index)]])
                #             previous_succ = new_board_t
                #     index += 1

                #Right movement
                index = 1
                # while index < 16 - piece[2]:
                while index < quintris.BOARD_WIDTH:
                    # print(index,"index")
                    # print(piece[2])

                    if not check_collision(cur_board_dup, cu_n_piece, np[1], min((np[2] + index), quintris.BOARD_WIDTH-1)):
                        new_col_val = min((np[2] + index), quintris.BOARD_WIDTH-1)
                        # print(new_col_val,"new_col_val")
                        right_movement = cu_n_piece
                        if np[2] < new_col_val < quintris.BOARD_WIDTH:
                            new_board_t = down(right_movement, cur_board_dup, np, new_col_val)
                            if previous_succ != new_board_t:
                                nsuccessor_list.append([new_board_t, s[1]])
                                # successor_list.append([new_board_t, ["m" * (index)]])
                                previous_succ = new_board_t
                    index += 1

        #print(nsuccessor_list)
        # #
        # #
        # #
        # # #Score calculation of successors
        # #
        score_succ = []
        for new_board in nsuccessor_list:
            # print(new_board[0])
            # print(new_board[1])
            # print(type(new_board[1]))
            # print(type(new_board))
            # print(type(new_board[0]))
            board = new_board[0]
            # print(len(board))
            #print(len(board),len(board[0]))
            column_heights = [len(board)] * len(board[0])
            #print(column_heights)
            for c in range(0, len(board[0])):
                for r in range(0, len(board)):
                    if board[r][c] == "x":
                        column_heights[c] = r
                        break
            #print("Column heights")
            #print(column_heights)
            #print("---------------")
            #if len(column_heights)!=15:
            #    print("Red flag",len(column_heights))

            #tall_index = column_heights.index(min(column_heights))
            #short_index = column_heights.index(max(column_heights))
            # print("tall_index", tall_index)

            # Calculate gaps
            gaps, c = 0, 0
            while c < len(board[0]):
                # print("c",c)
                for r in enumerate(column_heights):
                    # print(r,"r")
                    for new_r in range(r[1] + 1, len(board)):
                        # print(new_r,len(board),c)
                        if board[new_r][c] == " ":
                            gaps += 1
                    c += 1

            #print("gaps", gaps)

            # Calculate full row formation
            row_count = 0
            for r in range(len(board) - 1, -1, -1):
                if " " not in board[r]:
                    row_count += 1
            #print("row_count", row_count)

            #Calculate the uneveness
            uneven_val = 0
            for i in range(len(column_heights)-2):
                uneven_val += abs(column_heights[i+1] - column_heights[i])
            #print("uneven_val",uneven_val)

            tallest_height = quintris.BOARD_HEIGHT-min(column_heights)
            sum_heights = quintris.BOARD_HEIGHT*quintris.BOARD_WIDTH - sum(column_heights)
            height_diff = abs((quintris.BOARD_HEIGHT-min(column_heights)) - (quintris.BOARD_HEIGHT-max(column_heights)))
            heuristic_score = -1.91 * gaps - 1.6907 * sum_heights + 3.61 * row_count - 0.51 * uneven_val
            score_succ.append(heuristic_score)
        succ_index = score_succ.index(max(score_succ))
        #print(score_succ)
        #print(max(score_succ),"max_score")
        #print(print_state(successor_list[succ_index][0],0),"max_score succ")
        #print("max_score",heuristic_score)
        #print(score_succ)
        #print(''.join(successor_list[succ_index][1]))
        return(''.join(nsuccessor_list[succ_index][1]))
        #return random.choice("mnbh") * random.randint(1, 10)

    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [min([r for r in range(len(board) - 1, 0, -1) if board[r][c] == "x"] + [100, ]) for c in
                              range(0, len(board[0]))]
            index = column_heights.index(max(column_heights))

            if (index < quintris.col):
                quintris.left()
            elif (index > quintris.col):
                quintris.right()
            else:
                quintris.down()

###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)
    #print("in try loop")
    #game = 0
    # while game < 6:
    #     print("starting game number", game+1)
    #     quintris.start_game(player)
    #     game+=1
    #     print(game)

except EndOfGame as s:
    print("\n\n\n", s)
