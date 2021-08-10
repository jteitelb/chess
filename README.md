## Chess

a chess game, just for fun  
### Todo
- Refactor / Design Classes (currently a bit spaghetti / badly coupled)
  - decouple UI from logic (will make testing easier)
  - constants
  - handle coords/square names in Square class? (not UI related), and create SquareSprite class?
- UI
  - click to highlight square
  - moving pieces by click
- unit tests
  - Module functions
    - valid_coord
    - peek
  - Piece methods
    - move
    - probe_line/probe_multis
    - get_pawn_moves