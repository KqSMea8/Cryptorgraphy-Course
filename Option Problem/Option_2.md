从直观看，$GF(2^8)$在乘法上以一个“素数”做模，比如$GF(2^8)$的模数是0x11b（十进制的283），使得乘法具有群属性。于是，我们就脑洞打开把此推广到$GF(2^n$)去。找一个大于$2^n$且接近于$2^n$的素数做模数，就构成一个$GF(2^n)$。请问这种想法对不对？请验证自己的想法，并编程实现任意$GF(2^n)$的构造，也许模数可以自动选择或者手工指定，但是你要说明理由，至少实现上要对。

- 错的，比如$17=x^4+1$，有$(x+1)*(x^3+x^2+x+1)=x^4+1$

- 代码

  ```python
  def isPolynomialIrreducibleOnGF2n(p):
      """
      the calculate on polynomial's coefficient is under mod 2
      """
      if not isinstance(p, pl.Polynomial):
          raise TypeError
      for i in range(2, p.expression):
          if not p.gcd(pl.Polynomial(i)).equal(pl.Polynomial(1)):
              return False
      return True
  
  def constructGF2n(n: int):
      for i in range(1 << n, 1 << (n + 1)):
          if util.isPolynomialIrreducibleOnGF2n(pl.Polynomial(i)):
              return True, pl.Polynomial(i)
      return False, pl.Polynomial(0)
  ```