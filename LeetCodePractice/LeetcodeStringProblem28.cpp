#include <vector>
#include <string>
#include <iostream>
using namespace std;
class Solution {
public:
//kmp算法，时间复杂度O(m+n)，空间复杂度O(m)
    vector<int> getNextFunction(string a){
        int n = a.size();
        vector<int>next(n);
        for(int i = 1;i<n;++i){
            //因为在计算pi函数的时候，下一位的pi函数值要么是上一个加1，要么就小于等于上一个
            int j = next[i-1];
            while(j>0&&a[j]!=a[i])j=next[j-1];//回溯
            if(a[j]==a[i]){
                next[i]=++j;
            }
        }
        return next;
    }
    int strStr(string haystack, string needle) {
        if(haystack.size()<needle.size()){
            return -1;
        }
        string haystackNew=needle+'#'+haystack;
        vector<int>a = getNextFunction(haystackNew);
        for(int i = needle.size()+1;i<needle.size()+haystack.size()+1;i++){
            if(a[i]==needle.size()){
                return i-2*needle.size();
            }
        }
        return -1;
    }
};
int main(){
    Solution s;
    string haystack = "hello", needle = "ll";
    cout<<s.strStr(haystack, needle)<<endl;
    return 0;
}