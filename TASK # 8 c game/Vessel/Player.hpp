#ifndef PLAYER_HPP
#define PLAYER_HPP


#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <string>

#include "Ship.hpp"
#include "Carrier.hpp"
#include "Battleship.hpp"
#include "Submarine.hpp"
#include "Patrolboat.hpp"
#include "Vessel.hpp"
#include "Board.hpp"

class Player
{
private:
    std::string name;
    std::vector<Ship*> ships;
    static constexpr int ROWS = 11;
    static constexpr int COLS = 11;
    char board[ROWS][COLS];
    char shootingBoard[ROWS][COLS];
    char targetBoard[ROWS][COLS];

    bool canPlaceShip(Ship* ship);
    void placeShip(Ship* ship);

public:
    Player();
    std::string getName();
    void setName(const std::string& name);
    std::vector<Ship*> getShips() const;
    void setShips(const std::vector<Ship*>& ships);
    char getBoard();
    char getShootingBoard();
    char getTargetBoard();
    void placeShips();
    void placeShipsRandomly();
    bool shoot(int x, int y);
    bool allSunk();
    void printShipsBoard();
    void printShootingBoard();
    void printTargetBoard();
    Player& operator=(const Player& other);
};

#endif