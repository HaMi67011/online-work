#include <iostream>
using namespace std;
#include "Q2.cpp"

int main(){

	int N = 7;
	double x[7] = {10,30,15,21,17,14,13};
	double y[7] = {17,31,22,35,24,47,15};
	double power[7] = {0.000001,0.000001 ,0.000001 ,0.000001 ,0.000001 ,0.000001 ,0.000001 };

	AnalyzeSmartFarm(N, x, y, power);    
    return 0;
}
