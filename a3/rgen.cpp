#include <iostream>
#include <fstream>
#include <vector>
#include <unistd.h>

using namespace std;

vector< string > names;
vector< pair<int,int> > all_points;

int urandom() {
    int random_value;
    std::ifstream urandom("/dev/urandom");
    urandom.read(reinterpret_cast<char*>(&random_value), 4);
    urandom.close();
    return random_value;
}

int random_int(int min, int max) {
    int range = max-min;
    int i = urandom();
    int result = (i % (range+1) + (range+1) ) % (range+1) + min;
    return result;
}

float get_a (pair<int, int> p1, pair<int, int> p2){
    float x_diff;
    float y_diff;
    x_diff = p1.first - p2.first;
    y_diff = p1.second - p2.second;
    float a;
    a = y_diff / x_diff;
    return a;
}

float get_b (pair<int, int> p1, pair<int, int> p2){
    float b;
    b = p1.second - get_a(p1, p2)*p1.first;
    return b;
}

int x_min (pair<int, int> p1, pair<int, int> p2, pair<int, int> p3, pair<int, int> p4){
    int x1_left = min(p1.first, p2.first);
    int x2_left = min(p3.first, p4.first);
    int x_min = max(x1_left, x2_left);
    return x_min;
}

int x_max (pair<int, int> p1, pair<int, int> p2, pair<int, int> p3, pair<int, int> p4){
    int x1_right = max(p1.first, p2.first);
    int x2_right = max(p3.first, p4.first);
    int x_max = min(x1_right, x2_right);
    return  x_max;
}

int y_min (pair<int, int> p1, pair<int, int> p2, pair<int, int> p3, pair<int, int> p4){
    int y1_down = min(p1.second, p2.second);
    int y2_down = min(p3.second, p4.second);
    int y_min = max(y1_down, y2_down);
    return y_min;
}

int y_max (pair<int, int> p1, pair<int, int> p2, pair<int, int> p3, pair<int, int> p4){
    int y1_up = max(p1.second, p2.second);
    int y2_up = max(p3.second, p4.second);
    int y_max = min(y1_up, y2_up);
    return  y_max;
}

bool overlap(pair<int, int> p1, pair<int, int> p2, pair<int, int> p3, pair<int, int> p4){
    float a1 = get_a(p1, p2);
    float a2 = get_a(p3, p4);
    float b1 = get_b(p1, p2);
    float b2 = get_b(p3, p4);
    int min_x = x_min(p1, p2, p3, p4);
    int max_x = x_max(p1, p2, p3, p4);
    int min_y = y_min(p1, p2, p3, p4);
    int max_y = y_max(p1, p2, p3, p4);

    if(p1.first == p2.first && p2.first == p3.first && p3.first == p4.first){
        if(
                (p1.second <= max_x && p1.second >=min_x) ||
                (p2.second <= max_x && p2.second >=min_x) ||
                (p3.second <= max_x && p2.second >=min_x) ||
                (p4.second <= max_x && p2.second >=min_x))
            return true;
    }

    else{
        if (a1 == a2 && b1 == b2){
            if(
                    (p1.first <= max_y && p1.first >=min_y) ||
                    (p2.first <= max_y && p2.first >=min_y) ||
                    (p3.first <= max_y && p2.first >=min_y) ||
                    (p4.first <= max_y && p2.first >=min_y))
                return true;
        }
    }
    return false;
}

bool intersect(pair<int, int> p1, pair<int, int> p2, pair<int, int> p3, pair<int, int> p4){
    float a1 = get_a(p1, p2);
    float a2 = get_a(p3, p4);
    float b1 = get_b(p1, p2);
    float b2 = get_b(p3, p4);
    int min_x = x_min(p1, p2, p3, p4);
    int max_x = x_max(p1, p2, p3, p4);
    int min_y = y_min(p1, p2, p3, p4);
    int max_y = y_max(p1, p2, p3, p4);

    float intersect_x, intersect_y;
    if(p1.first == p2.first){
        intersect_x = p1.first;
        intersect_y = intersect_x * a2 + b2;
    }
    else if(p3.first == p4.first){
        intersect_x = p3.first;
        intersect_y = intersect_x * a1 + b1;
    }
    else{
        intersect_x = (b2 - b1)/(a1 - a2);
        intersect_y = a1 * intersect_x + b1;
    }

    if((intersect_x <= max_x && intersect_x >= min_x && intersect_y <= max_y && intersect_y >= min_y) )
        return true;

    return false;
}


bool valid(vector<pair<int,int> > street){
    for(int i =0;i<street.size();i++)
        for(int j=i+1;j<street.size();j++)
            if((street[i].first == street[j].first) && (street[i].second == street[j].second))
                return false;

    for(int i =0;i<street.size() - 1;i++)
        for(int j=i+1;j<street.size() - 1;j++)
            if(overlap(street[i], street[i+1], street[j], street[j+1]))
                return false;

    for(int i =0;i<street.size() - 1;i++)
        for(int j=i+2;j<street.size() - 1;j++)
            if(intersect(street[i], street[i+1], street[j], street[j+1]))
                return false;

    if(!all_points.empty())
        for(int i=0;i<street.size()-1;i++)
            for(int j=0;j<all_points.size()-1;j++)
                if(overlap(street[i], street[i+1], all_points[j],all_points[j+1]))
                    return false;
    return true;
}

vector< pair<int,int> > g_segments(int n, int c) {
    vector< pair<int,int> > street;
    int n_segments = random_int(2, n+1);
    int loop = 0;
    do{
        street.clear();
        for(int i = 0; i < n_segments; i++ ) {
            pair<int, int> point;
            point.first = random_int(-c, c);
            point.second = random_int(-c, c);
            street.push_back(point);
        }
        loop += 1;
        if (loop > 25){
            cerr <<"Error: failed to generate valid input for 25 simultaneous attempts";
            exit(0);
        }
    } while(!valid(street));
    for(auto & s_s : street)
        all_points.push_back(s_s);
    return street;
}

void g_street(int s, int n, int c) {
    names.clear();
    all_points.clear();
    vector< vector< pair<int,int> > > points;
    int n_streets = random_int(2, s);
    for(int i=0; i < n_streets; i++) {
        char letter = 'a' + i;
        string word = "street ";
        word += letter;
        names.push_back(word);
        points.push_back(g_segments(n, c));
    }

    for (int i=0; i < names.size(); i++){
        cout << "a " << '"' << names[i] << '"' << ' ';
        for (auto & j : points[i])
            cout << '(' << j.first << ',' << j.second << ')' << ' ';
        cout << endl;
    }
    cout << 'g' << endl;
}


int main(int argc, char **argv){
    string s_string, n_string, l_string, c_string;
    int s= 10, n = 5, l = 5, c = 20;
    int command;

    while ((command = getopt (argc, argv, "s:n:l:c:?")) != -1)
        switch (command){
            case 's':
                s_string = optarg;
                s = atoi(s_string.c_str());
                if(s < 2) {
                    cerr << "Error: s is less than 2" << endl;
                    return 1;
                }
                break;

            case 'n':
                n_string = optarg;
                n = atoi(n_string.c_str());
                if(n < 1) {
                    cerr << "Error: n is less than 1" << endl;
                    return 1;
                }
                break;

            case 'l':
                l_string = optarg;
                l = atoi(l_string.c_str());
                if(l < 5) {
                    cerr << "Error: l is less than 5"  << endl;
                    return 1;
                }
                break;

            case 'c':
                c_string = optarg;
                c = atoi(c_string.c_str());
                if(c < 1) {
                    cerr << "Error: c is less than 1" << endl;
                    return 1;
                }
                break;

            case '?':
                cerr << "Error: unknown option: " << optopt << endl;
                return 1;

            default:
                return 0;
        }

    while(true){
        g_street(s, n, c);
        sleep(random_int(5,l));
        for (auto& i : names)
            cout << "r " << '"' << i << '"' << endl;
    }
}
