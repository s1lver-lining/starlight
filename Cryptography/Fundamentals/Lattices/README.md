This section was made using [A Gentle Tutorial for Lattice-Based Cryptanalysis](https://eprint.iacr.org/2023/032.pdf) and the [Cryptohack lattice section](https://cryptohack.org/challenges/maths/).


## Lattices definition

> *Definition:* Lattice
>
> Given linarly independent vectors $v_1, v_2, \dots, v_n \in \mathbb{R}^m$, the lattice generated by $b_1, b_2, \dots, b_n$ is the set of all integer linear combinations of $b_1, b_2, \dots, b_n$:
> $$L = \{x_1b_1 + x_2b_2 + \dots + x_nb_n : x_i \in \mathbb{Z}\}$$


## Lattice based problems

Many cryptography problems can be reduced to lattice-based problems. These probleme can then be seen as a lattice problem, usually `SVP` or `CVP` which can be solved using the LLL algorithm.

| Lattice-based problems |
| ---------------------- |
| Finding small roots of polynomials | 
| Knapsack problem | 
| Hidden number problem | 
| Extended HNP |

### Finding small roots of polynomials

Finding small roots of polynomials modulo a composite integer can be solved using Coppersmith's method.

> *Definition:* Small roots problem
>
> Given an integer $N$ and a *monic* polynomial $f(x)$ of degree $d$ with coefficients in $\mathbb{Z}_N$,
> find all $x\in$ $\mathbb{Z}_N$ such that $f(x) \equiv 0 \mod N$ and $\vert x \vert < B$.
> This means solving:
> $$f(x) = x^d + a_{d-1} x^{d-1} + \dots + a_1 x + a_0 \equiv 0 \mod N $$

This problem can be solved using the LLL algorithm on:

$$
\left(\begin{array}{cc}
N & & & & & \\
& BN & & & & \\
& & B^2N & & & \\
& & & \ddots & & \\
& & & & B^{d-1}N & \\
a_0 & a_1 & a_2 & \dots & a_{d-1} & B^d
\end{array}\right)
$$

* Implementation
    
    See [this python script](./Tools/small_roots.py) for a quick implementation of this. If you need to be more precise, use [this github repository](https://github.com/josephsurin/lattice-based-cryptanalysis/blob/main/lbc_toolkit/problems/small_roots.sage)



### Subset sum problem

The subset sum problem is a special case of the knapsack problem. 

> *Definition:* Subset sum problem
>
> Given a set of integers $S = \{s_1, s_2, \dots, s_n\}$ and a target integer $t$, find a subset $S' \subseteq S$ such that 
> $$\sum_{s_i \in S'} s_i = t$$


### Hidden number problem

> *Definition:* Hidden number problem
>
> Given a a prime $p$ and a secret integer $\alpha \in \mathbb{Z}_p$, the hidden number problem is to find $x$ $m$ pairs of integers $(t_i, a_i)$ for $i = 1, 2, \dots, m$ such that $$ \beta_i - t_i \alpha + a_i \equiv 0 \mod p$$
> where $\beta_i$ are unknown integers.

This problem can be solved using the LLL algorithm on:

$$
\left(\begin{array}{cc} 
p & & & & & \\
& p & & & & \\
& & \ddots & & & \\
& & & p & & \\
t_1 & t_2 & \dots & t_m & B/p & \\
a_1 & a_2 & \dots & a_m & & B/p
\end{array}\right)
$$

where $B$ is a bound on the size of the $\beta_i$.
