#ifndef SHIP_HPP
#define SHIP_HPP

#include <iostream>
#include <string>

using namespace std;

class Ship
{
protected:
    string name;
    int size;
    char symbol;
    char orientation;
    int x, y;
    int hits;
    bool isSunk;

public:
    Ship();
    string getName();
    void setName(const string& name);
    int getSize();
    void setSize(int size);
    char getSymbol();
    void setSymbol(char symbol);
    char getOrientation();
    void setOrientation(char orientation);
    int getX();
    void setX(int x);
    int getY();
    void setY(int y);
    int getHits();
    void setHits(int hits);
    void hit();
    bool getIsSunk();
    void setIsSunk(bool sunk);

    friend istream& operator>>(istream& input, Ship& ship);
};

#endif // SHIP_HPP