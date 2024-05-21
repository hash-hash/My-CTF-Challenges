## c0d3+

+ Category: **Crypto**
+ Difficulty: ★☆
+ Tag: **LWE**

## Description

m@91C c0D3 ➡️ Magic Code!

## Solution

LWE与编码都是在做一些误差恢复的问题，但是不同的是 LWE 是 large weight, small error; Code 是 small weight, large error 。

这里最原始的方案需要求解一个 384 维度的格子，使用sage内置LLL耗时较长，可以利用线性的方式先降维到 256，再用flatter加速做约化，最终差不多一分钟结束。