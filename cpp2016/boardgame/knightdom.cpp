#include "knightdom.h"

vector<int> knights = {0, 1, 4, 4, 4, 5, 8, 10, 12, 14, 16,
                       21, 24, 28, 32, 36, 40, 46, 52, 57, 62};

vector<vector<int>> moves = { {-1, -2}, {+1, -2}, {+2, -1}, {+2, +1},
                              {+1, +2}, {-1, +2}, {-2, +1}, {-2, -1} };

KnightDom::KnightDom(int side)
{
    side_ = max(1, min(side, 16));
    knights_ = knights[side];
    board_.assign(side * side, 0);
}

void KnightDom::play_at(int x, int y)
{
    if (0 <= x && x < side_ && 0 <= y && y < side_) {
        auto pos = y * side_ + x;
        auto val = +1;
        if (board_[pos] >= 10) val = -1;

        knights_ -= val;
        board_[pos] += val * 10;

        for (auto m : moves) {
            auto mx = x + m[0], my = y + m[1];
            if (0 <= mx && mx < side_ && 0 <= my && my < side_) {
                board_[my * side_ + mx] += val;
            }
        }
    }
}

string KnightDom::get_val(int x, int y)
{
    if (0 <= x && x < side_ && 0 <= y && y < side_) {
        auto pos = y * side_ + x;
//        return to_string(board_[pos]);
        if (board_[pos] >= 10) return "@";
        if (board_[pos] != 0) return "+";
    }
    return ".";
}

bool KnightDom::finished()
{
    if (knights_ != 0) return false;
    for (auto val : board_) {
        if (val == 0) return false;
    }
    return true;
}
