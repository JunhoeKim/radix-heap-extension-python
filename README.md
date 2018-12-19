## Python implementation for radix heap extension

### input format (for shortest path)
 - [command] [parentNode] [childNode] [distance]
   ex) a 1 3 10
 - followed the format of shortest paths implementation challenge
   (http://www.dis.uniroma1.it/challenge9/download.shtml) 
 - input files placed in /inputs/*
 - ** show better performance node1000_mod.txt over node1000.txt
   (C is 100 in node1000_mod, but in 1000 in node1000)

### output format
 - [algorithm] : [elapsed time] [path count] [distance sum]

### how to run
 - python run.py [input file] [mode] (if mode is 1, print state of heap for each step)

### running example
~~~
> & python run.py .\inputs\node1000.txt
[data structure] : [elapsed time] [n] [distance]
---------------------------
Heapq : 0.402 1000 1376856
---------------------------
Radix level1 : 0.57 1000 1376856
---------------------------
Radix level2 : 0.435 1000 1376856
---------------------------
Fib. Heap : 0.525 1000 1376856
~~~

Reference
* AHUJA, R. K., MELHORN, K., ORLIN, J. B., AND TARJAN, R. E. 1990. Faster algorithms for the
shortest path problem. J. ACM 37, 213–223.