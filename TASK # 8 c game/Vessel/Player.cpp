#include "Player.hpp"

bool Player::canPlaceShip(Ship* ship)
{
    if (ship->getOrientation() == 'H')
    {
        if (ship->getY() + ship->getSize() > COLS)
        {
            return false;
        }
        for (int i = ship->getY() - 1; i <= ship->getY() + ship->getSize(); i++)
        {
            for (int j = ship->getX() - 1; j <= ship->getX() + 1; j++)
            {
                if (i >= 0 && i < COLS && j >= 0 && j < ROWS && board[j][i] != '.')
                {
                    return false;
                }
            }
        }
    }
    else
    {
        if (ship->getX() + ship->getSize() > ROWS)
        {
            return false;
        }
        for (int i = ship->getX() - 1; i <= ship->getX() + ship->getSize(); i++)
        {
            for (int j = ship->getY() - 1; j <= ship->getY() + 1; j++)
            {
                if (i >= 0 && i < ROWS && j >= 0 && j < COLS && board[i][j] != '.')
                {
                    return false;
                }
            }
        }
    }
    return true;
}

void Player::placeShip(Ship* ship)
{
    if (ship->getOrientation() == 'H')
    {
        for (int i = ship->getY(); i < ship->getY() + ship->getSize(); i++)
        {
            board[ship->getX()][i] = ship->getSymbol();
        }
    }
    else
    {
        for (int i = ship->getX(); i < ship->getX() + ship->getSize(); i++)
        {
            board[i][ship->getY()] = ship->getSymbol();
        }
    }
}

Player::Player()
{
    name = "DefaultPlayerName";
    ships.push_back(new Carrier());
    ships.push_back(new Battleship());
    ships.push_back(new Submarine());
    ships.push_back(new PatrolBoat());
    ships.push_back(new Vessel());

    for (int i = 0; i < ROWS; i++)
    {
        for (int j = 0; j < COLS; j++)
        {
            board[i][j] = '~';
        }
    }
}

std::string Player::getName()
{
    return name;
}

void Player::setName(const std::string& name)
{
    this->name = name;
}

std::vector<Ship*> Player::getShips() const
{
    return ships;
}

void Player::setShips(const std::vector<Ship*>& ships)
{
    this->ships = ships;
}

char Player::getBoard() {
    return board[ROWS][COLS];
  }

char Player::getShootingBoard() {
    return shootingBoard[ROWS][COLS];
  }

char Player::getTargetBoard() {
    return targetBoard[ROWS][COLS];
  }

void Player::placeShips()
{
    for (Ship* ship : ships)
    {
        std::cout << "Placing " << ship->getName() << " (" << ship->getSize() << " units)" << std::endl;

        int x, y;
        char orientation;

        std::cout << "Enter the starting coordinates (x, y): ";
        std::cin >> x >> y;
        ship->setX(x);
        ship->setY(y);

        std::cout << "Enter the orientation (H for horizontal, V for vertical): ";
        std::cin >> orientation;
        ship->setOrientation(orientation);

        if (canPlaceShip(ship))
        {
            placeShip(ship);
            std::cout << "Ship placed successfully!" << std::endl;
            printShipsBoard();
        }
        else
        {
            std::cout << "Invalid placement. Please try again." << std::endl;
            --ship; // Retry placing the same ship
        }
    }
}

void Player::placeShipsRandomly()
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> disX(0, ROWS - 1);
    std::uniform_int_distribution<int> disY(0, COLS - 1);
    std::uniform_int_distribution<int> disOrientation(0, 1);

    for (Ship* ship : ships)
    {
        bool placed = false;
        while (!placed)
        {
            int x = disX(gen);
            int y = disY(gen);
            char orientation = disOrientation(gen) == 0 ? 'H' : 'V';

            ship->setX(x);
            ship->setY(y);
            ship->setOrientation(orientation);

            if (canPlaceShip(ship))
            {
                placeShip(ship);
                placed = true;
            }
        }
    }
}

bool Player::shoot(int x, int y)
{
    char target = shootingBoard[x][y];
    if (target == '~') {
        shootingBoard[x][y] = 'O';  // Marca como água (O) no tabuleiro de tiros
        return false;  // Indica que o disparo foi em água
    } else if (target != '~') {
        shootingBoard[x][y] = 'X';  // Marca como atingido (X) no tabuleiro de tiros
        for (Ship* ship : ships) {
            if (ship->hit(x, y)) {
                if (ship->getIsSunk()) {
                    std::cout << "You sunk the " << ship->getName() << "!" << std::endl;
                    if (allSunk()) {
                        std::cout << "Congratulations! You have sunk all the ships. You win!" << std::endl;
                    }
                }
                return true;  // Indica que o disparo atingiu um navio
            }
        }
    }
    return false;  // Caso ocorra algum erro ou a posição já tenha sido atingida antes
}



bool Player::allSunk(){
    for (Ship* ship : ships)
    {
        if (!ship->getIsSunk()){
        {
            return false;
        }
    }
    return true;
    }
}

void Player::printShipsBoard(){
    std::cout << "Ships Board: " << std::endl;
    for (int i = 0; i < ROWS; ++i)
    {
        for (int j = 0; j < COLS; ++j)
        {
            std::cout << board[i][j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void Player::printTargetBoard(){
    std::cout << "Target Board: " << std::endl;
    for (int i = 0; i < ROWS; ++i)
    {
        for (int j = 0; j < COLS; ++j)
        {
            std::cout << targetBoard[i][j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}