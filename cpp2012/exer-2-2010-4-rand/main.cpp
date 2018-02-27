/**
 * @author Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
 * @license This software is free - http://www.gnu.org/licenses/gpl.html
 */

#include <iostream>
#include <ctime>
#include <cstdlib>

using namespace std;

int main(int argc, char *argv[]) {
    const int MAX_VAL = 90, MAX_TRIES = 10;
    int secret, guess, tries = 0;

    srand(time(NULL));  // just once! initial seed for random numbers

    
    secret = (rand() % MAX_VAL) + 1;  // generate the secret number

    do {
        cout << "Guess the number (1-90): ";
        cin >> guess;

        ++tries;

        if (secret < guess) {
            cout << "The secret is smaller than " << guess << endl;
        } else if (secret > guess) {
            cout << "The secret is larger than " << guess << endl;
        } else {
            cout << "Congratulations, you guessed in " << tries << " tries" << endl;
        }
    } while (secret != guess && tries < MAX_TRIES);
}
