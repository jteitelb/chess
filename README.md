## Chess

a chess game, just for fun  
### Todo
- Refactor / Design Classes (currently a bit spaghetti / badly coupled)
  - decouple UI from logic (will make testing easier)
- UI
  - click to highlight square
  - moving pieces by click
- unit tests
  - Module functions
  - Square methods
    - is_valid
    - peek
  - Piece methods
    - move
    - probe_line/probe_multis
    - get_pawn_moves