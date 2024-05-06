//用户界面版，可以不断输入数据。暂时是死循环

#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <limits> //出于适用场景考虑，使用到了limits，尽管在题目下上下界好找
#include <iomanip> // 添加头文件 <iomanip> 来使用 setw 函数

using namespace std;

int main() {
    // 输入每二三四组期待分到的数字数量
    

    // 原始数组
    vector<double> arr = { -1.65, -1.28, -1.04, -0.84, -0.685, -0.525, -0.385, -0.265, -0.125, 0 , 0.125 , 0.265 , 0.385 , 0.525 , 0.685 , 0.84 , 1.04 , 1.28 , 1.65 };

    // 初始化动态规划数组和路径数组
    const int N = arr.size();
    const int K = 5; // 分成五组

    vector<int> groupSizes(3);
    int flag = 1;

    do
    {
        cout << "Please enter three numbers representing the expected number of digits to be allocated for each group:" << endl;
        for (int i = 0; i < 3; ++i) {
            cout << "Group " << i + 2 << ": ";
            cin >> groupSizes[i]; // 读取用户输入的数字，并存储到 vector 中
        }

        vector<vector<double>> dp(N + 1, vector<double>(K + 1, numeric_limits<double>::infinity()));
        vector<vector<int>> prev(N + 1, vector<int>(K + 1, -1)); // 记录路径

        //// 计算总共需要分配的数字数量；在检测输入数字总和合法性时可以用
        //int totalSize = 0;
        //for (int size : groupSizes) {
        //    totalSize += size;
        //}

        // 动态规划求解

        for (int i = 0; i <= N; ++i) {
            //dp[i][1] = (i == 0) ? numeric_limits<double>::infinity() : arr[i - 1]; // 第一列
            dp[i][1] = numeric_limits<double>::infinity(); //
        }

        for (int j = 2; j <= K; ++j) {
            for (int i = j - 1; i <= N; ++i) {
                if (j >= 2 && j <= 4) { // 只在第二、三、四组考虑连续性
                    int groupSize = 0;
                    for (int k = i - 1; k >= max(1, i - groupSizes[j - 2]); --k) {
                        double maxVal = arr[i - 1];
                        double minVal = arr[i - 1];
                        for (int l = i - 1; l >= k; --l) {
                            maxVal = max(maxVal, arr[l]);
                            minVal = min(minVal, arr[l]);
                        }
                        groupSize++;
                        if (groupSize >= groupSizes[j - 2]) {
                            double newValue;
                            if (j == 2)
                                newValue = maxVal - minVal;
                            else
                            {
                                newValue = max(dp[k][j - 1], maxVal - minVal);
                            }
                            if (newValue < dp[i][j]) {
                                dp[i][j] = newValue;
                                prev[i][j] = k;
                            }
                        }
                    }
                }
                else { // 其他组不考虑连续性
                    for (int k = j - 2; k < i; ++k) {
                        double maxVal = arr[i - 1];
                        double minVal = arr[i - 1];
                        for (int l = i - 1; l >= k; --l) {
                            maxVal = max(maxVal, arr[l]);
                            minVal = min(minVal, arr[l]);
                        }
                        double newValue = max(dp[k][j - 1], maxVal - minVal);
                        if (newValue < dp[i][j]) {
                            dp[i][j] = newValue;
                            prev[i][j] = k;
                        }
                    }
                }
            }
        }

        // 输出结果
        cout << "Min-max difference of 2nd, 3rd, 4th group: " << dp[N][K] << endl;

        // 输出结果
        for (int i = 0; i <= K; ++i) {
            for (int j = 0; j <= N; ++j) {
                if (i == 0 && j == 0) {
                    cout << setw(6) << " ";
                }
                else if (i == 0) {
                    cout << setw(6) << j;
                }
                else if (j == 0) {
                    cout << setw(6) << i;
                }
                else {
                    cout << setw(6) << dp[j][i];
                }
            }
            cout << endl;
        }

        //cout << prev[2][1]<<endl;
        // 输出各组被分到的数字
        vector<vector<double>> groups(K);
        int i = N, j = K;
        while (j > 0) {
            int start = prev[i][j];
            if (start == -1) break; // 判断是否越界
            for (int k = start; k < i; ++k) {
                groups[j - 1].push_back(arr[k]);
                //cout << start << " k:" << k << " arr[k]" << arr[k] << " j-1 " << j - 1 <<" i "<<i << endl;
            }
            i = start;
            j--;

        }

        cout << "Numbers in each group:" << endl;
        for (int i = 0; i < K; ++i) {
            cout << "Group " << i + 1 << ": ";
            for (double num : groups[i]) {
                cout << num << " ";
            }
            cout << endl;
        }
        cout << endl;
    }while (flag);

    return 0;
}
