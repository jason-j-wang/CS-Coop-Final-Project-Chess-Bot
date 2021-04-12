import chess #to help with chess rules
import pygame #for the GUI
from pygame.locals import *
import sys
import random
import math

#square colours
WHITE_SQUARE = "#f0dab5"
BLACK_SQUARE = "#b58763"
#these two help indicate the last move played
WHITE_SQUARE_MOVED = "#cad76e"
BLACK_SQUARE_MOVED = "#a1a23e"
SCALE = 100
BOARD_X_SHIFT = 50
BOARD_Y_SHIFT = 75

#chess piece sprites
WHITE_PAWN = pygame.image.load("WPawn.png")
BLACK_PAWN = pygame.image.load("BPawn.png")
WHITE_KNIGHT = pygame.image.load("WKnight.png")
BLACK_KNIGHT = pygame.image.load("BKnight.png")
WHITE_BISHOP = pygame.image.load("WBishop.png")
BLACK_BISHOP = pygame.image.load("BBishop.png")
WHITE_ROOK = pygame.image.load("WRook.png")
BLACK_ROOK = pygame.image.load("BRook.png")
WHITE_QUEEN = pygame.image.load("WQueen.png")
BLACK_QUEEN = pygame.image.load("BQueen.png")
WHITE_KING = pygame.image.load("WKing.png")
BLACK_KING = pygame.image.load("BKing.png")
WHITE_PAWN_PROMOTION = pygame.image.load("WPawn Promote.png")
BLACK_PAWN_PROMOTION = pygame.image.load("BPawn Promote.png")
PROMOTION_BG = pygame.image.load("Promotion BG.png")
UNDO_BUTTON = pygame.image.load("Undo Button.png")
NEW_GAME_BUTTON = pygame.image.load("New Game Button.png")

#starting FEN string
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq – 0 1"

#special chess notations
CASTLING_DICT = {"Ke1g1": "O-O", "Ke1c1": "O-O-O", "Ke8g8": "O-O", "Ke8c8": "O-O-O"}

#variables to help with minimax
INF = 999999

#piece-square tables (shortened to PST) to help with bot move generation
#assigns points to each square on chess board relative to piece
#points > 0 are good positions for bot to move piece into, regardless of capture

KING_PST_WHITE = [[5, 30, 5, 0, 0, 10, 30, 5],
            [20, 20, 0, 0, 0, 0, 20, 20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30]]

KING_PST_BLACK = [[5, 30, 10, 0, 0, 5, 30, 5],
                  [20, 20, 0, 0, 0, 0, 20, 20],
                  [-10, -20, -20, -20, -20, -20, -20, -10],
                  [-20, -30, -30, -40, -40, -30, -30, -20],
                  [-30, -40, -40, -50, -50, -40, -40, -30],
                  [-30, -40, -40, -50, -50, -40, -40, -30],
                  [-30, -40, -40, -50, -50, -40, -40, -30],
                  [-30, -40, -40, -50, -50, -40, -40, -30]]

QUEEN_PST = [[-20, -10, -10, -5, -5, -10, -10, -20],
             [-10, 0, 5, 0, 0, 0, 0, -10],
             [-10, 5, 5, 5, 5, 5, 0, -10],
             [0, 0, 5, 5, 5, 5, 0, -5],
             [-5, 0, 5, 5, 5, 5, 0, -5],
             [-10, 0, 5, 5, 5, 5, 0, -10],
             [-10, 0, 0, 0, 0, 0, 0, -10], 
             [-20, -10, -10, -5,-5, -10, -10, -20]]

ROOK_PST = [[0, 0, 0, 5, 5, 0, 0, 0],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]]

BISHOP_PST = [[-20, -10, -10, -10, -10, -10, -10, -20],
              [-10, 5, 0, 0, 0, 0, 5, -10],
              [-10, 10, 10, 10, 10, 10, 10, -10],
              [-10, 0, 10, 10, 10, 10, 0, -10],
              [-10, 5, 5, 10, 10, 5, 5, -10],
              [-10, 0, 5, 10, 10, 5, 0, -10],
              [-10, 0, 0, 0, 0, 0, 0, -10],
              [-20, -10, -10, -10, -10, -10, -10, -20]]

KNIGHT_PST = [[-50, -40, -30, -30, -30, -30, -40, -50],
              [-40, -20, 0, 5, 5, 0, -20, -40],
              [-30, 5, 10, 15, 15, 10, 5, -30],
              [-30, 0, 15, 20, 20, 15, 0, -30],
              [-30, 5, 15, 20, 20, 15, 5, -30],
              [-30, 0, 10, 15, 15, 10, 0, -30],
              [-40, -20, 0, 0, 0, 0, -20, -40],
              [-50, -40, -30, -30, -30, -30, -40, -50]]

PAWN_PST = [[0, 0, 0, 0, 0, 0, 0, 0], 
            [5, 10, 10, -20, -20, 10, 10, 5],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, 5, 10, 20, 20, 10, 5, 5],
            [10, 10, 10, 15, 15, 10, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [0, 0, 0, 0, 0, 0, 0, 0]]

PST_DICT = {"": PAWN_PST, "N": KNIGHT_PST, "B": BISHOP_PST, "R": ROOK_PST, "Q": QUEEN_PST, "KW": KING_PST_WHITE, "KB": KING_PST_BLACK}

#helper functions

#converts board indexes to GUI coordinates
def index_to_pos(row, col):
    return BOARD_X_SHIFT + col * 100, BOARD_Y_SHIFT + row * 100

#converts board coordinates to indexes
def pos_to_index(x, y):
    return (y - BOARD_Y_SHIFT) // 100, (x - BOARD_X_SHIFT) // 100

#once a chess piece is deselcted, aligns it to centre of square
def align_pos(x, y):
    return (x // 100) * 100 + BOARD_X_SHIFT, (y // 100) * 100 + BOARD_Y_SHIFT

#turns matrix index into chess coordinates if player is white
def chess_notation_white(row, col):
    return "abcdefgh"[col] + str(8 - row)

#turns matrix index into chess coordinates if player is black
def chess_notation_black(row, col):
    return "hgfedcba"[col] + str(row + 1)

#turns chess coordinates to matrix index if player is white
def chess_notation_to_index_white(pos):
    return 8 - int(pos[1]), "abcdefgh".index(pos[0])

#turns chess coordinates to matrix index if player is black
def chess_notation_to_index_black(pos):
    return int(pos[1]) - 1, "hgfedcba".index(pos[0])

#turns chess notation to a pair of coordinates
def chess_move_to_indexes(chess_move):
    #if a pawn move
    if chess_move[0] not in "NBRQK":
        if player_colour:
            r, c = chess_notation_to_index_white(chess_move[0:2])
            new_r, new_c = chess_notation_to_index_white(chess_move[2:])
        else:
            r, c = chess_notation_to_index_black(chess_move[0:2])
            new_r, new_c = chess_notation_to_index_black(chess_move[2:])

    #if other move
    else:
        if player_colour:
            r, c = chess_notation_to_index_white(chess_move[1:3])
            new_r, new_c = chess_notation_to_index_white(chess_move[3:])
        else:
            r, c = chess_notation_to_index_black(chess_move[1:3])
            new_r, new_c = chess_notation_to_index_black(chess_move[3:])

    return r, c, new_r, new_c

#decodes FEN string if player is white
def decode_FEN_white(fen, board):
    pieces, current_turn, can_castle, can_empassant, fifty_move_counter, total_move_counter = fen.split()

    #translates pieces onto the board
    row, col = 0, 0
    for char in pieces:
        x, y = index_to_pos(row, col)
        if char == "/":
            row += 1
            col = 0
        elif char == "p":
            board[row][col] = Pawn("", False, x, y, BLACK_PAWN)
            col += 1
        elif char == "P":
            board[row][col] = Pawn("", True, x, y, WHITE_PAWN)
            col += 1
        elif char == "r":
            board[row][col] = Rook("R", False, x, y, BLACK_ROOK)
            col += 1
        elif char == "R":
            board[row][col] = Rook("R", True, x, y, WHITE_ROOK)
            col += 1
        elif char == "b":
            board[row][col] = Bishop("B", False, x, y, BLACK_BISHOP)
            col += 1
        elif char == "B":
            board[row][col] = Bishop("B", True, x, y, WHITE_BISHOP)
            col += 1
        elif char == "n":
            board[row][col] = Knight("N", False, x, y, BLACK_KNIGHT)
            col += 1
        elif char == "N":
            board[row][col] = Knight("N", True, x, y, WHITE_KNIGHT)
            col += 1
        elif char == "q":
            board[row][col] = Queen("Q", False, x, y, BLACK_QUEEN)
            col += 1
        elif char == "Q":
            board[row][col] = Queen("Q", True, x, y, WHITE_QUEEN)
            col += 1
        elif char == "k":
            board[row][col] = King("K", False, x, y, BLACK_KING)
            col += 1
        elif char == "K":
            board[row][col] = King("K", True, x, y, WHITE_KING)
            col += 1
        else:
            for c in range(col, col + int(char)):
                board[row][c] = 0
            col += int(char)

    return board

#decodes fen string if player is black       
def decode_FEN_black(fen, board):
    pieces, current_turn, can_castle, can_empassant, fifty_move_counter, total_move_counter = fen.split()
    row, col = 7, 7
    for char in pieces:
        x, y = index_to_pos(row, col)
        if char == "/":
            row -=1
            col = 7
        elif char == "p":
            board[row][col] = Pawn("", False, x, y, BLACK_PAWN)
            col -= 1
        elif char == "P":
            board[row][col] = Pawn("", True, x, y, WHITE_PAWN)
            col -= 1
        elif char == "r":
            board[row][col] = Rook("R", False, x, y, BLACK_ROOK)
            col -= 1
        elif char == "R":
            board[row][col] = Rook("R", True, x, y, WHITE_ROOK)
            col -= 1
        elif char == "b":
            board[row][col] = Bishop("B", False, x, y, BLACK_BISHOP)
            col -= 1
        elif char == "B":
            board[row][col] = Bishop("B", True, x, y, WHITE_BISHOP)
            col -= 1
        elif char == "n":
            board[row][col] = Knight("N", False, x, y, BLACK_KNIGHT)
            col -= 1
        elif char == "N":
            board[row][col] = Knight("N", True, x, y, WHITE_KNIGHT)
            col -= 1
        elif char == "q":
            board[row][col] = Queen("Q", False, x, y, BLACK_QUEEN)
            col -= 1
        elif char == "Q":
            board[row][col] = Queen("Q", True, x, y, WHITE_QUEEN)
            col -= 1
        elif char == "k":
            board[row][col] = King("K", False, x, y, BLACK_KING)
            col -= 1
        elif char == "K":
            board[row][col] = King("K", True, x, y, WHITE_KING)
            col -= 1
        else:
            for c in range(col, col - int(char), -1):
                board[row][c] = 0

            col -= int(char)

    return board


class Piece(pygame.sprite.Sprite):
    def __init__(self, name, colour, x_pos, y_pos, image):
        self.name = name
        self.col = colour
        self.x = x_pos
        self.y = y_pos
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def get_pos(self):
        return self.x, self.y

    def get_colour(self):
        return self.col

    def get_name(self):
        return self.name

    def draw(self, screen):
        pygame.Surface.blit(screen, self.img, (self.x, self.y))      

class Pawn(Piece):
    def __init__(self, name, colour, x_pos, y_pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.val = 100
        self.col = colour
        self.x = x_pos
        self.y = y_pos
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Knight(Piece):
    def __init__(self, name, colour, x_pos, y_pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.val = 300
        self.col = colour
        self.x = x_pos
        self.y = y_pos
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Bishop(Piece):
    def __init__(self, name, colour, x_pos, y_pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.val = 300
        self.col = colour
        self.x = x_pos
        self.y = y_pos
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Rook(Piece):
    def __init__(self, name, colour, x_pos, y_pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.val = 500
        self.col = colour
        self.x = x_pos
        self.y = y_pos
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Queen(Piece):
    def __init__(self, name, colour, x_pos, y_pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.val = 900
        self.col = colour
        self.x = x_pos
        self.y = y_pos
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class King(Piece):
    def __init__(self, name, colour, x_pos, y_pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.col = colour
        self.val = 10000
        self.x = x_pos
        self.y = y_pos
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Square:
    def __init__ (self, pos, size, colour, square_colour):
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.col = colour
        self.s_col = square_colour
        self.move_col = WHITE_SQUARE_MOVED if self.col else BLACK_SQUARE_MOVED
        self.draw_col = self.s_col

    def update(self):
        pass
        #will be implemented later to change the colour

    def draw(self, screen):
        pygame.draw.rect(screen, self.draw_col, (self.x, self.y, self.size, self.size))

    def get_pos(self):
        return self.x, self.y

    #change the colour of square to indicate piece move
    def change_green(self):
        self.draw_col = self.move_col

    #changes square colour back to original
    def change_back_colour(self):
        self.draw_col = self.s_col

class Button(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, size_x, size_y, image, bg_image=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_pos
        self.y = y_pos
        self.size_x = size_x
        self.size_y = size_y
        self.img = image
        self.bg_img = bg_image
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        if self.bg_img != None:
            pygame.Surface.blit(screen, self.bg_img, (self.x, self.y))
        pygame.Surface.blit(screen, self.img, (self.x, self.y))

class ChessBoard:
    def __init__(self):
        self.w = 13900
        self.b = 13900

    def get_piece_scores(self):
        return self.w, self.b

class ChessBot:
    def __init__(self, colour):
        self.col = colour 
        self.positions = 0

    #main function which determins which move the bot will play next
    def minimax(self, board, depth, alpha, beta, bot_turn, cb_pieces, cb):
        if depth == 0:
            self.positions += 1
            return self.evaluate_board(cb, board, board.fen()), None

        moves = [move for move in board.legal_moves]
        #if there are no legal moves
        if not moves:
            if board.is_checkmate():
                if bot_turn:
                    return -INF, None
                else:
                    return INF, None
            #else stalemate
            return 0, None

        #best_move = random.choice(moves)
        best_move = None

        if bot_turn:
            #bot is the maximizing player in minimax
            max_eval = -INF
            for move in moves:

                self.positions += 1

                #helps update chessboard piece scores
                move_coord = str(move)

                #if castling, has to update piece array differently
                if move_coord == "e8c8" or move_coord == "e8g8" or move_coord == "e1g1" or move_coord == "e1c1":
                    board.push(move)
                    if self.col:
                        cb_pieces = decode_FEN_black(board.fen(), cb_pieces)
                    else:
                        cb_pieces = decode_FEN_white(board.fen(), cb_pieces)

                    evaluation, m = self.minimax(board, depth - 1, alpha, beta, False, cb_pieces, cb)

                    #add positional score
                    #if king-side castle
                    if move_coord == "e1g1" or move_coord == "e8g8":
                        evaluation += 30
                    else:
                        evaluation += 10

                    board.pop()
                    if self.col:
                        cb_pieces = decode_FEN_black(board.fen(), cb_pieces)
                    else:
                        cb_pieces = decode_FEN_white(board.fen(), cb_pieces)
                else:
                    r, c, new_r, new_c = chess_move_to_indexes(move_coord)
                    moved_piece = cb_pieces[r][c]
                    #equals 0 if no piece was captured
                    captured_piece = cb_pieces[new_r][new_c]
                    value = 0
                    if captured_piece != 0:
                        value = captured_piece.val
                    cb_pieces[r][c], cb_pieces[new_r][new_c] = 0, moved_piece
                    if self.col:
                        cb.b -= value
                    else:
                        cb.w -= value

                    board.push(move)
                    evaluation, m = self.minimax(board, depth - 1, alpha, beta, False, cb_pieces, cb)

                    #adds position score to evaluation
                    #print(moved_piece, r, c, new_r, new_c)
                    evaluation += self.evaluate_position(moved_piece.name, new_r, new_c)

                    #checks for any pawn attacks on the new square
                    evaluation += self.check_pawn_attacks(moved_piece, new_r, new_c, cb_pieces)

                    board.pop()

                    #helps update chessboard piece scores back to normal
                    cb_pieces[r][c], cb_pieces[new_r][new_c] = moved_piece, captured_piece
                    if self.col:
                        cb.b += value
                    else:
                        cb.w += value

                #if depth == 4:
                    #print(move, evaluation, "depth 4")

                alpha = max(alpha, evaluation)

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move

                #player had a better move elsewhere, can skip evaluating
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            #player is the minimizing player in minimax
            min_eval = INF
            for move in moves:

                self.positions += 1
                
                #helps update chessboard piece scores
                move_coord = str(move)
                #if castling, has to update piece array differently
                if move_coord == "e8c8" or move_coord == "e8g8" or move_coord == "e1g1" or move_coord == "e1c1":
                    board.push(move)
                    if self.col:
                        cb_pieces = decode_FEN_black(board.fen(), cb_pieces)
                    else:
                        cb_pieces = decode_FEN_white(board.fen(), cb_pieces)

                    evaluation, m = self.minimax(board, depth - 1, alpha, beta, False, cb_pieces, cb)

                    board.pop()
                    if self.col:
                        cb_pieces = decode_FEN_black(board.fen(), cb_pieces)
                    else:
                        cb_pieces = decode_FEN_white(board.fen(), cb_pieces)

                else:
                    r, c, new_r, new_c = chess_move_to_indexes(move_coord)
                    moved_piece = cb_pieces[r][c]
                    #equals 0 if no piece was captured
                    captured_piece = cb_pieces[new_r][new_c]
                    value = 0
                    if captured_piece != 0:
                        value = captured_piece.val
                    cb_pieces[r][c], cb_pieces[new_r][new_c] = 0, moved_piece
                    if self.col:
                        cb.w -= value
                    else:
                        cb.b -= value

                    board.push(move)
                    evaluation, m = self.minimax(board, depth - 1, alpha, beta, True, cb_pieces, cb)
                    board.pop()

                    #helps update chessboard piece scores back to normal
                    cb_pieces[r][c], cb_pieces[new_r][new_c] = moved_piece, captured_piece
                    if self.col:
                        cb.w += value
                    else:
                        cb.b += value

                if evaluation < min_eval:
                    min_eval = evaluation

                beta = min(beta, evaluation)
                #bot had a better move elsewhere, can skip evaluating
                if beta <= alpha:
                    break
                
            return min_eval, best_move

    #evaluates entire state of the board using the board's fen
    def evaluate_board(self, cb, board, fen):
        pieces, current_turn, can_castle, can_empassant, fifty_move_counter, total_move_counter = fen.split()

        #board_pieces = [[0 for i in range(8)] for i in range(8)]
        #board_pieces = decode_FEN_white(fen, board_pieces) if self.col else decode_FEN_black(fen, board_pieces)
        return self.evaluate_pieces(cb)

    #finds the material value score for bot and player, returns the difference
    #if score < 0, player is winning; score > 0, bot is winning; score == 0, even
    def evaluate_pieces(self, cb):
        if self.col:
            return cb.w - cb.b
        else:
            return cb.b - cb.w

    def evaluate_position(self, piece_name, new_r, new_c):
        #if piece is a pawn
        if len(piece_name) == 0:
            return PST_DICT[""][new_r][new_c]
        #king PST does not apply to end games
        elif piece_name == "K" and end_game:
            return 0

        elif piece_name == "K":
            #setting value to -5 prevents bot from making same king moves over and over again
            if self.col:
                points = PST_DICT["KW"][new_r][new_c]
                PST_DICT["KW"][new_r][new_c] = -5
                return points
            else:
                points =  PST_DICT["KB"][new_r][new_c]
                PST_DICT["KB"][new_r][new_c] = -5
                return points
        else:
            return PST_DICT[piece_name][new_r][new_c]

    #if new square moved has a pawn attacking that square, subtracts 100 points from evaluation
    def check_pawn_attacks(self, piece, new_r, new_c, piece_arr):
        if piece.name in "NBRQ":
            if new_r + 1 < 8:
                if new_c - 1 > -1:
                    if piece_arr[new_r + 1][new_c -1] != 0 and piece_arr[new_r + 1][new_c -1].val == 100:
                        return -piece.val
                elif new_c + 1 < 8:
                    if piece_arr[new_r + 1][new_c + 1] != 0 and piece_arr[new_r + 1][new_c + 1].val == 100:
                        return -piece.val
        return 0

#game functions
def new_game():
    global cb, cb_squares, cb_pieces, player_colour, board, chess_bot, running, dragging, dragged_piece, pawn_promotion, has_updated, load_time, has_loaded, player_turn, end_game, text, bot_text, position_move_log, new_game_b, undo_b, temp_paused, temp_paused_counter

    #game loop variables
    running = True
    dragging = False
    dragged_piece = None
    pawn_promotion = False
    has_updated = False
    load_time = 0
    end_game = False
    temp_paused = False
    temp_paused_counter = 0
    text = "White's turn."
    bot_text = "..."
    #tracks moves played in game according to coordinates, helps with updating board square colours
    position_move_log = []

    cb = ChessBoard()
    board = chess.Board()
    new_game_b = Button(950, 775, 150, 100, NEW_GAME_BUTTON)
    undo_b = Button (1150, 775, 150, 100, UNDO_BUTTON)
    #creating the chessboard array
    cb_squares = [[0 for i in range(8)] for i in range(8)]
    for row in range(8):
        for col in range(8):
            x, y = index_to_pos(row, col)
            #if white square
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                cb_squares[row][col] = Square((x, y), SCALE, True, WHITE_SQUARE)
                
            #else black square
            else:
                cb_squares[row][col] = Square((x, y), SCALE, False, BLACK_SQUARE)

    #randomly picks colour for player
    num = random.randint(1, 2)
    #player is white if True else black
    player_colour = num == 1
    chess_bot = ChessBot(not player_colour)
    has_loaded = player_colour == True
    player_turn = player_colour == True

    #creating the chess pieces array
    cb_pieces = [[0 for i in range(8)] for i in range(8)]
    if player_colour:
        cb_pieces = decode_FEN_white(START_FEN, cb_pieces)
    else:
        cb_pieces = decode_FEN_black(START_FEN, cb_pieces)

#takes in original and new index of piece in matrix, converts it into chess notation and checks validity
def make_move(name, row, col, new_row, new_col, colour):
    global pawn_promotion, dragging, cb_pieces, chess_move, position_move_log, cb
    #chess_move is global to deal with the special case of a pawn promotion
    #rows represented with 1-8
    #cols represented with a-g

    #value gained by moving piece to new square, if legal
    value = 0

    #building the string to input
    if player_colour:
        chess_move = name + chess_notation_white(row, col) + chess_notation_white(new_row, new_col)
    else:
        chess_move = name + chess_notation_black(row, col) + chess_notation_black(new_row, new_col)

    r, c, new_r, new_c = chess_move_to_indexes(chess_move)

    #tries to make the move inputted by player, returns True if move can be made, False if not
    try:
        #if move is an attempted castle
        if chess_move in CASTLING_DICT:

            board.push_san(CASTLING_DICT[chess_move])
            #print(board)
            
        #if the move is a pawn, tries to see if it results in a promotion
        elif chess_move[0] not in "NRBQK":

            try:
                #test promotion move by defaulting pawn promotion to a queen
                board.push_san(chess_move + "Q")
                #if the above doesn't error, undos the move so that the player can chose what piece to promote to
                board.pop()
                pawn_promotion = True
                dragging = False

                 #checks if a piece will be captured
                #if so, needs to get the value of the piece to update the piece scores for each colour
                if cb_pieces[new_r][new_c] != 0:
                    value = cb_pieces[new_r][new_c].val
                if colour:
                    cb.b -= value
                else:
                    cb.w -= value

            except:
                #checks if a piece will be captured
                #if so, needs to get the value of the piece to update the piece scores for each colour
                if cb_pieces[new_r][new_c] != 0:
                    value = cb_pieces[new_r][new_c].val
                board.push_san(chess_move)
                if colour:
                    cb.b -= value
                else:
                    cb.w -= value

        else:
            if cb_pieces[new_r][new_c] != 0:
                value = cb_pieces[new_r][new_c].val
            board.push_san(chess_move)
            if colour:
                cb.b -= value
            else:
                cb.w -= value

        #will only run if legal move was made, updates the colour of the squares

        #if there was another move made before the current one, the old green squares must be reverted to original colour
        if position_move_log:
            last_move = position_move_log[-1]
            prev_r, prev_c, prev_new_r, prev_new_c = chess_move_to_indexes(last_move)
            cb_squares[prev_r][prev_c].change_back_colour()
            cb_squares[prev_new_r][prev_new_c].change_back_colour()

        #changes new squares to green
        cb_squares[r][c].change_green()
        cb_squares[new_r][new_c].change_green()

        position_move_log.append(chess_move)
        return True

    except:
        return False

#handles the special case of pawn promotion
def promotion_move(move):
    global cb_pieces
    board.push_san(move)
    if player_colour:
        cb_pieces = decode_FEN_white(board.fen(), cb_pieces)
    else:
        cb_pieces = decode_FEN_black(board.fen(), cb_pieces)

def bot_move(move, colour):
    global cb_pieces, cb

    #gets the board coordinates of the old and new pos
    move_coord = str(move)
    r, c, new_r, new_c = chess_move_to_indexes(move_coord)

    #makes the move
    board.push(move)

    #updates board piece scores
    value = 0
    if cb_pieces[new_r][new_c] != 0:
        value = cb_pieces[new_r][new_c].val
    if colour:
        cb.b -= value
    else:
        cb.w -= value

     #if there was another move made before the current one, the old green squares must be reverted to original colour
    if position_move_log:
        last_move = position_move_log[-1]
        prev_r, prev_c, prev_new_r, prev_new_c = chess_move_to_indexes(last_move)
        cb_squares[prev_r][prev_c].change_back_colour()
        cb_squares[prev_new_r][prev_new_c].change_back_colour()

    #changes new squares to green
    cb_squares[r][c].change_green()
    cb_squares[new_r][new_c].change_green()

    position_move_log.append(move_coord)

    #gets the FEN string of the board and updates the GUI from it
    if player_colour:
        cb_pieces = decode_FEN_white(board.fen(), cb_pieces)
    else:
        cb_pieces = decode_FEN_black(board.fen(), cb_pieces)

#set a refresh rate for display screen
FPS = 60
FramePerSec = pygame.time.Clock()

#initialize
pygame.init()
pygame.font.init()

#display parameters
SCREEN = pygame.display.set_mode((1400, 950))
pygame.display.set_caption("Chess Game")
display_font = pygame.font.SysFont('Comic Sans MS', 30)
square_font = pygame.font.SysFont('Comic Sans MS', 25)

new_game()

#game loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        #checks for a piece being selected by mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos


                #if clicks undo button
                if 1150 <= mouse_x <= 1300 and 775 <= mouse_y <= 875:
                    temp_paused = True
                    if position_move_log:
                        position_move_log.pop(-1)
                        board.pop()

                        #changes squares back to original colour
                        for r in range(8):
                            for c in range(8):
                                cb_squares[r][c].change_back_colour()

                        #updates board
                        if player_colour:
                            cb_pieces = decode_FEN_white(board.fen(), cb_pieces)
                        else:
                            cb_pieces = decode_FEN_black(board.fen(), cb_pieces)

                        player_turn = board.turn if player_colour else not board.turn



                elif 950 <= mouse_x <= 1100 and 775 <= mouse_y <= 875:
                    new_game()

                elif player_turn:
                    if not pawn_promotion:
                        for i in range(8):
                            for j in range(8):
                                piece = cb_pieces[i][j]
                                if piece != 0:
                                    #if there is collision with a piece
                                    if piece.rect.collidepoint(event.pos):
                                        dragging = True
                                        dragged_piece = piece
                                        original_x, original_y = piece.x, piece.y
                                        mouse_x, mouse_y = event.pos
                                        #calculates the off set from mouse contact and top-left corner
                                        offset_x = piece.x - mouse_x
                                        offset_y = piece.y - mouse_y

                    elif pawn_promotion:
                        x, y = event.pos
                        #if queen selected
                        if 50 <= x < 250 and 400 <= y <= 600:
                            promotion_move(chess_move + "Q")
                            pawn_promotion = False
                            if player_colour:
                                cb.w += 900
                            else:
                                cb.b += 900

                        #if knight selected
                        elif 250 <= x < 450 and 400 <= y <= 600:
                            promotion_move(chess_move + "N")
                            pawn_promotion = False
                            if player_colour:
                                cb.w += 300
                            else:
                                cb.b += 300

                        #if rook selected
                        elif 450 <= x < 650 and 400 <= y <= 600:
                            promotion_move(chess_move + "R")
                            pawn_promotion = False
                            if player_colour:
                                cb.w += 500
                            else:
                                cb.b += 500

                        #if bishop selected
                        elif 650 <= x < 850 and 400 <= y <= 600:
                            promotion_move(chess_move + "B")
                            pawn_promotion = False
                            if player_colour:
                                cb.w += 300
                            else:
                                cb.b += 300

                        player_turn = False

        #checks for piece being unselected by mouse
        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and dragging:            
                dragging = False

                #checks if the position of the mouse is within the chessboard
                if 50 <= mouse_x < 850 and 75 <= mouse_y < 850:
                    x, y = align_pos(mouse_x + offset_x, mouse_y + offset_y)
                    
                    row, col = pos_to_index(x, y)
                    original_row, original_col = pos_to_index(original_x, original_y)

                    legal = make_move(dragged_piece.name, original_row, original_col, row, col, player_colour)
                    
                    if legal:
                        
                        #gets the FEN string of the board and updates the GUI from it
                        if player_colour:
                            cb_pieces = decode_FEN_white(board.fen(), cb_pieces)
                        else:
                            cb_pieces = decode_FEN_black(board.fen(), cb_pieces)
                        player_turn = False
                        #special pawn promotion case, needs to draw the pawn in new position before promoting
                        if pawn_promotion:
                            player_turn = True
                            dragged_piece.x = x
                            dragged_piece.y = y
                            cb_pieces[row][col] = dragged_piece
                            cb_pieces[original_row][original_col] = 0
                
                    else:
                        dragged_piece.x = original_x
                        dragged_piece.y = original_y
                        dragged_piece.rect.x = original_x
                        dragged_piece.rect.y = original_y

                else:
                    dragged_piece.x = original_x
                    dragged_piece.y = original_y
                    dragged_piece.rect.x = original_x
                    dragged_piece.rect.y = original_y

                dragged_piece = None
                
        #checks for mouse movement
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                #updates position of moved piece
                dragged_piece.x = mouse_x + offset_x
                dragged_piece.y = mouse_y + offset_y
                dragged_piece.rect.x = dragged_piece.x
                dragged_piece.rect.y = dragged_piece.y
                
    #draws the background
    SCREEN.fill((0, 0, 0))
    
    #draws the chessboard
    for i in range(8):
        for j in range(8):
            cb_squares[i][j].draw(SCREEN)

    new_game_b.draw(SCREEN)
    undo_b.draw(SCREEN)

    #draws the text labelling squares
    #bot_text_surface = display_font.render(bot_text, False, (255, 255, 255))
    #SCREEN.blit(bot_text_surface, (900, 100))
    if player_colour:
        a = square_font.render("a", False, WHITE_SQUARE)
        b = square_font.render("b", False, BLACK_SQUARE)
        c = square_font.render("c", False, WHITE_SQUARE)
        d = square_font.render("d", False, BLACK_SQUARE)
        e = square_font.render("e", False, WHITE_SQUARE)
        f = square_font.render("f", False, BLACK_SQUARE)
        g = square_font.render("g", False, WHITE_SQUARE)
        h = square_font.render("h", False, BLACK_SQUARE)

        one = square_font.render("1", False, WHITE_SQUARE)
        two = square_font.render("2", False, BLACK_SQUARE)
        three = square_font.render("3", False, WHITE_SQUARE)
        four = square_font.render("4", False, BLACK_SQUARE)
        five = square_font.render("5", False, WHITE_SQUARE)
        six = square_font.render("6", False, BLACK_SQUARE)
        seven = square_font.render("7", False, WHITE_SQUARE)
        eight = square_font.render("8", False, BLACK_SQUARE)

        SCREEN.blit(a, (130, 835))
        SCREEN.blit(b, (230, 835))
        SCREEN.blit(c, (330, 835))
        SCREEN.blit(d, (430, 835))
        SCREEN.blit(e, (530, 835))
        SCREEN.blit(f, (630, 835))
        SCREEN.blit(g, (730, 835))
        SCREEN.blit(h, (830, 835))

        SCREEN.blit(one, (55, 775))
        SCREEN.blit(two, (55, 675))
        SCREEN.blit(three, (55, 575))
        SCREEN.blit(four, (55, 475))
        SCREEN.blit(five, (55, 375))
        SCREEN.blit(six, (55, 275))
        SCREEN.blit(seven, (55, 175))
        SCREEN.blit(eight, (55, 75))

    else:
        h = square_font.render("h", False, WHITE_SQUARE)
        g = square_font.render("g", False, BLACK_SQUARE)
        f = square_font.render("f", False, WHITE_SQUARE)
        e = square_font.render("e", False, BLACK_SQUARE)
        d = square_font.render("d", False, WHITE_SQUARE)
        c = square_font.render("c", False, BLACK_SQUARE)
        b = square_font.render("b", False, WHITE_SQUARE)
        a = square_font.render("a", False, BLACK_SQUARE)

        eight = square_font.render("8", False, WHITE_SQUARE)
        seven = square_font.render("7", False, BLACK_SQUARE)
        six = square_font.render("6", False, WHITE_SQUARE)
        five = square_font.render("5", False, BLACK_SQUARE)
        four = square_font.render("4", False, WHITE_SQUARE)
        three = square_font.render("3", False, BLACK_SQUARE)
        two = square_font.render("2", False, WHITE_SQUARE)
        one = square_font.render("1", False, BLACK_SQUARE)

        SCREEN.blit(h, (130, 835))
        SCREEN.blit(g, (230, 835))
        SCREEN.blit(f, (330, 835))
        SCREEN.blit(e, (430, 835))
        SCREEN.blit(d, (530, 835))
        SCREEN.blit(c, (630, 835))
        SCREEN.blit(b, (730, 835))
        SCREEN.blit(a, (830, 835))

        SCREEN.blit(eight, (55, 775))
        SCREEN.blit(seven, (55, 675))
        SCREEN.blit(six, (55, 575))
        SCREEN.blit(five, (55, 475))
        SCREEN.blit(four, (55, 375))
        SCREEN.blit(three, (55, 275))
        SCREEN.blit(two, (55, 175))
        SCREEN.blit(one, (55, 75))

    #draws the chess pieces
    for i in range(8):
        for j in range(8):
            if cb_pieces[i][j] != 0 and cb_pieces[i][j] != dragged_piece:
                cb_pieces[i][j].draw(SCREEN)

    #ensures that the piece selected will always appear on top
    if dragging:           
        dragged_piece.draw(SCREEN)

    #if pawn is to be promoted, pauses the game so player can choose which piece to promote to
    if pawn_promotion:
        #if whites turn
        if board.turn:
            promotion_button = Button(50, 400, 800, 200, WHITE_PAWN_PROMOTION, PROMOTION_BG)
        else:
            promotion_button = Button(50, 400, 800, 200, BLACK_PAWN_PROMOTION, PROMOTION_BG)

        promotion_button.draw(SCREEN)

    #helpful text showing the state of the game
    if board.is_checkmate():
        winner = "White" if not board.turn else "Black"
        text = winner + " wins by checkmate."
    elif board.is_stalemate():
        text = "Stalemate, neither side wins."
    elif board.is_fivefold_repetition():
        text = "Stalemate by five-fold repetition."
    elif board.is_seventyfive_moves():
        text = "Stalemate, no pawn moves after seventy-five moves."
    elif board.turn:
        text = "White's turn."
    elif not board.turn:
        text = "Black's turn."

    #waits two seconds after undo button was pressed, then resumes game for bot
    if temp_paused:
        temp_paused_counter += 1
        if temp_paused_counter == 120:
            temp_paused = False
            temp_paused_counter = 0
            has_updated = False

    #if not player's turn, not during pawn promotion, not game over, and screen has updated, meets requirements to start bot move
    #has_loaded prevents the bot from making the first move (if white) before GUI has finished loading
    #print(not player_turn, not pawn_promotion, not board.is_game_over(), has_updated, has_loaded)
    if not player_turn and not pawn_promotion and not board.is_game_over() and has_updated and has_loaded and not temp_paused:
        score, move = chess_bot.minimax(board, 4, -INF, INF, True, cb_pieces, cb)
        bot_text = str(chess_bot.positions) + " positions evaluated."
        score2, move2 = chess_bot.minimax(board, 2, -INF, INF, True, cb_pieces, cb)
        #print("depth 4:", move, score)
        #print("depth 2:", move2, score2)

        #evaluates at depth 4 and 2 to prevent bot from making worse moves due to overthinking
        if score > score2:
            bot_move(move, chess_bot.col)
        else:
            bot_move(move2, chess_bot.col)
        
        chess_bot.positions = 0
        player_turn = True
        has_updated = False
    
    #ensures piece updates into new position before making bot move
    if not player_turn and not has_updated:
        has_updated = True
        bot_text = "Evaluating..."

    if board.is_game_over() or temp_paused:
        bot_text = "..."

    #if bot is white, waits one second before playing first move
    if not has_loaded:
        load_time += 1
        if load_time >= 60:
            has_loaded = True

    #checks if end game with rough estimate of pieces left
    if cb.w <= 11500 and cb.b <= 11500:
        end_game = True

    #drawing the text
    text_surface = display_font.render(text, False, (255, 255, 255))
    SCREEN.blit(text_surface, (900, 75))

    bot_text_surface = display_font.render(bot_text, False, (255, 255, 255))
    SCREEN.blit(bot_text_surface, (900, 150))

    bot_name = display_font.render("Chess Bot", False, (255, 255, 255))
    SCREEN.blit(bot_name, (50, 25))

    player_name = display_font.render("Player", False, (255, 255, 255))
    SCREEN.blit(player_name, (50, 880))

    new_game_text = display_font.render("New Game", False, (255, 255, 255))
    SCREEN.blit(new_game_text, (950, 725))

    undo_text = display_font.render("Undo", False, (255, 255, 255))
    SCREEN.blit(undo_text, (1187, 725))

    #shows who is up in material
    #if white material - black material != 0, one player must be up material
    player_adv = False
    bot_adv = False
    advantage = 0
    if cb.w - cb.b != 0:
        advantage = int(math.fabs(cb.w - cb.b) // 100)
        difference = cb.w - cb.b

        #player is white and up material
        if player_colour and difference > 0:
            player_adv = True
        #player is black and up material
        elif not player_colour and difference < 0:
            player_adv = True
        else:
            bot_adv = True

    score_text = "(+" + str(advantage) + ")"

    if player_adv:
        player_score = display_font.render(score_text, False, (255, 255, 255))
        SCREEN.blit(player_score, (150, 880))
    elif bot_adv:
        bot_score = display_font.render(score_text, False, (255, 255, 255))
        SCREEN.blit(bot_score, (200, 25))


    #print(board.turn) True if white, False if black
    pygame.display.update()
    FramePerSec.tick(FPS)