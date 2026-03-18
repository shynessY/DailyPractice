#include <vector>
#include <iostream>
#include <algorithm>
#include  <string>
#include <ctime>
using namespace std;
class Solution {
/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

public:
    vector<int> findAnagrams(string s, string p) {
        //首先肯定能够想到当s的长度小于p时，肯定是没有的
        vector<int> a;
        int sSize=s.size(),pSize=p.size();
        if(sSize<pSize){
            return a;
        }
        //主要思路是将s按照p的长度从左到右遍历，取出区间，然后sort，与sort后的p比较
        sort(p.begin(),p.end());
        for(int i=0;i<sSize-pSize+1;i++)
        {
            string newS=s.substr(i,pSize);
            sort(newS.begin(),newS.end());
            if(newS==p){
                a.push_back(i);
            }
        }
        return a;
    }
};
/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
class Solution1 {
public:
    vector<int> findAnagrams(string s, string p) {
        vector<int> res;
        int n = s.size(), m = p.size();
        if (n < m) return res;

        vector<int> pCount(26, 0), sCount(26, 0);
        for (char c : p) pCount[c - 'a']++;

        for (int i = 0; i < n; i++) {
            sCount[s[i] - 'a']++;                   // 加入右边界字符
            if (i >= m) {
                sCount[s[i - m] - 'a']--;           //"因为会有这样的情况,当s为abab,p为ab的时候,当i=2时,sCount会多一个a,所以需要减去左边界字符"，
                                                    //类比下来就是当i>=m时，说明窗口已经超过了p的长度，需要将左边界字符移出窗口，所以sCount需要减去s[i - m]对应的计数。
            }
            if (sCount == pCount) {                 //solution1中主要核心是使用了一个字母表来记录p中每个字母的出现次数，再利用for循环来移动一个滑动的窗口，只不过就像上面注释所说的那样需要特殊处理一下
                                                    
                res.push_back(i - m + 1);
            }
        }
        return res;
    }
};
/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
class Solution2 {
public:
    vector<int> findAnagrams(string s, string p) {
        int sLen = s.size(), pLen = p.size();

        if (sLen < pLen) {
            return vector<int>();
        }

        vector<int> ans;
        vector<int> count(26);
                                //先初始化第一个窗口
        for (int i = 0; i < pLen; ++i) {
            ++count[s[i] - 'a'];
            --count[p[i] - 'a'];
        }
                                    //计算刚开始的differ
        int differ = 0;
        for (int j = 0; j < 26; ++j) {
            if (count[j] != 0) {
                ++differ;
            }
        }

        if (differ == 0) {
            ans.emplace_back(0);    //如果相等，这说明第一个窗口就是一个异位词，直接加入结果中
        }

        for (int i = 0; i < sLen - pLen; ++i) {
            if (count[s[i] - 'a'] == 1) {  //在移动之前如果s[i]这个字符所对应的是1，那么就表明此时p的这个字符的数量比s的这个字符的数量多1，
                                    //所以当我们将s[i]这个字符移出窗口时，窗口中字母 s[i] 的数量与字符串 p 中的数量从不同变得相同，所以differ需要减1
                --differ;
            } else if (count[s[i] - 'a'] == 0) {  //同样的，在移动之前，如果s[i]这个字符所对应的是0，那么就表明此时p的这个字符的数量与s的这个字符的数量相同，
                                    //所以当我们将s[i]这个字符移出窗口时，窗口中字母 s[i] 的数量与字符串 p 中的数量从相同变得不同，所以differ需要加1
                ++differ;
            }
            --count[s[i] - 'a'];    //处理真正的移动，也就是将s[i]这个字符移出窗口，所以s[i]这个字符的数量需要减1
                                    //下面就是处理将s[i+pLen]这个字符加入窗口的情况了，同样的道理，如果s[i+pLen]这个字符所对应的是-1，
                                    //那么就表明此时p的这个字符的数量比s的这个字符的数量少1，先到这里我有疑问？问什么处理前后if的时候前面是0,1而后面是-1,0呢？这其实跟
                                    //初始化的时候有关，在初始化第一个窗口的时候，我们是先将s[i]这个字符的数量加1，再将p[i]这个字符的数量减1，所以当s[i]这个字符的数量为1时，说明p的这个字符的数量比s的这个字符的数量多1，
                                    //当s[i]这个字符的数量为0时，说明p的这个字符的数量与s的这个字符的数量相同，
                                    //而当s[i+pLen]这个字符的数量为-1时，在之前的滑动窗口并没有出现过这个字符，而p里面一定有这个字符，甚者可能会出现-2的情况，但这并不影响，我们只需要处理临界状况
                                    //什么是临界状况，就是会影响differ的特殊情况
            if (count[s[i + pLen] - 'a'] == -1) {  // 窗口中字母 s[i+pLen] 的数量与字符串 p 中的数量从不同变得相同
                --differ;
            } else if (count[s[i + pLen] - 'a'] == 0) {  // 窗口中字母 s[i+pLen] 的数量与字符串 p 中的数量从相同变得不同
                ++differ;
            }
            ++count[s[i + pLen] - 'a'];
            
            if (differ == 0) {
                ans.emplace_back(i + 1);
            }
        }

        return ans;
    }
};//https://leetcode.cn/problems/find-all-anagrams-in-a-string/solutions/1123971/zhao-dao-zi-fu-chuan-zhong-suo-you-zi-mu-xzin/来源：力扣（LeetCode）

//soulution2是官方的滑动窗口的优化版本，本人觉得十分得精妙，在原来要滑动的情况下，通过实时维护一个count数组来记录当前窗口
//中每个字母与p中对应字母的数量差异，并通过一个differ变量来记录当前窗口与p的差异程度，从而在每次滑动窗口时只需要O(1)的时间复杂度
//来更新differ，而不需要每次都比较整个count数组，从而将整体时间复杂度优化到O(n)。并且该方法只需要遍历一次p，除了初始化第一个窗口的时候，后面只需要处理窗口的前后两个字符，所以整体效率非常高。
//另外，在c++中应该尽量把自增和自减符号放在前面（因为某些原因）
int main(){
    Solution s;
    string str1="cbaebabacd";
    string str2="abc";
    vector<int> a=s.findAnagrams(str1,str2);
    for(int i=0;i<a.size();i++){
        cout<<a[i]<<" ";
    }
}