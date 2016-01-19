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

The quantity we are trying to estimate ($$x$$ in this case) is commonly referred to as the *state*. As discussed in a [previous post](http://marcgallant.ca/2015/12/16/you-dont-know-where-your-robot-is/), you can never know for sure what $$x$$ is. Instead you use a Gaussian distribution with mean $$\mu_x$$ and variance $$\sigma_x^2$$ to represent $$x$$ as a continuous random variable. Another way to write this is

$$
x \sim \mathcal{N}(\mu_x, \sigma_x^2).
$$

Similarly, you should also represent your joystick commands as a continuous random variable. This is because there are lots of little things that can make the true speed of the robot different from your joystick command (e.g., slightly deflated tires on the robot, resolution of the joystick, etc.). Therefore, the speed of the robot $$u$$ is represented with a Gaussian distribution; i.e.,

$$
u \sim \mathcal{N}(\mu_u, \sigma_u^2).
$$

Finally, your one-dimensional laser scanner should also be represented as a continuous random variable. No sensor is perfect, so we can expect some noise in our measurements of the wall. Therefore, each laser measurement is represented with a Gaussian distribution; i.e.,

$$
z \sim \mathcal{N}(\mu_z, \sigma_z^2).
$$

### Assumptions

- discrete time
- independent measurements
- gaussian distributions appropriate

### The motion model
The *motion model* describes how our state changes over time in response to inputs. In our case, it describes what happens to the position of the robot when you apply joystick commands. Given the position at the previous time step $$x_{k-1}$$ and the current velocity input by the joystick $$u_k$$, the new position of the robot $$x_k$$ is

$$
x_k = x_{k-1} + t u_k,
$$

where $$t$$ is length of the time step. For example, if the position of the robot is $$0.43$$ m and you command the robot to go $$0.5$$ m/s for $$0.1$$ s, then the new position of the robot is

$$
0.43 + (0.1)(0.5) = 0.48 \text{ m}.
$$

Note, however, that $$x_k$$, $$x_{k-1}$$, and $$u_k$$ are random variables. We will address how to calculate the variance of $$x_k$$ given the variances of $$x_{k-1}$$, and $$u_k$$ later; however, would you expect the variance to increase or decrease? If you think about it, by moving the robot forward with a noisy joystick command, we are "adding" together two sources of uncertainty: the uncertainty in our previous position, and the uncertainty associated with the noise in our joystick command. Therefore, the variance of $$x_k$$ should *increase*. If you were to repeatedly apply the motion model to new joystick commands, the resulting estimation of the robot's position over time is called *dead reckoning*, and is doomed to become more and more uncertain the longer you do it.

#### Motion model coefficients

The Kalman filter requires two terms that are part of the motion model. The first is $$a_k$$, which describes how you would expect $$x_k$$ to change in response to changes in $$x_{k-1}$$, which can be calculated by taking the partial derivative of the motion model with respect to $$x_{k-1}$$; i.e.,

$$
a_k = \frac{\partial x_k}{\partial x_{k-1}} = 1.
$$

In other words, a change in $$x_{k-1}$$ by some value $$\Delta x$$ would result in a change in $$x_k$$ by $$(1)(\Delta x)$$. For example, let's say I increased $$x_{k-1}$$ in the previous example by $$0.2$$ m (i.e., $$0.43 + 0.2 = 0.63$$ m). Then the new $$x_k$$ is $$ 0.63 + (0.1)(0.5) = 0.68 \text{ m}$$, which is $$0.2$$ m greater than the $$x_k$$ in the previous example, as expected. Similarly, we require $$b_k$$, which describes how you would expect $$x_k$$ to change in response to changes in $$u_k$$; i.e.,

$$
b_k = \frac{\partial x_k}{\partial u_k} = t.
$$

For example, if I decreased $$u_k$$ in the original example by $$0.1$$ m/s (i.e., $$0.5 - 0.1 = 0.4$$ m/s), the new $$x_k$$ is $$ 0.43 + (0.1)(0.4) = 0.47 \text{ m} $$, which is $$t(0.1) = (0.1)(0.1) = 0.01$$ m less than the original position, as expected.

Did you notice anything special about the values of $$a_k$$ and $$b_k$$? Maybe you noticed that the motion model has the following form:

$$
x_k = a_k x_{k-1} + b_k u_k.
$$

This is always the case when the motion model is *linear*, which was one of our assumptions. When the motion model is linear, the expressions for $$a_k$$ and $$b_k$$ do not contain the state or the input. Furthermore, consider the role of $$a_k$$ and $$b_k$$. The $$a_k$$ term converts a state in the past to a state in the present in the absence of inputs (in our case, the position of the robot doesn't change if there are no inputs, therefore $$a_k = 1$$ makes sense), and the $$b_k$$ terms converts an input to a change in state (in our case, velocity is converted into a change in position through numerical integration by multiplying by $$t$$, therefore $$b_k = t$$ makes sense). As a result, note that $$a_k$$ is unitless and $$b_k$$ has units of seconds.

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
