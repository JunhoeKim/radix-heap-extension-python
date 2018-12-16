## Python implementation for radix heap extension

### input format (for shortest path)
 - followed the format of shortest paths implementation challenge
   (http://www.dis.uniroma1.it/challenge9/download.shtml) 
 - [command] [parentNode] [childNode] [distance]
   ex) a 1 3 10
 - input files placed in /inputs/*

### output format
 - [algorithm] : [elapsed time] [path count] [distance sum]

### how to run
 - python run.py [input file]

### description for demo
 - 여기 추가 필요

### running example
~~~
> & python run.py .\inputs\node2000.txt
---------------------------
naive heap : 1.91 2000 5540
---------------------------
Radix level1 : 1.055 2000 5540
---------------------------
Radix level2 : 0.976 2000 5540
---------------------------
Fib. Heap : 12.983 2000 5540
~~~

Reference
* AHUJA, R. K., MELHORN, K., ORLIN, J. B., AND TARJAN, R. E. 1990. Faster algorithms for the
shortest path problem. J. ACM 37, 213–223.