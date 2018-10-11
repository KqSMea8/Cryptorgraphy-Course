- Write a program to play with $\mathbb{Z}_p^*$，where p is a prime. (a) What is the order of $\mathbb{Z}_p^*$. (b) Find all the generators of $\mathbb{Z}_{11}^*$ and $\mathbb{Z}_{13}^*$. (c) How many generators do $\mathbb{Z}_{11}^*$ and $\mathbb{Z}_{13}^*$ have. (d) Have more computation. Then find a pattern, and make a conjecture about the number of generator of $\mathbb{Z}_{p}^*$, for any prime $p$. Prove it. 

  - 根据定义，$Z_n^*=\{x|gcd(x,n)=1\}$，所以，order是$\phi(n)$，所以为p-1

  - 11: 2, 6, 7, 8. 13: 2, 6, 7, 11

  - 4， 4

  - $\phi(p-1)$ 个，证明如下

    - 首先，对于整系数D次多项式$F(x)$和素数$p$，$F(x)\equiv 0(mod\ p)$ 有至多D个解

      - 对于D为1，显然成立
      - 假设对于$D\leq k$ 时成立，以下证明对于$D=k+1$ 成立
        - 如果没有解，那么显然成立
        - 如果有解，假设是a，即$F(a)-kp=0$，则可以设$F(x)-kp=(x-a)h(x)$，其中$h(x)$ 是$k$次多项式，保证$h(x)$ 存在
          - 构造$h(x)$ 的过程其实就是构造一个方程，对于使得$F(x)$ 为0的$x$的取值，其也取值为0。（设这些取值构成为$x_1, x_2, x_3...$ ）。所以必然可以构造出一个result 矩阵$A$，其乘以系数向量$c$得到结果向量，结果向量$r$的element为$bp(b\in N)$ ，保证这个result矩阵为可逆矩阵。
          - 假设有$d+1$ 个取值使得$F(x)$ 过零点，那么$h(x)$从$\{x^i|0\leq i\leq n\}$中取$d$ 个元素$x^{p_1}, x^{p_2}, x^{p_3}...$（且必然要包括$x^n$），这些元素系数包括所有不为0的系数，分别为$c_1, c_2,...$，构成系数向量
          - 然后，A矩阵的第$i$行为$[x_i^{p_1}, x_i^{p_2}, ....]$。$A$ 矩阵可逆。
          - 所以，可以求得系数向量$c$ ，那么$h(x)$ 存在
        - 根据假设，$h(x)$ 至多有$D$个解，所以$F(x)$ 至多有$D+1$ 个解

    - 现在，对于素数$p$ 和任意$Z_p^*$ 上的元素$X$，设$p-1=nq$ ，则$$X^{p-1}-1=X^{nq}-1=(X^n-1)((X^n)^{q-1}+(X^n)^{q-2}+((X^n)^{q-3}+...+(X^n)^1+1)$$ 

      根据欧拉定理，$X^{p-1}=1(mod\ p)$ 有p-1个解，而右式一个有至多$n$个解，一个至多有$nq-n$ 个解，所以右式最多有$p-1$个解，所以$X^n-1$ 一定有$n$个解

    -  设$\varphi(j)$ 为使得$a^j=1(mod\ p)$ 成立的a的个数（其中，对于任意一个a，$j$ 是使其满足式子的最小正整数），则$\varphi(d_1)+\varphi(d_2)+...=n$ 其中，$d_i$为$n$ 的因子（不仅仅是素因子）

    - 利用$\phi(d_1)+\phi(d_2)+...=n$，使用归纳法可以证明$\varphi(n)$ 刚好等于$\phi(n)$ ，所以有$\varphi(p-1)=\phi(p-1)$个原根 

      - 如果n=1，则$\varphi(1)=\phi(1)​$

      - 设对于$s<t$ 都满足$\varphi(s)=\phi(s)$ ，对于$$\varphi(t)=\varphi(d_1)+\varphi(d_2)+...+\varphi(t)=t=\phi(d_1)+\phi(d_2)+...+\phi(n)$$

        因为$d_i<t$，所以可以消去，所以$\phi(n)=\varphi(n)$

- Write a program to play with $\mathbb{Z}_n^*$. (a) Given an integer $n$, construct the multiplicative group $\mathbb{Z}_n^*$; (b) Find a subgroup of the group $\mathbb{Z}_n^*$; (c) Find a relation between the size of subgroup and the size of $\mathbb{Z}_n^*$.

  - ```python
    def constructZn(n):
        ans = []
        for i in range(1, n):
            if util.binaryGCD(n, i) == 1:
                ans.append(i)
        return ans
    ```

  - 因为是有限群，所以任意一个元素都可以形成循环群，并且这个循环群也是子群

  - $|S|\Big||Z_n^*|$

- Suppose that $q$ is a prime and $p = 2*q + 1$ is also a prime. Let $g = h^{(p-1)/2} $ is not equal to $1$, where $h$ is a random number choosen from $\mathbb{Z}_p$. Certainly, $\langle g \rangle$ is a cyclic group. \\ (a) Write a python(or Sage) program to generate the cyclic group $\langle g \rangle$.\\ (b) What is the order of $\langle g \rangle$, and why?\\ (c) How many generators are there in the group $\langle g \rangle$? Why?

  - ```python
    lambda x : [x*i%p for i in range(1, p+1)]
    ```

  - p或1。因为$|Z_p|=p$ ，根据拉格朗日定理，子群要么都是0，order为1，要么等于$Z_p$，order 为 p

  - p-1个或1个，除了0（order是1），其余元素形成的子群等于$Z_p$

