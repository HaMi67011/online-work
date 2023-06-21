#include <iostream>
#include <vector>
#include <queue>

void AnalyzeTheVirus(int N, int C, int I, int source[], int dest[], int infected_computers[]) {
    std::vector<std::vector<int>> adj_list(N);  // Adjacency list to represent connections
    
    // Build the adjacency list
    for (int i = 0; i < C; i++) {
        adj_list[source[i]].push_back(dest[i]);
        adj_list[dest[i]].push_back(source[i]);
    }
    
    std::queue<int> q;
    std::vector<bool> visited(N, false);
    int start_computer = infected_computers[0];  // Assuming the first infected computer started the attack
    
    // Mark the already infected computers as visited and enqueue them
    for (int i = 0; i < I; i++) {
        visited[infected_computers[i]] = true;
        q.push(infected_computers[i]);
    }
    
    // Perform BFS to simulate virus spread
    int total_infected = I;  // Count the already infected computers
    while (!q.empty()) {
        int current = q.front();
        q.pop();
        
        for (int neighbor : adj_list[current]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
                total_infected++;
            }
        }
    }
    
    // Print the results
    std::cout << "The computer that started the attack: " << start_computer << std::endl;
    std::cout << "The total number of computers that will be infected in 40 minutes: " << total_infected << std::endl;
}
