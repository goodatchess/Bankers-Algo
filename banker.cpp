#include <iostream>
#include <vector>
using namespace std;

bool isSafe(int n, int m, const vector<vector<int>>& alloc, const vector<vector<int>>& maxNeed, const vector<int>& avail) {
    vector<int> work = avail;
    vector<bool> finish(n, false);
    vector<int> safeSeq;

    while (safeSeq.size() < n) {
        bool found = false;
        for (int i = 0; i < n; ++i) {
            if (!finish[i]) {
                bool canRun = true;
                for (int j = 0; j < m; ++j) {
                    if (maxNeed[i][j] - alloc[i][j] > work[j]) {
                        canRun = false;
                        break;
                    }
                }
                if (canRun) {
                    for (int j = 0; j < m; ++j)
                        work[j] += alloc[i][j];
                    safeSeq.push_back(i);
                    finish[i] = true;
                    found = true;
                }
            }
        }
        if (!found) break;
    }

    if (safeSeq.size() == n) {
        cout << "System is in a SAFE state.\nSafe sequence: ";
        for (int p : safeSeq) cout << "P" << p << " ";
        cout << endl;
        return true;
    } else {
        cout << "System is in an UNSAFE state (deadlock possible).\n";
        return false;
    }
}

int main() {
    int n, m;
    cin >> n >> m;

    vector<vector<int>> alloc(n, vector<int>(m));
    vector<vector<int>> maxNeed(n, vector<int>(m));
    vector<int> avail(m);

    // Read allocation
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            cin >> alloc[i][j];

    // Read max need
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            cin >> maxNeed[i][j];

    // Read available
    for (int j = 0; j < m; ++j)
        cin >> avail[j];

    isSafe(n, m, alloc, maxNeed, avail);

    return 0;
}
