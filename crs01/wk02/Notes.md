# Stanford Algorithms Specialization on Coursera
## Course 01 - Week 02
2017-06-10

### Master Method

* For recursive algorithms
* NOTE: The version of the Master Method in this class requires recursions of equal size (more or less). Other versions - more complex - can handle uneven recursions.
* Define T(n) ("time/number of operations required based on input size n") for:
	* Base Case, T(1)
		* When n is sufficiently small to require no additional recursions
		* Frequently constant or linear O
	* Recursive Case, T(n)
		* When n is large enough to require additional recursions
		* Two components
			* The time/NOPs to recurse expressed as aT(n/b)
			* The time/NOPs to combine expressed as C*O(n^d)
			* So T(n) = aT(n/b) + C*O(n^d)
* Compare a, b, and d in the Recursive Case for three possible scenarios:
	* a = b^d : T(n) = O(n^d * log(n)) --> For recursive case!!!
	* a < b^d : T(n) = O(n^d)
	* a > b^d : T(n) = O(n^(log\_b(a))
* Neat Trick: If the Recursive Case can be defined as T(n) = aT(n/b) + Theta(n^d), then the cases are also asymptotic.
* Reminder: log\_b(n) = log\_a(b) / log\_a(b)
	* The equality case therefore ignores the logarithm base since different bases will differ by a constant
	* HOWEVER, the a > b^d case must include the bases since n raised to different constants has significant impact
* PROOF:
    * *Not 100% rigorous*
    * Assumptions:
        * Same Base Case and Recursive Case T(n) definitions as above
        * n is a power of b
    * Basic Idea:
        * Like direct Merge Sort analysis, think in terms of the number of sub-problems (k) at each level of a tree (j)
            * Level j=0 has k=1
            * Level j=1 has k=2
            * Level j=2 has k=4
            * Etc.
        * More generally, each level j from 0 to log\_b(n) has a^j sub-problems with input size n * (1/b)^j
        * "Zoom in" on a given level j to evaluate work done only in that level, not by subsequent recursions
            * Multiply the number of sub-problems times the amount of work done in each, again ignoring work done in subsequent recursions
            * We know the number of sub-problems, a^j
            * The amount of work depends on O(n^d) from above **but on a smaller size of n * (1/b)^j**
            * So Work(n, j) = a^j * (n * (1/b)^j)^d --> removed the O() to simplify notation; applies to entire formula
            * Or n^d * (a / b^d)^j) --> dropped the constant from C*O(b^d)
        * Then sum over j levels
            * TotalWork(n) = n^d * sum[j=0 --> log\_b(n)]((a / b^d)^j)
            * Now the cases start to resolve:
                * a = b^d : the sum simplifies to adding one log_b(n) + 1 times
                * a < b^d : the sum simplifies to adding a value k that approaches 0 as j increases
                    * It has an asymptote at some constant
                    * Rephrased: Work done at the root > sum work at all subsequent levels
                * a > b^d : Does not have an easy simplification
                    * However, supressing a couple constants using O() and incorporating it with the n^d, we get
                        * TotalWork(n) = O(n^d * (a / b^d)^log\_b(n))
                        * = O(a^log\_b(n)) * n^d * b^(-d * log\_b(n)))
                        * = O(a^log\_b(n)) * n^d * (b^log\_b(n))^(-d))
                        * = O(a^log\_b(n)) * n^d * n^(-d))
                        * = O(a^log\_b(n)) = O(n^log\b(a)) --> take log\_b or both sides if you don't believe!
                    * See the "Helpful reminder" below
                    * Rephrased: Work done at the lowest level > sum work at all preceding levels
* Helpful reminder for summations
    * Given a ratio r > 0 and r != 1
    * The sum[i=0 --> k](r^i) = (r^(k + 1) - 1) / (r - 1)
* DON'T FORGET:
    * The Master Method only yields O() or Theta() for the recursive component
    * Must still add the base case * the number of sub-problems at the base case
    * Generally not a significant factor