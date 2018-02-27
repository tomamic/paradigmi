#ifndef KNIGHTDOM_H
#define KNIGHTDOM_H

#include "boardgame.h"
#include <vector>

using namespace std;

class KnightDom : public BoardGame
{
public:
    bool finished();
    KnightDom(int side);
    void play_at(int x, int y);
    std::string get_val(int x, int y);
    int cols() { return side_; }
    int rows() { return side_; }
    std::string message() { return "Solved!"; }
private:
    vector<int> board_;
    int side_;
    int knights_;
};

#endif // KNIGHTDOM_H
