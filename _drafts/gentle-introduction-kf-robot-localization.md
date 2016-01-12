---
layout: post
title:  An intuitive introduction to the Kalman filter
comments: true
date:   2016-01-12
---

Introductory paragraph will go here. Remember to write disclaimer saying that it's to get an intuitive understanding, not technically rigourous with proofs. Maybe talk about how it's a special case of the Bayes' filter.

### Problem setup

Setting up the problem goes here.

![Driving a robot towards a wall](/images/random_variable_example.png)

$$
x_k \sim \mathcal{N}(\mu_{x,k}, \sigma_{x,k}^2)
$$

$$
u_k \sim \mathcal{N}(\mu_{u,k}, \sigma_{u,k}^2)
$$

$$
z_k \sim \mathcal{N}(\mu_{z,k}, \sigma_{z,k}^2)
$$

### Assumptions

### The motion model

$$
x_k = x_{k-1} + t u_{k-1}
$$

### The measurement model

$$
z_k = w - x_k
$$

### The Kalman filter

$$
\mu_{x,k} = \mu_{x,k-1} + t\mu_{u,k-1}
$$

$$
\sigma_{x,k}^2 = (\sigma_{x,k-1})(\sigma_{x,k-1}) + (t\sigma_{u,k})(t\sigma_{u,k}) = \sigma_{x,k-1}^2 + t^2\sigma_{u,k}^2
$$

$$
\mu_{z,k} = w - \mu_{x,k}
$$

$$
K_k = \frac{-\sigma_{x,k}^2}{\sigma_{x,k}^2 + \sigma_{z,k}^2}
$$

$$
\mu_{x,k} \gets \mu_{x,k} + K_k\left(z_k - \mu_{z,k}\right)
$$

$$
\sigma_{x,k}^2 \gets (1 + K_k)\sigma_{x,k}^2
$$

### Simulation

<pre>
<code class="julia">

x = 37
\mu = 43

type Neato
x::Int64
y::Float64
end

</code>
</pre>
