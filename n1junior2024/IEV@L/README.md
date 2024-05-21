## IEV@L

+ Category: **Crypto**
+ Difficulty: ★★
+ Solved: 0
+ Tag: **isogeny hash, jail**

## Description

The eval function is full of dangers, taste the new IEV@L function.

## Details

定义了一个利用 `2-isogeny` 构造的哈希函数，需要找到 `print('Welcome 2 n1junior')` 的碰撞，并且碰撞的字符需要利用 eval 去完成 `getshell` 或者 `read flag`

## Solution

对于 `2-isogeny` 的图，每个点出度为3

函数 ihash 会检测是否进入自环，若进入自环则报错(同源图中自环数目较少)，注意到同源图为无向图，故限制哈希游走时不能从当前节点走到上一步的节点，这样可以利用每一比特信息决定当前节点走向

由于选择的模数比较小，图中任意两点存在规模为 $log_2N$ 的路径

其中 $N\approx\lfloor\frac{p}{12}\rfloor$ ，可以利用中间相遇的想法进行路径求解

下面解决如何构造 cmd

pyjail 里有大量技巧在不过滤的情况下利用 eval，但是这里需要利用那些能在命令中加载随机字符的绕过方式，即通过随机字符摆动我们的路径完成碰撞

出题时采用的 `__import__('os').system('/bin/sh;XXX')` 这种类似命令注入的方式，或者也可以采用 `cat /FLAG xxx` 的方式，但是需要明确文件名和路径

后来问了下Nightu师傅，发现还有一些其他的方法，`[a:=__import__('os').system("sh"),a:="XXX"]` 以及 `{1:"XXX",2:__import__('os').system("sh")}` 等可以自行了解

这样只需要完成  `ihash("__import__('os').system('/bin/sh;")` 到 `rev_ihash("')")` 的路径搜索

实际上 `rev_ihash` 比较难处理，但是由于要碰撞的字符具有相同后缀，相当于提供了一个现成的终点

故只需要完成 `ihash("__import__('os').system('/bin/sh;")` 到 `ihash("print('Welcome 2 n1junior")` 的路径搜索

由于采用 `input` 输入，命令部分必须全为 `utf-8` ，所以搜索出的路径不一定满足要求

这里利用路径穿越等想法像 `//bin/sh;` 或者 `/./bin/sh;` 或者 `;sh;` 都能形成不同的起点搜索到一个满足要求的路径即可
