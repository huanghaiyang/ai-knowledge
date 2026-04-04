# LaTeX数学公式编写指南

## 概述

本文档说明如何在Markdown文件中正确编写LaTeX数学公式，以便在前端正确渲染。

## 基本语法

### 行内公式
使用单个美元符号 `$` 包裹公式：

```markdown
这是一个行内公式 $E = mc^2$ 的示例。
```

### 块级公式
使用双美元符号 `$$` 包裹公式：

```markdown
$$
f(x) = \frac{1}{\sqrt{2\pi}} e^{-\frac{x^2}{2}}
$$
```

## 常用数学符号

### 希腊字母

| 符号 | LaTeX代码 | 示例 |
|------|-----------|------|
| α | `\alpha` | `$\alpha$` |
| β | `\beta` | `$\beta$` |
| γ | `\gamma` | `$\gamma$` |
| δ | `\delta` | `$\delta$` |
| ε | `\epsilon` | `$\epsilon$` |
| θ | `\theta` | `$\theta$` |
| λ | `\lambda` | `$\lambda$` |
| μ | `\mu` | `$\mu$` |
| π | `\pi` | `$\pi$` |
| σ | `\sigma` | `$\sigma$` |
| φ | `\phi` | `$\phi$` |
| ω | `\omega` | `$\omega$` |
| Δ | `\Delta` | `$\Delta$` |
| Σ | `\Sigma` | `$\Sigma$` |

### 数学运算符

| 符号 | LaTeX代码 | 示例 |
|------|-----------|------|
| ∂ | `\partial` | `$\partial$` |
| ∑ | `\sum` | `$\sum_{i=1}^{n}$` |
| ∏ | `\prod` | `$\prod_{i=1}^{n}$` |
| ∫ | `\int` | `$\int_{a}^{b}$` |
| √ | `\sqrt` | `$\sqrt{x}$` |
| ∞ | `\infty` | `$\infty$` |
| · | `\cdot` | `$a \cdot b$` |
| × | `\times` | `$a \times b$` |
| ÷ | `\div` | `$a \div b$` |
| ± | `\pm` | `$\pm$` |
| ∓ | `\mp` | `$\mp$` |

### 关系符号

| 符号 | LaTeX代码 | 示例 |
|------|-----------|------|
| ≠ | `\neq` | `$\neq$` |
| ≤ | `\leq` | `$\leq$` |
| ≥ | `\geq` | `$\geq$` |
| ≈ | `\approx` | `$\approx$` |
| ∈ | `\in` | `$\in$` |
| ∉ | `\notin` | `$\notin$` |
| ⊂ | `\subset` | `$\subset$` |
| ⊆ | `\subseteq` | `$\subseteq$` |
| ∪ | `\cup` | `$\cup$` |
| ∩ | `\cap` | `$\cap$` |

### 箭头符号

| 符号 | LaTeX代码 | 示例 |
|------|-----------|------|
| → | `\rightarrow` | `$\rightarrow$` |
| ← | `\leftarrow` | `$\leftarrow$` |
| ↔ | `\leftrightarrow` | `$\leftrightarrow$` |
| ⇒ | `\Rightarrow` | `$\Rightarrow$` |
| ⇐ | `\Leftarrow` | `$\Leftarrow$` |
| ⇔ | `\Leftrightarrow` | `$\Leftrightarrow$` |

## 常用公式示例

### 线性回归

```markdown
简单线性回归模型：
$$y = wx + b$$

多元线性回归模型：
$$y = w_1x_1 + w_2x_2 + \cdots + w_nx_n + b$$

矩阵形式：
$$\mathbf{y} = \mathbf{X}\mathbf{w} + \mathbf{b}$$
```

### 损失函数

```markdown
均方误差（MSE）：
$$MSE = \frac{1}{n} \sum_{i=1}^{n} (y_{pred} - y_{true})^2$$

交叉熵损失：
$$L = -\sum_{i} y_i \log(\hat{y}_i)$$
```

### 梯度下降

```markdown
权重更新公式：
$$\mathbf{w} = \mathbf{w} - \eta \nabla L$$

链式法则：
$$\frac{\partial L}{\partial W^l} = \frac{\partial L}{\partial a^l} \cdot \frac{\partial a^l}{\partial z^l} \cdot \frac{\partial z^l}{\partial W^l}$$
```

### 激活函数

```markdown
Sigmoid函数：
$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

ReLU函数：
$$ReLU(z) = \max(0, z)$$

Softmax函数：
$$softmax(z_i) = \frac{e^{z_i}}{\sum_{j} e^{z_j}}$$
```

### 神经网络

```markdown
前向传播：
$$z^{[l]} = W^{[l]} a^{[l-1]} + b^{[l]}$$
$$a^{[l]} = g(z^{[l]})$$

反向传播：
$$\delta^{[l]} = ((W^{[l+1]})^T \delta^{[l+1]}) \odot g'(z^{[l]})$$
```

### 卷积神经网络

```markdown
卷积操作：
$$(I * K)(i, j) = \sum_{m} \sum_{n} I(i+m, j+n) K(m, n)$$

池化操作：
$$max_{m,n} I(i+m, j+n)$$
```

### 注意力机制

```markdown
自注意力：
$$Attention(Q, K, V) = softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

位置编码：
$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$
$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$
```

### 概率统计

```markdown
贝叶斯定理：
$$P(A|B) = \frac{P(B|A)P(A)}{P(B)}$$

正态分布：
$$f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

期望：
$$E[X] = \sum_{i} x_i p(x_i)$$
```

## 重要提示

### 1. 不要使用Unicode符号

❌ 错误示例：
```markdown
$∂L/∂W = ∂L/∂a · ∂a/∂z · ∂z/∂W$
```

✅ 正确示例：
```markdown
$\frac{\partial L}{\partial W} = \frac{\partial L}{\partial a} \cdot \frac{\partial a}{\partial z} \cdot \frac{\partial z}{\partial W}$
```

### 2. 使用正确的LaTeX语法

❌ 错误示例：
```markdown
$y = wx + b$  # 缺少空格
```

✅ 正确示例：
```markdown
$y = w x + b$  # 运算符前后有空格
```

### 3. 分数使用 \frac

❌ 错误示例：
```markdown
$1/2m * sum(...)$
```

✅ 正确示例：
```markdown
$\frac{1}{2m} \sum ...$
```

### 4. 上标和下标

```markdown
$x^2$          # 上标
$x_i$          # 下标
$x_i^j$        # 同时上下标
$x^{i+j}$      # 复杂上标
$x_{i,j}$      # 复杂下标
```

### 5. 矩阵和向量

```markdown
向量：$\mathbf{x}$, $\vec{x}$
矩阵：$\mathbf{W}$, $\mathbf{X}$
转置：$\mathbf{W}^T$
点积：$\mathbf{a} \cdot \mathbf{b}$
```

## 常用环境

### 对齐公式

```markdown
$$
\begin{aligned}
y &= wx + b \\
z &= \sigma(y) \\
L &= \frac{1}{2}(z - \hat{z})^2
\end{aligned}
$$
```

### 矩阵

```markdown
$$
\mathbf{W} = \begin{bmatrix}
w_{11} & w_{12} & \cdots & w_{1n} \\
w_{21} & w_{22} & \cdots & w_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
w_{m1} & w_{m2} & \cdots & w_{mn}
\end{bmatrix}
$$
```

### 分段函数

```markdown
$$
f(x) = \begin{cases}
0 & \text{if } x < 0 \\
x & \text{if } x \geq 0
\end{cases}
$$
```

## 参考资料

- [KaTeX支持的函数](https://katex.org/docs/supported.html)
- [LaTeX数学符号大全](https://en.wikibooks.org/wiki/LaTeX/Mathematics)
- [Markdown数学公式教程](https://www.markdownguide.org/extended-syntax/#math)

---

**注意**：编写数学公式时，请始终使用LaTeX语法，不要使用Unicode数学符号，以确保在前端正确渲染。