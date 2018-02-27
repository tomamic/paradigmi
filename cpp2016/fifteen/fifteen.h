/**
 * @author Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
 * @license This software is free - http://www.gnu.org/licenses/gpl.html
 */

#ifndef FIFTEEN_H
#define FIFTEEN_H

#include <iostream>
#include <vector>
#include <complex>

using namespace std;

typedef complex<int> Coord;

class Fifteen
{
public:
    Fifteen(int cols, int rows);
    void init(int cols, int rows);
    void new_game();
    void move_val(int value);
    int get(int x, int y);
    Coord blank() { return blank_; }
    Coord moved() { return moved_; }
    void write(ostream &out);
    string str();

    void play_at(int x, int y);
    std::string get_val(int x, int y);
    bool finished();
    std::string message() { return "Puzzle solved!"; }
    int cols() { return cols_; }
    int rows() { return rows_; }
private:
    void swap_blank_with(int x, int y);

    int cols_;
    int rows_;

    vector<int> board_;
    Coord blank_;  // where's the blank?
    Coord moved_;  // which cell has been moved?

    // DIRS is a vector of couples: (dx, dy)
    const vector<Coord> DIRS = { {0, -1}, {-1, 0}, {0, 1}, {1, 0} };
};

#endif // FIFTEEN_H
