#include <iostream>
#include <chrono>
#include <thread>
#include <cstdlib>
#include <limits>

#include "Player.hpp"
#include "Game.hpp"

using namespace std;

void waitForSeconds(int seconds) //tempo de espera
{
    for (int i = seconds; i > 0; i--)
    {
        cout << i << "..." << endl;
        this_thread::sleep_for(chrono::seconds(1));
    }
}

void battle(Game& game) //função principal chamada em startNewGame(), que por sua vez é chamada no main
{
    Player& player1 = game.getPlayer(1);
    Player& player2 = game.getPlayer(2);
    bool gameOver = false;
    bool player1Turn = true; //vez do jogador 1

    while (!gameOver) //"enquanto o jogo acontecer"
    {
      if (player1Turn) //se vez do jogador 1
        {
            bool validInput = false;
            while (!validInput){
              player1.printShipsBoard();
              player2.printShootingBoard();
              cout << player1.getName() << ", it's your turn. Enter the coordinates (example: A3): ";
                    char row;
                    char column;
                    cin >> row >> column;
                    int x = row - 'A';
                    int y = column - '0';

                    try
                    {
                        if (cin.fail() || !isupper(row) || row < 'A' || row > 'J')
                        {
                            throw invalid_argument("Invalid coordinate. Please enter a capital letter between A and J.");
                        }
                        else if (!isdigit(column) || y < 0 || y > 9)
                        {
                            throw invalid_argument("Invalid coordinate. Please enter a number between 0 and 9.");
                        }
                        else
                        {
                            validInput = true;
                        }
                    }
                    catch (const invalid_argument& e)
                    {
                        cout << e.what() << endl;
                        cin.clear();
                        cin.ignore(numeric_limits<::streamsize>::max(), '\n');
                        continue;
                    }

                    player1Turn = player2.shoot(x, y) ? true : false;
                }
            }
            else
            {
                bool validInput = false;
                while (!validInput)
                {
                    player2.printShipsBoard();
                    player1.printShootingBoard();
                    cout << player2.getName() << ", it's your turn. Enter the coordinates (example: A3): ";
                    char row;
                    char column;
                    cin >> row >> column;
                    int x = row - 'A';
                    int y = column - '0';

                    try
                    {
                        if (cin.fail() || !isupper(row) || row < 'A' || row > 'J')
                        {
                            throw invalid_argument("Invalid coordinate. Please enter a capital letter between A and J.");
                        }
                        else if (!isdigit(column) || y < 0 || y > 9)
                        {
                            throw invalid_argument("Invalid coordinate. Please enter a number between 0 and 9.");
                        }
                        else
                        {
                            validInput = true;
                        }
                    }
                    catch (const invalid_argument& e)
                    {
                        cout << e.what() << endl;
                        cin.clear();
                        cin.ignore(numeric_limits<::streamsize>::max(), '\n');
                        continue;
                    }

                    player1Turn = player1.shoot(x, y) ? false : true;
                }
            }
        }

        if (player2.allSunk()) // se todos navios foram afundados
        {
            cout << endl;
            cout << "Sunk and destroyed! " << player1.getName() << " win!" << endl;
            player1.printShipsBoard();
            player2.printShootingBoard();
            cout << "Congratulations " << player1.getName() << ", you are the champion!" << endl;
            gameOver = true;
            cout << endl;
            cout << "GAME IS OVER." << endl;
        }
    
    }

void startNewGame()
{
    Game game;

    Player player1;
    cout << "Enter Player 1's name: ";
    string name1;
    cin >> name1;
    player1.setName(name1);


    player1.placeShips();

    cout << endl;
    cout << "Player 2, sbe ready to position your ships..." << endl;
    waitForSeconds(5);
  

    Player player2;
    cout << "Enter Player 2's name: ";
    string name2;
    cin >> name2;
    player2.setName(name2);

  
    player2.placeShips();

  
    game.setPlayer(player1, 1);
    game.setPlayer(player2, 2);

    cout << endl;
    cout << "Battle begins!" << endl;
    waitForSeconds(10);

    battle(game);
}

void displayMenu()
{
    cout << "Welcome to the game! Please select an option:" << endl;
    cout << "1. Novo jogo" << endl;
    cout << "2. Sair" << endl;
    cout << "Input your selection: ";
}

int main()
{
    bool validOp = false;
    int menuOption;
    while (!validOp)
    {
        try
        {
            displayMenu();
            cin >> menuOption;
            if (cin.fail())
            {
                throw std::invalid_argument("Input is not a number!");
            }
            if (menuOption < 1 || menuOption > 2)
            {
                throw std::invalid_argument("Choose an option between 1 and 2!");
            }
            validOp = true;
            switch (menuOption)
            {
                case 1:
                    cout << "Starting a new game..." << endl;
                    Game();
                    break;
                case 2:
                    cout << "Closing the program..." << endl;
                    return 0;
                default:
                    cout << "ERROR" << endl;
                    break;
            }
        }
        catch (const std::invalid_argument& e)
        {
            
            cout << e.what() << endl;
            cin.clear();
            cin.ignore(numeric_limits<::streamsize>::max(), '\n');
            continue;
        }
    }

    return 0;
}