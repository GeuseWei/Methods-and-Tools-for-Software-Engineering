#include <vector>
#include <sys/wait.h>
#include <unistd.h>
#include <csignal>
#include <iostream>

using namespace std;

int main (int argc, char **argv) {
    string s_string, n_string, l_string, c_string;
    int s= 10, n = 5, l = 5, c = 20;
    int command;


    while ((command = getopt (argc, argv, "s:n:l:c:?")) != -1)
        switch (command)
        {
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
                    cerr << "Error: l is less than 5" << endl;
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

    vector<pid_t> children;
    pid_t child;

    int r_a1[2];
    pipe(r_a1);

    int a1_a2[2];
    pipe(a1_a2);

    // run rgen.cpp
    child = fork();
    if (child == 0) {
        dup2(r_a1[1], STDOUT_FILENO);
        for (int i : r_a1)
            close(i);
        execv("rgen", argv);

    }
    children.push_back(child);

    // run a1ece650.py
    child = fork();
    if (child == 0) {
        dup2(r_a1[0], STDIN_FILENO);
        for (int i : r_a1)
            close(i);
        dup2(a1_a2[1], STDOUT_FILENO);
        for (int i : a1_a2)
            close(i);
        execv("a1ece650.py", argv);
    }
    children.push_back(child);

    // run a2ece650.cpp
    child = fork();
    if (child == 0) {
        dup2(a1_a2[0], STDIN_FILENO);
        for (int i : a1_a2)
            close(i);
        execv("a2ece650", argv);
    }
    children.push_back(child);

    // run a3ece650.cpp
    child = fork();
    if (child == 0) {
        dup2(a1_a2[1], STDOUT_FILENO);
        for (int i : a1_a2)
            close(i);
        string input;
        while (true){
            getline(cin, input);
            if (cin.eof())
                break;
            if (!input.empty())
                cout << input << endl;
        }
    }
    children.push_back(child);

    int m;
    wait(&m);

    for (pid_t i : children) {
        int status;
        kill (i, SIGTERM);
        waitpid(i, &status, 0);
    }

    return 0;
}

