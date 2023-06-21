#include <iostream>
using namespace std;
#include "Q3.cpp"

int main(){
    int N=20;
    int C=22;
    int I=5;



    int sources[22]={0,0 ,0 ,0 ,1 ,2 ,2 ,3 ,4 ,4 ,5 ,8  ,13,14,3 ,12,2 ,11 ,6 ,10,17,18};
    int dests[22]={1,2,3,4,5,6,7,7,8,9,9,13 ,14,16,12,15,11,19,10,17,18,19};

    
    int infected_computers[5]={0,1,2,3,4};
    
    AnalyzeTheVirus(N, C, I,  sources,  dests, infected_computers);
    // should output 0 16
    return 0;
}
