#include <iostream>
#include<sstream>
#include<vector>
#include<queue>
using namespace std;

vector<vector<int> > graph;

bool bfs(int start, int end, int size, int pre[]){
    int visit[size];
    int distance[size];
    string circle[size];
    for (int i = 0;i<size;i++)
        visit[i] = 0;

    if (start == end){
        circle[start] = to_string(start);
    }

    queue<int> q;
    q.push(start);
    visit[start] = 1;
    distance[start] = 0;

    while(!q.empty()){
        int f = q.front();
        q.pop();
        for(int cur : graph[f]){
            if (visit[cur] == 1 && start != end)
                continue;

            if (visit[cur] == 1 && start == end && pre[f] == cur)
                continue;

            if (visit[cur] == 1 && start == end && pre[f]!=cur){
                string ans = circle[cur] + '-' + to_string(f);
                int back = f;
                while (back != start){
                    back = pre[f];
                    ans += '-' + to_string(back);
                }
                cout << ans << endl;
                return true;
            }

            visit[cur] = 1;
            distance[cur] = distance[f] + 1;
            pre[cur] = f;

            if (start == end){
                circle[cur] = circle[f] + '-' + to_string(cur);
            }
            else
            if (cur == end)
                return true;
            q.push(cur);
        }
    }
    return false;
}

void get_edges(string coordinate, int size){
    string x,y;
    for (int i=0;i<coordinate.size();i++){
        if (coordinate[i] == '<'){
            x.push_back(coordinate[i+1]);
            if (coordinate[i+2] != ','){
                x.push_back(coordinate[i+2]);
                if (coordinate[i+3] != ',')
                    x.push_back(coordinate[i+3]);
            }
            x.push_back(' ');
        }

        if (coordinate[i] == ',' && coordinate[i+1] != '<'){
            y.push_back(coordinate[i+1]);
            if (coordinate[i+2] != '>'){
                y.push_back(coordinate[i+2]);
                if (coordinate[i+3] != '>')
                    y.push_back(coordinate[i+3]);
            }
            y.push_back(' ');
        }
    }

    stringstream x_value(x);
    stringstream y_value(y);
    int x_int;
    int y_int;
    while(x_value >> x_int && y_value >> y_int) {
        if (x_int > size - 1 || y_int > size - 1)
            cout << "Error: vertex does not exist!" << endl;
        graph[x_int].push_back(y_int);
        graph[y_int].push_back(x_int);
    }
}

void print(int end, int pre[]){
    vector<int> path;
    int last = end;
    path.push_back(last);
    while(pre[last] != -1){
        path.push_back(pre[last]);
        last = pre[last];
    }
    for (int i = path.size()-1;i>=0;i--){
        if (i==0)
            cout << path[i] << endl;
        else
            cout << path[i] << '-';
    }
}

int main() {
    string input;
    string initial;
    int size;

    while (true){
        getline(cin, input);
        if (cin.eof())
            break;

        istringstream split(input);
        split >> initial;

        if (initial == "V") {
            split >> size;
            cout << "V " << size << endl;
            graph = *new vector<vector<int> >;
            graph.resize(size);
        }

        if (initial == "E") {
            string coordinate;
            split >> coordinate;
            cout << "E " << coordinate << endl;
            get_edges(coordinate, size);
        }

        if (initial == "s") {
            int start;
            int end;
            int pre[size];
            for (int i = 0;i<size;i++)
                pre[i] = -1;
            split >> start;
            split >> end;

            if(start > size-1 || end > size-1)
                cout << "Error: vertex does not exist!"<< endl;
            else{
                if (bfs(start, end, size, pre)){
                    if (start != end)
                        print(end, pre);
                }
                else
                    cout << "Error: the shortest path between these two vertexes does not exist!" << endl;
            }
        }
    }
}
