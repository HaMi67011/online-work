#include <iostream>
using namespace std;
#include "Q1.cpp"
#include<iomanip>

int main(){

	int N=5;

	double latitudes[]={40.6943,34.1141,41.8375,25.784,32.7935};
	double longitudes[]={-73.9249,-118.4068,-87.6866,-80.2101,-96.7667};

    cout << fixed << std::setprecision(2);
	cout<<GetMinCost (N,latitudes,longitudes);
    // result should be 6207.15
	return 0;
}
