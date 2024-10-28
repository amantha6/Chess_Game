from typing import List, Tuple
import copy

class ChessPiece:
    def __init__(self, color: str, piece_type: str, position: Tuple[int, int]):
        self.color = color
        self.piece_type = piece_type
        self.position = position
        self.has_moved = False

    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        row, col = self.position

        if self.piece_type == 'pawn':
            direction = 1 if self.color == 'black' else -1
            
            # Forward move
            if 0 <= row + direction < 8 and board[row + direction][col] is None:
                moves.append((row + direction, col))
                # Initial two-square move
                if not self.has_moved and 0 <= row + 2*direction < 8 and board[row + 2*direction][col] is None:
                    moves.append((row + 2*direction, col))
            
            # Captures
            for c in [-1, 1]:
                if 0 <= row + direction < 8 and 0 <= col + c < 8:
                    target = board[row + direction][col + c]
                    if target and target.color != self.color:
                        moves.append((row + direction, col + c))

        elif self.piece_type == 'knight':
            knight_moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            for move in knight_moves:
                new_row, new_col = row + move[0], col + move[1]
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = board[new_row][new_col]
                    if target is None or target.color != self.color:
                        moves.append((new_row, new_col))

        elif self.piece_type in ['bishop', 'rook', 'queen']:
            directions = []
            if self.piece_type in ['bishop', 'queen']:
                directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            if self.piece_type in ['rook', 'queen']:
                directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for direction in directions:
                for i in range(1, 8):
                    new_row = row + direction[0] * i
                    new_col = col + direction[1] * i
                    if not (0 <= new_row < 8 and 0 <= new_col < 8):
                        break
                    target = board[new_row][new_col]
                    if target is None:
                        moves.append((new_row, new_col))
                    elif target.color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break

        elif self.piece_type == 'king':
            king_moves = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)
            ]
            for move in king_moves:
                new_row, new_col = row + move[0], col + move[1]
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = board[new_row][new_col]
                    if target is None or target.color != self.color:
                        moves.append((new_row, new_col))

        return moves

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.move_history = []
        self.initialize_board()
        self.is_check = False
        self.is_checkmate = False

    def initialize_board(self):
        # Initialize pawns
        for col in range(8):
            self.board[1][col] = ChessPiece('black', 'pawn', (1, col))
            self.board[6][col] = ChessPiece('white', 'pawn', (6, col))
        
        # Initialize other pieces
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col in range(8):
            self.board[0][col] = ChessPiece('black', piece_order[col], (0, col))
            self.board[7][col] = ChessPiece('white', piece_order[col], (7, col))

    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        piece = self.board[from_pos[0]][from_pos[1]]
        if not piece or piece.color != self.current_player:
            return False
        
        possible_moves = piece.get_possible_moves(self.board)
        if to_pos not in possible_moves:
            return False
            
        # Test move for check
        test_board = copy.deepcopy(self.board)
        test_board[to_pos[0]][to_pos[1]] = test_board[from_pos[0]][from_pos[1]]
        test_board[from_pos[0]][from_pos[1]] = None
        
        if self.is_in_check(self.current_player, test_board):
            return False
            
        return True

    def is_in_check(self, color: str, board=None) -> bool:
        if board is None:
            board = self.board

        # Find king position
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == color and piece.piece_type == 'king':
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos:  # This shouldn't happen in a valid game
            return False
        
        # Check if any opponent piece can capture the king
        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == opponent_color:
                    if king_pos in piece.get_possible_moves(board):
                        return True
        return False

    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        if not self.is_valid_move(from_pos, to_pos):
            return False

        # Record the move
        self.move_history.append({
            'from': from_pos,
            'to': to_pos
        })

        # Make the move
        piece = self.board[from_pos[0]][from_pos[1]]
        self.board[to_pos[0]][to_pos[1]] = piece
        self.board[from_pos[0]][from_pos[1]] = None
        if piece:
            piece.position = to_pos
            piece.has_moved = True

        # Switch players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        # Update check status
        self.is_check = self.is_in_check(self.current_player)
        if self.is_check:
            self.is_checkmate = self.is_checkmate_state()
            
        return True

    def undo_move(self) -> bool:
        if not self.move_history:
            return False

        last_move = self.move_history.pop()
        from_pos = last_move['from']
        to_pos = last_move['to']
        
        # Move the piece back
        piece = self.board[to_pos[0]][to_pos[1]]
        self.board[from_pos[0]][from_pos[1]] = piece
        self.board[to_pos[0]][to_pos[1]] = None
        
        if piece:
            piece.position = from_pos
            piece.has_moved = False
        
        # Switch back to previous player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        # Reset check/checkmate status
        self.is_check = self.is_in_check(self.current_player)
        self.is_checkmate = False
        
        return True

    def is_checkmate_state(self) -> bool:
        # Check if any piece can make a legal move
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == self.current_player:
                    possible_moves = piece.get_possible_moves(self.board)
                    for move in possible_moves:
                        if self.is_valid_move((row, col), move):
                            return False
        return True