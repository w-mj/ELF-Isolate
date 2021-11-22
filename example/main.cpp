#include <iostream>

using namespace std;

void externalFunc();
void interfaceFunc();

void someCommonFunc() {
    cout << "Call comm func in main\n";
}

int main() {
    externalFunc();
    interfaceFunc();
    someCommonFunc();
}