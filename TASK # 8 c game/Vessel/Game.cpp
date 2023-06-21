#include "Game.hpp"

Game::Game()
{
}

void Game::setPlayer(const Player& player, int number)
{
    if (number == 1)
    {
        player1 = player;
    }
    else
    {
        player2 = player;
    }
}

Player& Game::getPlayer(int number)
{
    if (number == 1)
    {
        return player1;
    }
    else
    {
        return player2;
    }
}