#ifndef GAME_HPP
#define GAME_HPP

#include "Player.hpp"
#include <fstream>

class Game
{
private:
    Player player1;
    Player player2;

public:
    Game();
    void setPlayer(const Player& player, int number);
    Player& getPlayer(int number);
};

#endif