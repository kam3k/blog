---
layout: post
title: A gentle introduction to robot localization with a Kalman filter
comments: true
date:   2016-01-28
---

I've come across various instances of people asking for an intuitive introduction to the Kalman filter in the context of robotics. These people are often hobbyists, undergraduate students, or keen high school students trying to get their robot to properly combine various sensor information. I've even written some answers on the [Robotics Stack Exchange](http://robotics.stackexchange.com) helping people with various localization and mapping problems. These people are often referred to great references (e.g., [Probabilistic Robots](http://www.probabilistic-robotics.org)), but many give up in the first few chapters because of a lack of grasping what is really going on, or trouble with why something works. To this end, this post shows how a very basic Kalman filter works using a bottom-up approach. I use a simple one-dimensional robot to really try to get across *why* this fancy algorithm has been so popular over the years.

I should point out that this is not a mathematically rigourous treatment of the Kalman filter. I'll leave that to the textbooks. What I hope to accomplish here is a basic understanding of the fundamentals, and to leave the reader with an appreciation of the usefulness of this beautiful algorithm.

## Prerequisities

## Problem setup

The problem we are trying to solve is illustrated below. We have a robot that can drive forward towards a wall given your joystick commands $$u$$ (e.g., $$u = 2.3$$ m/s). The robot is equipped with a sensor capable of measuring the distance $$z$$ to the wall (e.g., $$z = 8.31$$ m), and know the position of the wall $$w$$ relative to the start (e.g., $$w = 10.0$$ m). You place the robot near the start and command it to start moving forward. Given all this information, you are interested in estimating the position of the robot $$x$$. 

![Driving a robot towards a wall](/images/random_variable_example.png)

How do you combine all of this information to estimate $$x$$? This is where the Kalman filter comes in. It combines

- your joystick commands $$u$$;
- the laser measurements $$z$$;
- the known position of the wall $$w$$; and
- the initial position of the robot $$x_0$$

to come up with an estimate of $$x$$. The quantity we are trying to estimate ($$x$$ in this case) is commonly referred to as the *state*. As discussed in a [previous post](http://marcgallant.ca/2015/12/16/you-dont-know-where-your-robot-is/), you can never know for sure what $$x$$ is. Instead you use a Gaussian distribution with mean $$\mu_x$$ and variance $$\sigma_x^2$$ to represent $$x$$ as a continuous random variable. Another way to write this is

$$
x \sim \mathcal{N}(\mu_x, \sigma_x^2).
$$

Similarly, you should also represent your joystick commands as a continuous random variable because there are lots of little things that can make the true speed of the robot different from your joystick command (e.g., slightly deflated tires on the robot, resolution of the joystick, etc.). Therefore, the speed of the robot $$u$$ is represented with a Gaussian distribution; i.e.,

$$
u \sim \mathcal{N}(\mu_u, \sigma_u^2).
$$

Finally, your sensor measurements should also be represented as a continuous random variable. No sensor is perfect, so we can expect some noise in our measurements of the wall. Therefore, each laser measurement is represented with a Gaussian distribution; i.e.,

$$
z \sim \mathcal{N}(\mu_z, \sigma_z^2).
$$

## Assumptions
Before we continue, I should note that the following Kalman filter makes a couple (reasonable) assumptions. 

1. All measurements are *independent*. In other words, previous measurements have no effect whatsoever on future measurements. For example, if your sensor measures $$z=8.45$$ m, this does not influence the next value of $$z$$. 

2. Gaussian distributions are a good representation of $$x$$, $$u$$, and $$z$$. For example, if our robot was standing still and our sensor took thousands of measurements, we'd expect those measurements to be normally distributed. This is usually a fair assumption because the [central limit theorem](https://en.wikipedia.org/wiki/Central_limit_theorem).

## Our strategy for estimating $$x$$
Before getting into the mathematical details, I'm going to discuss the general strategy of how we are going to proceed. First, we're going to say our initial estimate of $$x$$ is the location at which (we think) the robot starts. Let's say there is a "starting line" drawn on the ground at $$x=0$$ where we place our robot. So at this point we have (for example)

$$
\mu_{x,0} = 0 \text{ m}, \quad \sigma_{x,0}^2 = 0.05^2 \text{ m}^2.
$$

Note that we are not sure if we started the robot at *exactly* $$x=0$$ m, so we say our mean is zero with some initial variance. Now we apply a joystick command to start driving forward. Estimating $$x$$ now depends on combining two pieces of information: our commanded speed and our sensor measurements. We combine these by repeatedly performing the following two steps:

1. *Predict* the new position of the robot by integrating the speed we commanded with the joystick. Think of it this way: if the robot was at $$x=8.1$$ m and we commanded it to go $$0.3$$ m/s for one second, a good prediction of where the robot is now would be $$x=8.4$$ m.

2. *Correct* our prediction with a new measurement by the sensor. Let's say our prediction was $$x = 8.4$$ m, and we know the wall is $$10$$ m from the start. Now we take a measurement with our sensor, and we get (for example) $$z = 1.67$$ m. Well given that our wall is at $$w = 10$$ m, a measurement of $$z = 1.67$$ m implies that we are at $$x = 10 - 1.67 = 8.33$$ m, which is different from our prediction. So which value do we use? The answer is *both*. We combine the two estimates, using their respective uncertainties to determine how much we "believe" one versus the other.

The following couple sections go into the details of these two steps.

## Prediction
The prediction uses a *motion model* to predict the new state based on new inputs. In our case, it describes what happens to the position of the robot when you apply joystick commands. Given the position at the previous time step $$x_{k-1}$$ and the current velocity input by the joystick $$u_k$$, the predicted position of the robot $$x_k$$ is

$$
x_k = x_{k-1} + t u_k,
$$

where $$t$$ is length of the time step. Note, however, that $$x_k$$, $$x_{k-1}$$, and $$u_k$$ are random variables. Here, we take advantage of a couple important properties of Gaussian random variables:

1. Given two Gaussian random variables $$a\sim\mathcal{N}(\mu_a,\sigma^2_a)$$ and $$b\sim\mathcal{N}(\mu_b,\sigma^2_b)$$, their sum $$c = a + b$$ is also a Gaussian random variable, where $$c\sim\mathcal{N}(\mu_a + \mu_b,\sigma^2_a + \sigma^2_b)$$.

2. Given a Gaussian random variable $$a\sim\mathcal{N}(\mu_a,\sigma^2_a)$$, multiplying it by a scalar $$b = na$$ results in the Gaussian random variable $$b\sim\mathcal{N}(n\mu_a, n^2\sigma^2_a)$$.

In other words, if you apply a *linear* operation to a Gaussian random variable, the result is also a Gaussian random variable. Keeping this in mind, let's look at how we properly update our position estimate when we perform a prediction using the motion model:

$$
\begin{align}
\mu_{x,k} &= \mu_{x,k-1} + t \mu_{u,k} \\
\sigma^2_{x,k} &= \sigma^2_{x,k-1} + t^2\sigma^2_{u,k}.
\end{align}
$$

So it turns out updating our estimate of $$x$$ in the prediction step is pretty straightforward precisely because our motion model is linear. When this is not the case, we *cannot* use a regular Kalman filter (this is commonly dealt with by using the extended Kalman filter (EKF) or unscented Kalman filter (UKF), but that is beyond the scope of this post).

An important result of the prediction step is that the variance of our estimate of $$x$$ has *increased*. It is the old variance plus some additional uncertainty caused by our noisy motion command. Intuitively this makes sense; we applied a noisy motion command so naturally we are less certain about where the robot is. Let's look at an example of PDFs of our estimate of $$x$$ before and after an application of the prediction step (see [this previous post](http://marcgallant.ca/2015/12/16/you-dont-know-where-your-robot-is/) for a review of PDFs):

![PDFs illustrating the prediction step of the Kalman filter](/images/kf_predict.png)

The above example illustrates the two things the prediction does: it moves our estimate forward and increases the variance. You can imagine what would happen if we didn't have sensor to perform a correction step: the best we could do is just repeatedly perform predictions using our joystick commands. As a result, we would keep moving the estimate forward, but it would get more and more uncertain over time. This is called *dead reckoning*, and is usually only a suitable form of estimation over short distances.

## Correction

## Putting it all together

<!---
## The motion model
The *motion model* describes how our state changes over time in response to inputs. In our case, it describes what happens to the position of the robot when you apply joystick commands. Given the position at the previous time step $$x_{k-1}$$ and the current velocity input by the joystick $$u_k$$, the new position of the robot $$x_k$$ is

$$
x_k = x_{k-1} + t u_k,
$$

where $$t$$ is length of the time step. For example, if the position of the robot is $$0.43$$ m and you command the robot to go $$0.5$$ m/s for $$0.1$$ s, then the new position of the robot is

$$
0.43 + (0.1)(0.5) = 0.48 \text{ m}.
$$

Note, however, that $$x_k$$, $$x_{k-1}$$, and $$u_k$$ are random variables. We will address how to calculate the variance of $$x_k$$ given the variances of $$x_{k-1}$$, and $$u_k$$ later; however, would you expect the variance to increase or decrease? If you think about it, by moving the robot forward with a noisy joystick command, we are "adding" together two sources of uncertainty: the uncertainty in our previous position, and the uncertainty associated with the noise in our joystick command. Therefore, the variance of $$x_k$$ should *increase*. If you were to repeatedly apply the motion model to new joystick commands, the resulting estimation of the robot's position over time is called *dead reckoning*, and is doomed to become more and more uncertain the longer you do it.

### Motion model coefficients

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

## The measurement model

$$
z_k = w - x_k
$$

$$
c_k = \frac{\partial z_k}{\partial x_k} = -1
$$

## The Kalman filter

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

-->

## Simulation

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
