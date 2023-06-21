## Battleship Game

The objective of the project is to develop a C++ game called "Battleship" in which two players take turns strategically placing their own fleet and trying to sink the opposing player's fleet through guessing the location of the opponent's ships on a 10x10 grid.



### 1. Rules
The game is played between two players. Each player has two grids: one to place their own ships and another to record the results of their shots. The columns are numbered (0-9) and the rows are labeled with capital letters (A-J). At the beginning of the game, each player must place their ships on their own grid. Each player has five ships:

- An aircraft carrier that occupies 5 spaces
- An battleship that occupies 4 spaces
- An submarine that occupies 3 spaces
- An patrol boat that occupies 2 spaces
- An ship that occupies 1 space

1. The ships must be placed horizontally or vertically and there must be a clear space around the ships.
2. The ships cannot touch each other.
3. Once the ships are placed, each player takes turns shooting at the opponent's grid by indicating the coordinates of the chosen space (e.g. "B3").
4. If the shot misses, the system will indicate "water."
5. If the shot hits a ship, the system will indicate "hit" and the player gets another turn.
6. If all spaces of a ship are hit, the ship is considered "sunk". If all of the opponent's ships are sunk, the game is over.