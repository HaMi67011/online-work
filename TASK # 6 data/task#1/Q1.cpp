#include <iostream>
#include <vector>
#include <algorithm>
#include <math.h>
#include<iomanip>

using namespace std;
#define M_PI           3.14159265358979323846 

//do not change this function
double toRadians(const double& degree)
{
    double one_deg = (M_PI) / 180;
    return (one_deg * degree);
}

//do not change this function
double ComputeDistance(double lat1, double long1,
    double lat2, double long2)
{
    lat1 = toRadians(lat1);
    long1 = toRadians(long1);
    lat2 = toRadians(lat2);
    long2 = toRadians(long2);

    double dlong = long2 - long1;
    double dlat = lat2 - lat1;

    double ans = pow(sin(dlat / 2), 2) +
        cos(lat1) * cos(lat2) *
        pow(sin(dlong / 2), 2);
    ans = 2 * asin(sqrt(ans));
    double R = 6371;
    ans = ans * R;

    return ans;
}

struct Edge {
    int src, dest;
    double weight;
};

// Find operation for disjoint set
int find(vector<int>& parent, int i) {
    if (parent[i] == -1)
        return i;
    return find(parent, parent[i]);
}

// Union operation for disjoint set
void unionOp(vector<int>& parent, int x, int y) {
    int xset = find(parent, x);
    int yset = find(parent, y);
    parent[xset] = yset;
}

// Comparator function for sorting edges based on weight
bool compareEdges(const Edge& a, const Edge& b) {
    return a.weight < b.weight;
}

double GetMinCost(int N, double latitude[], double longitude[]) {
    vector<Edge> edges;
    
    // Generate all possible edges between cities
    for (int i = 0; i < N - 1; ++i) {
        for (int j = i + 1; j < N; ++j) {
            double lat1 = latitude[i];
            double lon1 = longitude[i];
            double lat2 = latitude[j];
            double lon2 = longitude[j];
            double distance = ComputeDistance(lat1, lon1, lat2, lon2);
            
            Edge edge;
            edge.src = i;
            edge.dest = j;
            edge.weight = distance;
            
            edges.push_back(edge);
        }
    }
    
    // Sort edges based on weight in ascending order
    sort(edges.begin(), edges.end(), compareEdges);
    
    vector<int> parent(N, -1);
    double min_cost = 0.0;
    
    for (const Edge& edge : edges) {
        int srcParent = find(parent, edge.src);
        int destParent = find(parent, edge.dest);
        
        // Check if including the current edge forms a cycle
        // If not, include it in the MST and update the cost
        if (srcParent != destParent) {
            unionOp(parent, srcParent, destParent);
            min_cost += edge.weight;
        }
    }
    
    return min_cost;
}
