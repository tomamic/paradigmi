#ifndef KNIGHTDOM_H
#define KNIGHTDOM_H

#include "game.h"
#include <vector>

using namespace std;

class Queens : public Game
{
public:
    bool finished();
    Queens(int side);
    void play_at(int x, int y);
    std::string get_val(int x, int y);
    int cols() { return side_; }
    int rows() { return side_; }
    std::string message() { return "Solved!"; }
private:
    vector<vector<int>> board_;
    vector<vector<int>> cover_;
    int side_;
    int queens_;
};

#endif // KNIGHTDOM_H
