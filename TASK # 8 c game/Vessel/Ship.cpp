#include "Ship.hpp"

Ship::Ship()
{
    name = "Ship";
    size = 0;
    symbol = 'S';
    orientation = 'V';
    x = 0;
    y = 0;
    hits = 0;
    isSunk = false;
}

string Ship::getName()
{
    return name;
}

void Ship::setName(const string& name)
{
    this->name = name;
}

int Ship::getSize()
{
    return size;
}

void Ship::setSize(int size)
{
    this->size = size;
}

char Ship::getSymbol()
{
    return symbol;
}

void Ship::setSymbol(char symbol)
{
    this->symbol = symbol;
}

char Ship::getOrientation()
{
    return orientation;
}

void Ship::setOrientation(char orientation)
{
    this->orientation = orientation;
}

int Ship::getX()
{
    return x;
}

void Ship::setX(int x)
{
    this->x = x;
}

int Ship::getY()
{
    return y;
}

void Ship::setY(int y)
{
    this->y = y;
}

int Ship::getHits()
{
    return hits;
}

void Ship::setHits(int hits)
{
    this->hits = hits;
}

void Ship::hit()
{
    ++hits;
}

bool Ship::getIsSunk()
{
    return isSunk;
}

void Ship::setIsSunk(bool sunk)
{
    this->isSunk = sunk;
}

istream& operator>>(istream& input, Ship& ship)
{
    cout << "Enter the " << ship.name << " coordinates (x y) and orientation (h/v): ";
    input >> ship.x >> ship.y >> ship.orientation;
    return input;
}
