import pygame
import os
from chess_pieces import ChessBoard, ChessPiece

# Initialize Pygame and its mixer for sound effects
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_SIZE = 900  # Increased to accommodate move history
BOARD_SIZE = 700
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (118, 150, 86)
LIGHT_GREEN = (238, 238, 210)
YELLOW = (186, 202, 43)
BLUE = (0, 0, 255, 50)
RED = (255, 0, 0, 50)

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, BOARD_SIZE))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        
        # Load resources
        self.load_images()
        self.load_sounds()
        
        # Initialize game state
        self.chess_board = ChessBoard()
        self.selected_piece = None
        self.selected_pos = None
        self.possible_moves = []
        
        # Initialize fonts
        self.font = pygame.font.Font(None, 24)
        
        # Move history display
        self.move_history_surface = pygame.Surface((WINDOW_SIZE - BOARD_SIZE, BOARD_SIZE))
        self.move_history_surface.fill(WHITE)

    def load_images(self):
        self.piece_images = {}
        piece_letters = {
            'pawn': 'P',
            'rook': 'R',
            'knight': 'N',  # N for kNight to avoid confusion with King
            'bishop': 'B',
            'queen': 'Q',
            'king': 'K'
        }
        
        for color in ['white', 'black']:
            self.piece_images[color] = {}
            base_color = WHITE if color == 'white' else BLACK
            outline_color = BLACK if color == 'white' else WHITE
            
            for piece_type, letter in piece_letters.items():
                surface = pygame.Surface((SQUARE_SIZE - 20, SQUARE_SIZE - 20), pygame.SRCALPHA)
                
                # Draw circle background
                pygame.draw.circle(surface, base_color, 
                                (SQUARE_SIZE//2 - 10, SQUARE_SIZE//2 - 10), 
                                SQUARE_SIZE//3)
                pygame.draw.circle(surface, outline_color, 
                                (SQUARE_SIZE//2 - 10, SQUARE_SIZE//2 - 10), 
                                SQUARE_SIZE//3, 2)
                
                # Draw letter
                font = pygame.font.Font(None, int(SQUARE_SIZE//2))  # Larger font size
                text = font.render(letter, True, outline_color)
                text_rect = text.get_rect(center=(SQUARE_SIZE//2 - 10, SQUARE_SIZE//2 - 10))
                surface.blit(text, text_rect)
                
                self.piece_images[color][piece_type] = surface

    def load_sounds(self):
        self.sounds = {}
        # Simple initialization without actual sound files
        for sound_name in ['move', 'capture', 'check']:
            self.sounds[sound_name] = None

    def draw_board(self):
        # Draw squares
        for row in range(8):
            for col in range(8):
                color = LIGHT_GREEN if (row + col) % 2 == 0 else DARK_GREEN
                pygame.draw.rect(self.screen, color,
                               (col * SQUARE_SIZE, row * SQUARE_SIZE,
                                SQUARE_SIZE, SQUARE_SIZE))

        # Highlight selected piece
        if self.selected_pos:
            pygame.draw.rect(self.screen, YELLOW,
                           (self.selected_pos[1] * SQUARE_SIZE,
                            self.selected_pos[0] * SQUARE_SIZE,
                            SQUARE_SIZE, SQUARE_SIZE))

        # Highlight king in check with red background
        if self.chess_board.is_check:
            # Find the king position
            for row in range(8):
                for col in range(8):
                    piece = self.chess_board.board[row][col]
                    if (piece and piece.piece_type == 'king' and 
                        piece.color == self.chess_board.current_player):
                        # Draw red highlight for king in check
                        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        s.fill((255, 0, 0, 100))  # Semi-transparent red
                        self.screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

        # Highlight possible moves
        for move in self.possible_moves:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((0, 0, 255, 100))  # Semi-transparent blue
            self.screen.blit(s, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE))

        # Draw pieces
        for row in range(8):
            for col in range(8):
                piece = self.chess_board.board[row][col]
                if piece:
                    piece_img = self.piece_images[piece.color][piece.piece_type]
                    img_rect = piece_img.get_rect()
                    img_rect.center = (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                     row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    self.screen.blit(piece_img, img_rect)

        # Draw move history
        self.draw_move_history()

        # Draw check/checkmate status with alert box
        if self.chess_board.is_checkmate:
            # Draw alert box for checkmate
            alert_surface = pygame.Surface((300, 100), pygame.SRCALPHA)
            alert_surface.fill((0, 0, 0, 180))  # Semi-transparent black background
            winner = 'Black' if self.chess_board.current_player == 'white' else 'White'
            text = self.font.render(f"Checkmate! {winner} wins!", True, RED)
            text_rect = text.get_rect(center=(150, 50))
            alert_surface.blit(text, text_rect)
            self.screen.blit(alert_surface, 
                            ((WINDOW_SIZE - 300)//2, (BOARD_SIZE - 100)//2))
        elif self.chess_board.is_check:
            # Draw alert box for check
            alert_surface = pygame.Surface((300, 100), pygame.SRCALPHA)
            alert_surface.fill((0, 0, 0, 180))  # Semi-transparent black background
            text = self.font.render(f"{self.chess_board.current_player.upper()} KING IS IN CHECK!", True, RED)
            text_rect = text.get_rect(center=(150, 50))
            alert_surface.blit(text, text_rect)
            self.screen.blit(alert_surface, 
                            ((WINDOW_SIZE - 300)//2, (BOARD_SIZE - 100)//2))

    def draw_move_history(self):
        # Clear the move history surface
        self.move_history_surface.fill(WHITE)
        
        # Draw title
        title = self.font.render("Move History", True, BLACK)
        self.move_history_surface.blit(title, (10, 10))
        
        # Draw moves in simpler format
        for i, move in enumerate(self.chess_board.move_history[-15:]):  # Show last 15 moves
            from_pos = move['from']
            to_pos = move['to']
            
            # Simple algebraic notation (e.g., "e2 to e4")
            from_square = f"{chr(97 + from_pos[1])}{8 - from_pos[0]}"
            to_square = f"{chr(97 + to_pos[1])}{8 - to_pos[0]}"
            
            move_text = f"{i+1}. {from_square} → {to_square}"
            text = self.font.render(move_text, True, BLACK)
            self.move_history_surface.blit(text, (10, 40 + i * 20))
        
        # Draw the move history surface
        self.screen.blit(self.move_history_surface, (BOARD_SIZE, 0))

    def handle_click(self, pos):
        if pos[0] >= BOARD_SIZE:  # Click in move history panel
            return

        row = pos[1] // SQUARE_SIZE
        col = pos[0] // SQUARE_SIZE
        clicked_pos = (row, col)

        print(f"Clicked position: {clicked_pos}")
        print(f"Current player: {self.chess_board.current_player}")

        if self.selected_pos:
            # Try to make a move
            print(f"Attempting move from {self.selected_pos} to {clicked_pos}")
            if self.chess_board.make_move(self.selected_pos, clicked_pos):
                print("Move successful")
                # Check if the move resulted in check
                if self.chess_board.is_check:
                    print(f"{self.chess_board.current_player.upper()} KING IS IN CHECK!")
            else:
                print("Invalid move")
            
            # Reset selection
            self.selected_pos = None
            self.possible_moves = []
        else:
            # Select a piece
            piece = self.chess_board.board[row][col]
            if piece and piece.color == self.chess_board.current_player:
                self.selected_pos = clicked_pos
                self.possible_moves = piece.get_possible_moves(self.chess_board.board)
                print(f"Selected piece at {clicked_pos}")
                print(f"Possible moves: {self.possible_moves}")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                    elif event.button == 3:  # Right click
                        self.selected_pos = None
                        self.possible_moves = []
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:  # Undo move with 'U' key
                        if hasattr(self.chess_board, 'undo_move'):
                            self.chess_board.undo_move()
                            self.selected_pos = None
                            self.possible_moves = []

            # Draw everything
            self.screen.fill(WHITE)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()