# Python Chess Game

A two-player chess game implemented in Python using Pygame. Features a graphical interface with move highlighting, check/checkmate detection, move history, and undo/redo functionality.
![image](https://github.com/user-attachments/assets/d1f9ae21-669d-4ae6-9ad6-73897aed638e)




## Features

- Complete chess rule implementation
- Graphical user interface with piece highlighting
- Legal move validation and suggestions
- Move history display
- Check and checkmate detection with alerts
- Undo/Redo system
- Simple and intuitive controls

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chess-game.git
cd chess-game
```

2. Install required packages:
```bash
pip install pygame
```

3. Run the game:
```bash
python chess_game.py
```

## How to Play

### Controls
- Left Click: Select piece and make moves
- Right Click: Deselect piece
- U: Undo move
- R: Redo move
- Close window to quit

### Game Rules
- Standard chess rules apply
- White moves first
- Available moves are highlighted in blue
- Checked king is highlighted in red
- Move history is displayed on the right
- Alert appears when king is in check or checkmate

## Project Structure

```
chess-game/
│
├── chess_game.py      # Main game file with GUI and game loop
├── chess_pieces.py    # Chess logic and piece movement rules
└── README.md         # Project documentation
```

## Code Structure

### chess_game.py
- Contains the game GUI implementation
- Handles user input and display
- Manages game state visualization

### chess_pieces.py
- Implements chess rules and logic
- Manages piece movement validation
- Handles game state (check, checkmate)

## Contributing

Feel free to fork the project and submit pull requests. Some areas for potential improvement:

- AI opponent implementation
- Network multiplayer support
- Game state saving/loading
- Opening book integration
- Performance optimizations
- Additional visual effects


## Future Improvements

- Add sound effects for moves and captures
- Implement an AI opponent
- Add online multiplayer capability
- Save/Load game functionality
- Custom theme support
- Move timer/clock



## Acknowledgments

- Thanks to Pygame for providing the graphics library
- Chess piece designs inspired by [source if applicable]
- [Any other acknowledgments]

## Author

[Your Name]
- GitHub: [@yourusername](https://github.com/yourusername)
- [Other contact information if desired]

## Version History

- v1.0.0 (2024-02-27)
  - Initial release
  - Basic chess functionality
  - GUI implementation
  - Move validation
  - Check/Checkmate detection
  - Undo/Redo system
