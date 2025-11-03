## n1fsr

+ Category: **Crypto**
+ Difficulty: ★★
+ Tag: **LFSR, Linear Algebra**

## Description

Our encounters with LFSRs over the years. 📅

## Solution

This challenge provides a series of masks and filters. You first need to perform some basic analysis on the data. Some useful properties can be found.

+ The second filter is linear.

+ Mask (`0x83c7efefc783`) has a very short cycle.

+ Some masks have the same cycle length.

The intended solution is to use these properties to linearize. Let's consider the number of variables.

Firstly, for LFSRs with a linear filter or no filter, we will treat their initial state as unknown variables. This will produce `32+24` variables. Then, we can merge the output of filter with the same cycle lfsr, that is, treat the outputs of filters as variables rather than the lfsr state. This will add `63+255` variables. In the end, only 10 bits and 14 bits lfsr need to be processed. Linearizing directly will add $\sum_{i=1}^7 (\binom{14}{i}+\binom{10}{i})$ variables. This is much more than the amount of data we have. We can brute-force the 7 bits of lfsr-14 and the 3 bits of lfsr-10. In this case, `127*2` variables are added. 

Therefore, we will have a linear system of 628 variables. $2^{10}$ different matrices are constructed in the offline phase (before interaction). The online phase which includes  solving $2^{10}$ matrix equations will be completed in only 5 seconds. After we get solution, the simplest way to obtain the subsequent output is to construct the matrix in the same rule then multiply the solution.
