#include <bits/stdc++.h>

using namespace std;

bool isOpeartor(char); //Check whether the intended character is an operator
int compute(int, int, char); //Implement the input operator to the input numbers
void nextStep(); //Store and then pop the output-stack top twice and then call compute function
inline void removeSpaces(string&);

map<char, int> precedence = { //Map each operator to its precedence order
	{'^', 4}, 
	{'*', 3}, 
	{'/', 3}, 
	{'+', 2}, 
	{'-', 2}
};

stack<char> operators;
stack<int> output;

int main(){
    string input;
    cout<<"Enter the arithmetic expression: ";
    getline(cin, input);
    removeSpaces(input);
    for(int i = 0; i < input.size(); i++){
        if(isOpeartor(input[i])){
            if(operators.empty() || precedence[input[i]] > precedence[operators.top()] || input[i] == '^')
                operators.push(input[i]);
            else{
                while(!operators.empty() && precedence[operators.top()] >= precedence[input[i]] && operators.top() != '(')
                    nextStep();
                operators.push(input[i]);
            }
        }
        else if(input[i] == '(')
            operators.push(input[i]);

        else if(input[i] == ')'){
            while(!operators.empty() && operators.top() != '(')
                nextStep();
            operators.pop();
        }
        else{
            string num= "";
            while(!isOpeartor(input[i])){
                num += input[i];
                i++;
            }
            i--;
            output.push(stoi(num));
        }
    }
    while(!operators.empty()) //Final check: if stacks are empty...! if not does the final step
        nextStep();

    cout<<"\u250B "<<input<<" = "<<output.top()<<" \u250B"<<endl;
}

bool isOpeartor(char c){
    if(precedence.find(c) != precedence.end())
        return true;

    return false;
}
int compute(int b, int a, char c){
    switch (c){
        case '+':   return a+b;
        case '-':   return a-b;
        case '*':   return a*b;
        case '/':   return a/b;
        case '^':   return pow(a, b);
    }
}
void nextStep(){
    int a = output.top();
    output.pop();
    int b = output.top();
    output.pop();
    int result = compute(a, b, operators.top());
    operators.pop();
    output.push(result);
}

inline void removeSpaces(string& s){
    int i=0, j=0;
    while(i < s.length()){
        if(s[i] != ' ')
            s[j++] = s[i];
        i++;
    }
    s.resize(j);
}