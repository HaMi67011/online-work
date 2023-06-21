#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

using namespace std;

// Constants
const int BOARD_SIZE = 10;
const int SHIP_SIZE = 3;
const int NUM_SHIPS = 3;
const char EMPTY_CELL = '-';
const char SHIP_CELL = 'S';
const char HIT_CELL = 'X';
const char MISS_CELL = 'O';

// Ship class
class Ship {
public:
    Ship(int x, int y, bool horizontal);

    int getX() const { return x; }
    int getY() const { return y; }
    bool isHorizontal() const { return horizontal; }
    bool isSunk() const { return hits == SHIP_SIZE; }

    bool checkCollision(const Ship& other) const;
    bool hit(int x, int y);
    
private:
    int x;
    int y;
    bool horizontal;
    int hits;
    vector<char> cells;
};

Ship::Ship(int x, int y, bool horizontal)
    : x(x), y(y), horizontal(horizontal), hits(0) {
        cells.resize(SHIP_SIZE, SHIP_CELL);
    }

bool Ship::checkCollision(const Ship& other) const {
    if (horizontal && other.horizontal) {
        if (y != other.y)
            return false;
        int start = max(x - 1, 0);
        int end = min(x + SHIP_SIZE, BOARD_SIZE);
        int otherStart = max(other.x - 1, 0);
        int otherEnd = min(other.x + SHIP_SIZE, BOARD_SIZE);
        return (start < otherEnd) && (end > otherStart);
    } else if (!horizontal && !other.horizontal) {
        if (x != other.x)
            return false;
        int start = max(y - 1, 0);
        int end = min(y + SHIP_SIZE, BOARD_SIZE);
        int otherStart = max(other.y - 1, 0);
        int otherEnd = min(other.y + SHIP_SIZE, BOARD_SIZE);
        return (start < otherEnd) && (end > otherStart);
    } else {
        if (horizontal) {
            int start = max(x - 1, 0);
            int end = min(x + SHIP_SIZE, BOARD_SIZE);
            return (y >= other.y - 1 && y < other.y + 1) && (start < other.x + 1) && (end > other.x);
        } else {
            int start = max(y - 1, 0);
            int end = min(y + SHIP_SIZE, BOARD_SIZE);
            return (x >= other.x - 1 && x < other.x + 1) && (start < other.y + 1) && (end > other.y);
        }
    }
}

bool Ship::hit(int x, int y) {
    if ((horizontal && (y < this->y || y >= this->y + SHIP_SIZE)) ||
        (!horizontal && (x < this->x || x >= this->x + SHIP_SIZE)))
        return false;

    int index = horizontal ? (x - this->x) : (y - this->y);
    if (index < 0 || index >= SHIP_SIZE)
        return false;

    if (cells[index] == SHIP_CELL) {
        cells[index] = HIT_CELL;
        hits++;
        return true;
    } else {
        return false;
    }
}

// Board class
class Board {
public:
    Board();

    void print(bool showShips) const;
    bool placeShip(const Ship& ship);
    bool shoot(int x, int y);

private:
    char grid[BOARD_SIZE][BOARD_SIZE];
};

Board::Board() {
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            grid[i][j] = EMPTY_CELL;
        }
    }
}

void Board::print(bool showShips) const {
    cout << "   ";
    for (int i = 0; i < BOARD_SIZE; i++) {
        cout << static_cast<char>('A' + i) << " ";
    }
    cout << endl;

    for (int i = 0; i < BOARD_SIZE; i++) {
        cout << " " << i << " ";
        for (int j = 0; j < BOARD_SIZE; j++) {
            if (showShips || grid[i][j] != SHIP_CELL)
                cout << grid[i][j] << " ";
            else
                cout << EMPTY_CELL << " ";
        }
        cout << endl;
    }
}

bool Board::placeShip(const Ship& ship) {
    if (ship.isHorizontal()) {
        if (ship.getX() < 0 || ship.getX() + SHIP_SIZE > BOARD_SIZE || ship.getY() < 0 || ship.getY() >= BOARD_SIZE)
            return false;

        for (int i = ship.getX(); i < ship.getX() + SHIP_SIZE; i++) {
            if (grid[ship.getY()][i] != EMPTY_CELL)
                return false;
        }

        for (int i = ship.getX(); i < ship.getX() + SHIP_SIZE; i++) {
            grid[ship.getY()][i] = SHIP_CELL;
        }
    } else {
        if (ship.getX() < 0 || ship.getX() >= BOARD_SIZE || ship.getY() < 0 || ship.getY() + SHIP_SIZE > BOARD_SIZE)
            return false;

        for (int i = ship.getY(); i < ship.getY() + SHIP_SIZE; i++) {
            if (grid[i][ship.getX()] != EMPTY_CELL)
                return false;
        }

        for (int i = ship.getY(); i < ship.getY() + SHIP_SIZE; i++) {
            grid[i][ship.getX()] = SHIP_CELL;
        }
    }

    return true;
}

bool Board::shoot(int x, int y) {
    if (x < 0 || x >= BOARD_SIZE || y < 0 || y >= BOARD_SIZE)
        return false;

    if (grid[y][x] == SHIP_CELL) {
        grid[y][x] = HIT_CELL;
        return true;
    } else if (grid[y][x] == EMPTY_CELL) {
        grid[y][x] = MISS_CELL;
    }

    return false;
}

// Game class
class Game {
public:
    Game();

    void play();

private:
    Board playerBoard;
    Board computerBoard;
    vector<Ship> playerShips;
    vector<Ship> computerShips;

    void printBoards() const;
    void placePlayerShips();
    void placeComputerShips();
    void playerTurn();
    void computerTurn();
    bool checkGameOver() const;
};

Game::Game() {
    srand(static_cast<unsigned>(time(nullptr)));
}

void Game::play() {
    cout << "Welcome to Battleship!" << endl;
    cout << "You need to sink all " << NUM_SHIPS << " ships of the computer to win." << endl;

    placePlayerShips();
    placeComputerShips();

    while (!checkGameOver()) {
        printBoards();
        playerTurn();

        if (checkGameOver())
            break;

        computerTurn();
    }

    printBoards();
    cout << "Game Over!" << endl;
    cout << (playerShips.empty() ? "You lost." : "Congratulations! You won!") << endl;
}

void Game::printBoards() const {
    cout << "Your Board:" << endl;
    playerBoard.print(true);

    cout << endl;

    cout << "Computer's Board:" << endl;
    computerBoard.print(false);
}

void Game::placePlayerShips() {
    cout << "Place your ships:" << endl;

    for (int i = 0; i < NUM_SHIPS; i++) {
        int x, y;
        bool horizontal;

        cout << "Enter coordinates for Ship #" << i + 1 << ": ";
        cin >> x >> y;

        cout << "Enter orientation (0 for horizontal, 1 for vertical): ";
        cin >> horizontal;

        Ship ship(x, y, horizontal);

        if (!playerBoard.placeShip(ship)) {
            cout << "Invalid ship placement. Try again." << endl;
            i--;
            continue;
        }

        playerShips.push_back(ship);
        cout << "Ship placed successfully!" << endl;
    }
}

void Game::placeComputerShips() {
    cout << "Computer is placing ships..." << endl;

    for (int i = 0; i < NUM_SHIPS; i++) {
        int x, y;
        bool horizontal;
        Ship ship(x, y, horizontal);  // Declare the ship variable here

        do {
            x = rand() % BOARD_SIZE;
            y = rand() % BOARD_SIZE;
            horizontal = rand() % 2;
        } while (!computerBoard.placeShip(ship));

        computerShips.push_back(ship);
    }

    cout << "Computer placed ships successfully!" << endl;
}

void Game::playerTurn() {
    int x, y;

    cout << "Your Turn!" << endl;
    cout << "Enter coordinates to shoot: ";
    cin >> x >> y;

    if (computerBoard.shoot(x, y)) {
        cout << "Hit!" << endl;
        for (int i = 0; i < computerShips.size(); i++) {
            if (computerShips[i].hit(x, y)) {
                if (computerShips[i].isSunk()) {
                    cout << "You sank the computer's ship!" << endl;
                    computerShips.erase(computerShips.begin() + i);
                    break;
                }
            }
        }
    } else {
        cout << "Miss!" << endl;
    }

    printBoards(); // Display the boards after each turn
}

void Game::computerTurn() {
    int x, y;

    cout << "Computer's Turn!" << endl;
    do {
        x = rand() % BOARD_SIZE;
        y = rand() % BOARD_SIZE;
    } while (!playerBoard.shoot(x, y));

    cout << "Computer shot at " << static_cast<char>('A' + x) << y << endl;

    if (playerBoard.shoot(x, y)) {
        cout << "The computer hit your ship!" << endl;
        for (int i = 0; i < playerShips.size(); i++) {
            if (playerShips[i].hit(x, y)) {
                if (playerShips[i].isSunk()) {
                    cout << "The computer sank your ship!" << endl;
                    playerShips.erase(playerShips.begin() + i);
                    break;
                }
            }
        }
    } else {
        cout << "The computer missed!" << endl;
    }

    printBoards(); // Display the boards after each turn
}



bool Game::checkGameOver() const {
    return playerShips.empty() || computerShips.empty();
}

// Main function
int main() {
    Game game;
    game.play();

    return 0;
}

