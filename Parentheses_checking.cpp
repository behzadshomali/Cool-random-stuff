#include <bits/stdc++.h>

using namespace std;

int main(){
    string input;
    cout<<"Enter the arithmetic experssion: ";
    getline(cin, input);
    int i = 0;
    stack<pair<char, int>> s;
    while(i < input.length()){
        if(input[i] == ')'){
            if(s.size() == 0){
                cout<<"Oops parentheses aren't matched at the "<<i<<" index!"<<endl;
                return 0;
            }
            s.pop();
        }
        else if(input[i] == '(')
            s.push(make_pair(input[i], i));
        i++;
    }
    if(s.size() == 0)
        cout<<"Everything is OK!"<<endl;
    else{
        cout<<"Oops parentheses aren't matched at the ";
        while(!s.empty()){
            cout<<s.top().second<<" ";
            s.pop();
        }
        cout<<"index(es)!"<<endl;
    }
}