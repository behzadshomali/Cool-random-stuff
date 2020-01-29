This piece of code is a C++ header which implements Quicksort but it differs with common Quicksort algorithms. (Why?) Cause it is working with 2 pivots (instead of 1) so it is called 5 Way-Partition Quicksort. The order is going to be like: 
[inclusive, inclusive]

from p  to q1-1 --> values<pivot1
from q1 to q2-1 --> values=pivot1
from q2 to q3-1 --> pivot1<valuse<pivot2
from q3 to q4-1 --> values=pivot2
from q4 to r    --> values>pivot2
