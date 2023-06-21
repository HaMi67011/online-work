/*****************************************************************//**
 * \file   Board.hpp
 * \brief  
 * 
 * \author pablo
 * \date   January 2023
 *********************************************************************/
#ifndef BOARD_HPP
#define BOARD_HPP

#include <iostream>
#include "Ship.hpp"

class Board
{
private:
    char board[11][11];
    void fillBoard();

public:
    Board();
    char** getBoard();
    void displayBoard();
    bool isValidPlacement(Ship ship, int x, int y);
    bool isOccupied(int x, int y) const;
};

#endif // BOARD_HPP
