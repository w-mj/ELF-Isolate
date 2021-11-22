#include <iostream>

using namespace std;
void externalFunc();

void someCommonFunc() {
	cout << "Call common func in library\n";
}

void interfaceFunc()  __attribute__((visibility("default")));

void interfaceFunc(){
	cout << "Call interface func\n";
	externalFunc();
	someCommonFunc();
	cout << "End call interface func\n";
}
