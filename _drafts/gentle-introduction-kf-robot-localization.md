---
layout: post
title:  A gentle introduction to the Kalman filter
comments: true
date:   2016-01-12
---

Introductory paragraph will go here. Remember to write disclaimer saying that it's to get an intuitive understanding, not technically rigourous with proofs. Maybe talk about how it's a special case of the Bayes' filter.

### Prerequisities

### Problem setup

The figure below illustrates the scenario for which a KF will be implemented. We will be estimating the position of a one-dimensional robot as it drives toward a wall. 

![Driving a robot towards a wall](/images/random_variable_example.png)

The robot begins at the "Start" on the far left. Before starting the experiment, you measure the distance between "Start" and the wall. You equip the robot with a one-dimensional laser scanner that measures the distance between the robot and the wall ten times per second. 

Now imagine you are holding a joystick with which you can command the robot to go forward or backward at any practical speed. You start by placing the robot close to "Start" and start driving the robot towards the wall. Using all of this information, you want to estimate how far you've driven. In other words, you want to estimate $$x$$ given

- your joystick commands $$u$$;
- the laser measurements $$z$$;
- the known position of the wall $$w$$; and
- the initial position of the robot $$x_0$$.

As discussed in a [previous post](http://marcgallant.ca/2015/12/16/you-dont-know-where-your-robot-is/), you can never know for sure what $$x$$ is. Instead you use a Gaussian distribution with mean $$\mu_x$$ and variance $$\sigma_x^2$$ to represent $$x$$ as a continuous random variable. Another way to write this is

$$
x \sim \mathcal{N}(\mu_x, \sigma_x^2).
$$

Similarly, you should also represent your joystick commands as a continuous random variable. This is because there are lots of little things that can make the true speed of the robot different from your joystick command (e.g., slightly deflated tires on the robot, resolution of the joystick, etc.). Therefore, the speed of the robot $$u$$ is represented as a Gaussian random variable; i.e.,

$$
u \sim \mathcal{N}(\mu_u, \sigma_u^2)
$$

$$
z \sim \mathcal{N}(\mu_z, \sigma_z^2)
$$

### Assumptions

### The motion model

$$
x_k = x_{k-1} + t u_k
$$

$$
a_k = \frac{\partial x_k}{\partial x_{k-1}} = 1
$$

$$
b_k = \frac{\partial x_k}{\partial u_k} = t
$$

### The measurement model

$$
z_k = w - x_k
$$

$$
c_k = \frac{\partial z_k}{\partial x_k} = -1
$$

### The Kalman filter

$$
\begin{align}
\mu_{x,k} &= a_k\mu_{x,k-1} + b_k\mu_{u,k} \\
&= \mu_{x,k-1} + t\mu_{u,k}
\end{align}
$$

$$
\begin{align}
\sigma_{x,k}^2 &= a_k^2\sigma_{x,k-1}^2 + b_k^2\sigma_{u,k}^2 \\
&= \sigma_{x,k-1}^2 + t^2\sigma_{u,k}^2
\end{align}
$$

$$
\mu_{z,k} = w - \mu_{x,k}
$$

$$
\begin{align}
K_k &= c_k\frac{\sigma_{x,k}^2}{c_k^2\sigma_{x,k}^2 + \sigma_{z,k}^2} \\
&= -\frac{\sigma_{x,k}^2}{\sigma_{x,k}^2 + \sigma_{z,k}^2} \\
\end{align}
$$

$$
\mu_{x,k} \gets \mu_{x,k} + K_k\left(z_k - \mu_{z,k}\right)
$$

$$
\sigma_{x,k}^2 \gets (1 + K_k)\sigma_{x,k}^2
$$

### Simulation

<pre>
<code class="julia">julia> κ = 0
module Directionals

import Base: +, -, ==, angle, inv, log, mean, show, getindex

export UnitAxis, UnitDirection, ⊞, ⊟, axis, covariance, dist, vector

const EPS = 1e-9

####################################################################################################
# Type Definitions
####################################################################################################

abstract Directional

immutable UnitAxis <: Directional
    κ::Vector{Float64}
    λ::Float64

    function UnitAxis(κ, λ) 
        length(κ) == 2 || error("Must be a 2-vector.")
        κ_norm, λ_norm = normalize(κ, λ)
        λ_norm >= zero(λ_norm) ? new(κ_norm, λ_norm) : new(-κ_norm, -λ_norm)
    end
end

immutable UnitDirection <: Directional
    κ::Vector{Float64}
    λ::Float64

    function UnitDirection(κ, λ) 
        length(κ) == 2 || error("Must be a 2-vector.")
        κ_norm, λ_norm = normalize(κ, λ)
        new(κ_norm, λ_norm)
    end
end
</code></pre>
