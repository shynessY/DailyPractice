#include <iostream>
#include <vector>
#include <unordered_map>
using std::vector;
using std::cout;
using std::unordered_map;
class Solution1 {
public:
    int subarraySum(vector<int>& nums, int k) {
        int numsSize= nums.size(),res=0;
        for(int i=0;i<numsSize;++i){
            int sums=nums[i],j=i+1;
            if(sums==k)++res;
            while(j<numsSize){
                sums+=nums[j];
                if(sums==k)++res;
                ++j;
            }
        }
        return res;
    }
};
//第一次做出来的方法显然时间复杂度过高，暴力解法，O(n^2)，需要优化
class Solution2 {
public:
    int subarraySum(vector<int>& nums, int k) {
        int sums=0,res=0;
        unordered_map<int,int>hasMap;
        for(auto i:nums){
            hasMap[0]=1;//前缀和为0的子数组出现一次,为什么要添加这个呢？例如1，2，3,target为6，那么前三个的和分别为1，3，6。
            //明明是有结果的，但是如果没有添加前缀和为0的子数组出现一次，那么在计算到6的时候就会去hasmap中找sums-k=6-6=0的前缀和
            sums+=i;
            if(hasMap.contains(sums-k)){
                res+=hasMap[sums-k];
            }
            hasMap[sums]++;
        }
        return res;
    }
};
//第二种方法使用了前缀和，使用了hashmap来记录前缀和出现的次数，每次计算完当前的前缀和之后就去hasmap中找
//是否存在sums-k的前缀和，如果存在就说明在当前前缀和之前存在一个前缀和为sums-k的子数组，那么这个子数组的和就是k，res就加上这个前缀和出现的次数，最后返回res即可
int main(){
    //test
}