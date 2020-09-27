---
layout: post
title: A gentle introduction to the Kalman filter
comments: false
date:   2016-01-28
---

I've come across various instances of people asking for an intuitive introduction to the Kalman filter, often in the context of robotics. These people are often hobbyists, undergraduate students, or keen high school students trying to get their robot to properly combine data from various sensors. I've even written some answers on the [Robotics Stack Exchange](http://robotics.stackexchange.com) helping people with various localization and mapping problems. These people are often referred to great references (e.g., [Probabilistic Robots](http://www.probabilistic-robotics.org)), but many give up in the first few chapters because of a lack of grasping what is really going on, or trouble with why something works. To this end, this post shows how a very basic Kalman filter works using a bottom-up approach. I use a simple one-dimensional robot to really try to get across *why* this fancy algorithm has been so popular over the years.

I should point out that this is not a mathematically rigourous treatment of the Kalman filter. I'll leave that to the textbooks. What I hope to accomplish here is a basic understanding of the fundamentals, and to leave the reader with an appreciation of the usefulness of this beautiful algorithm.

## Prerequisities

You understand that in the real world, anything you measure or are estimating is often represented by a random variable. That is, in the field of mobile robotics, [you don't know where your robot is]({% post_url 2015-12-16-you-dont-know-where-your-robot-is %}). It is helpful if you know what a mean and standard deviation are. You should be able to do simple arithmetic (addition, subtraction, multiplication, division) and understand simple equations and how to manipulate them using basic algebra (e.g., "move" $$x$$ to the other side of the equal sign by subtracting it from both sides).

## Problem setup

An in-fashion application of localizing a robot using a Kalman filter is in the development of driverless cars. The car needs to know where in the world it is and how it's oriented with great accuracy so it can safely drive around a city, for example. This is a really complicated problem. There are bicycles, pot holes, pedestrians, hills, speed limits, weather, lighting changes, other vehicles, and so on. The driverless car itself may have laser scanners, GPS, cameras, radar, and wheel encoders among other sensors. Although localizing a driverless car can be solved with a Kalman filter, it is much too involved for an introduction like this one. So we're going to greatly simplify the problem but keep the same approach: combining sensor data and information about the world to localize a robot.

The simplified problem we will try to solve is illustrated below. We have a robot that can drive forward towards a wall. This wall is a landmark in the environment with a known location, similar to how a driverless car may use a pre-constructed map of buildings and other objects to help it navigate. Since we are focusing on estimating where the robot is (localization problem) and not how we should drive it (control problem), let's pretend you are standing somewhere with a joystick that lets you adjust the speed of the robot. The robot has a sensor that gives you a noisy measurement of how far it is from the wall. As you drive it, you want to estimate how far your robot has travelled; that is, its current position relative to the start. More formally, you are trying to estimate the *state* $$x$$ (the position of the robot) given

- the *command* $$u$$ (your joystick command);
- the *map* $$w$$ (your prior knowledge of the environment, the position of the wall);
- the *measurement* $$z$$ (the sensor measurement of the environment); and
- the *initial state* $$x_0$$ (the initial position of the robot).

![Driving a robot towards a wall](/images/random_variable_example.png)

## Why use a Kalman filter?

Maybe at this point you're thinking, why do I need a Kalman filter here? This problem is easy! If you know where the wall is (e.g., $$w=10$$ m) and you have a sensor that can measure the current position of the wall (e.g., $$z=3$$ m), then we can just directly calculate the position of the robot (e.g., $$x=(10\text{ m})-(3\text{ m})=7\text{ m }$$). Sure, but consider the situation where your sensor has a lot of noise, and perhaps can only measure the position of the wall with a standard deviation of $$1$$ metre. Then the best you can do (assuming your knowledge of the wall's position is perfect) is limited by the noise in the sensor.

But wait! If you are setting the speed of the robot with the joystick, you can just time how long it has been driving, then its position is the product of its speed and the elapsed time (i.e., $$x=ut$$ for elapsed time $$t$$). For example, if you've commanded the robot to go $$2$$ metres per second for $$5$$ seconds, its position is $$(2\text{ m/s})(5\text{ s})=10\text{ m}$$. Unfortunately, here I come again to burst your bubble, but who said that the robot goes at exactly the speed you commanded it? Any imperfection in the robot (e.g., slightly flat tires), joystick (e.g., somebody ate cheetos before using it and it sticks a bit), or your timer (I hope you weren't just using a stopwatch) and your estimate is wrong. Not only wrong, but it gets worse over time. If the robot was actually driving at $$2.1$$ metres per second, after $$5$$ seconds you're off by at least $$0.5$$ metres. And after $$20$$ seconds, it's $$2$$ metres, and so on.

And now we've arrived at brilliant idea number three. You combine the two approaches above. You notice that over short distances, the speed and timer approach is pretty accurate, but gets worse over time. On the other hand, the sensor measuring the wall approach is the same at any time, but isn't too accurate. So how to you combine these? Maybe at some set interval (e.g., every second), you estimate how far the robot has driven with the timer and joystick command, and you also take a measurement of the wall with your sensor. Now you have two estimates of the robot's position, so which do you use? You could take an average, but shouldn't you consider how much noise each method has? So maybe you take some sort of weighted average. And now you've invented the Kalman filter.

---
**Key point**: a Kalman filter combines your current knowledge of the state (and its uncertainty) with the most recent command (and its uncertainty) and measurement (and its uncertainty) to calculate a new estimate of the state that minimizes the state's new uncertainty. It does this by calculating a weight (called the Kalman gain) that is proportional to ratios of the uncertainties of the previous state, the command, and the measurement.

---

Going even further, if all the uncertain elements (state, command, measurement) can be represented perfectly by Gaussian random variables (more on this below), and the calculation of new states from the command and measurements uses only linear equations (more on this below, too), then the Kalman filter is the best possible estimate you can come up with. That is, it has been proven that no other method in combining the information can give you a more accurate estimate of the state.

## Gaussian random variables

As was eluded to earlier, the state, commands, measurements, map, and initial state of the robot all have uncertainty. To model this uncertainty, we're going to represent each quantity as a *Gaussian random variable*. For the high-level understanding we're going for in this tutorial, it's enough to think of Gaussian random variables as a mean and variance, where the variance is the squared standard deviation. 

For example, suppose we read the manual that came with the sensor and it says it measures the distance to things with a standard deviation of $$0.5\text{ m}$$. For Gaussian random variables, this means that

- About 68% of the time, the true distance to the wall is within $$\pm 0.5\text{ m}$$ (one standard deviation) what the sensor measures
- About 95% of the time, the true distance to the wall is within $$\pm 1.0\text{ m}$$ (two standard deviations) what the sensor measures
- About 99.7% of the time, the true distance to the wall is within $$\pm 1.5\text{ m}$$ (three standard deviations) what the sensor measures

So, for example, when the sensor says the wall is $$10\text{ m}$$ away, you are 99.7% sure the true distance to the wall is between $$8.5\text{ m}$$ and $$11.5\text{ m}$$ away. 

A common notation to say that something is being represented by a Gaussian random variable is

$$
z \sim \mathcal{N}(\mu_z, \sigma_z^2).
$$

which is another way of saying $$z$$ (the measurement in our case) is a Gaussian random variable with mean $$\mu_z$$ (the true distance to the wall) and variance $$\sigma_z^2$$ (the noise of the sensor). In plain English, that's "when we take a measurement with our sensor, it is going to give use the true distance to the wall plus or minus some noise", where the noise is represented by the variance (the squared standard devation). As mentioned above, the noise (and therefore the variance) can be obtained from the sensor's manual, which is $$\sigma_z^2=(0.5\text{ m})^2=0.25\text{ m}^2$$.

In the same vein, the state, commands, map, and initial state will also be represented by Gaussian random variables. To summarize,

- $$x \sim \mathcal{N}(\mu_x, \sigma_x^2)$$, or "we estimate our robot to be within its true position plus or minus some uncertainty"
- $$u \sim \mathcal{N}(\mu_u, \sigma_u^2)$$, or "the speed we command the robot to go is the true speed of the robot plus or minus some noise"
- $$z \sim \mathcal{N}(\mu_z, \sigma_z^2)$$, or "the sensor measures the true distance to the wall, plus or minus some noise"
- $$w \sim \mathcal{N}(\mu_w, \sigma_w^2)$$, or "where we think the wall is in the environment is the true position of the wall plus or minus some uncertainty"
- $$x_0 \sim \mathcal{N}(\mu_{x_0}, \sigma_{x_0}^2)$$, or "when we put the robot at the start line, we put it exactly at the start line plus or minus some uncertainty"

The role of the Kalman filter is to estimate the state $$x$$ given the commands $$u$$, measurements $$z$$, the map $$w$$, and the initial state $$x_0$$. For these latter Gaussian random variables, it's not uncommon to have a good guess at their variances ahead of time. For this tutorial, we'll use the variances

- $$\sigma_u^2=0.04\text{ m}^2/\text{s}^2$$ (i.e., the joystick commands have a standard deviation of $$0.2\text{ m/s}$$),
- $$\sigma_z^2=0.49\text{ m}^2$$ (i.e., the sensor measurements have a standard deviation of $$0.2\text{ m}$$),
- $$\sigma_w^2=0.01\text{ m}^2$$ (i.e., the position of the wall on the map has a standard deviation of $$0.1\text{ m}$$),
- $$\sigma_{x_0}^2=0.09\text{ m}^2$$ (i.e., the initial position of the robot has a standard deviation of $$0.3\text{ m}$$),

Note that in some Kalman filter implementations, the variances $$\sigma_u^2$$ and $$\sigma_z^2$$ can change over time. For example, perhaps your joystick gets more uncertain the faster you go, or as it loses battery power. Similarly, perhaps the sensor is less accurate at farther distances.


## Discrete time

Although not strictly necessary when using a Kalman filter, we are going to use discrete time, where we update our command and then take a measurement at every timestep. For simplicity, we're going to make this timestep equal to one second. Put differently, we're going to estimate $$x$$ once per second using the velocity $$u$$ we commanded at the start of that second and the measurement $$z$$ we took at the end of that second. 

It is common to use the subscript $$k$$ to denote the timestep you're talking about. That is, if your timestep is $$0.5\text{ s}$$ long, then $$k=1$$ is at $$t=0.5\text{ s}$$, $$k=2$$ is at $$t=1.0\text{ s}$$ and so on. In our case, the timestep is one second long, so $$k$$ actually matches the number of seconds. To summarize, we are going to estimate $$x_k$$ (the position of the robot at the end of timestep $$k$$) using $$u_{k-1}$$ (the command we sent at the start of timestep $$k$$, or equivalently, the end of timestep $$k-1$$) and $$z_k$$ (the sensor measurement we took at timestep $$k$$). 

Note that $$w$$ is the same for all $$k$$ (that is, $$w_k$$ is always equal to $$w_{k-1}$$ because the wall does not move) so we'll omit its subscript. Also note that you can now see why I wrote the initial position as $$x_0$$, which is the position $$x_k$$ when $$k=0$$.

## The Kalman filter 

Now on to the main event! The Kalman fitler is made up of two steps that are executed at each timestep. The first is called the *prediction step*, which incorporates the command $$u_{k-1}$$ (that is, the command at the start of the timestep or the end of the previous timestep). In our example, this step *predicts* the robot position $$x_k$$ by incorporating the speed commanded by the joystick over the length of the timestep.

The second step is called the *correction step*, which incorporates the measurement $$z_k$$ (that is, the sensor measurement at the end of the timestep). In our example, this step *corrects* the predicted robot position by incorporating the sensor's measurement of the position of the wall.

### The prediction step

The prediction step of the Kalman filter is where we estimate the position of the robot using the command. So get out the joystick and your stopwatch, its time to predict where the robot will be ($$x_k$$) after we've given our joystick command ($$u_{k-1}$$) and it has driven for the timestep of one second. This should be pretty straightforward. We predict the robot to be where it was when the timestep started ($$x_{k-1}$$) plus the speed the robot was driving ($$u_{k-1}$$) times how long it drove ($$\Delta t$$). That is,

$$
x_k = x_{k-1} + u_{k-1}\Delta t.
$$

Let's put some numbers into this equation. Suppose we estimated our initial position of the robot to be at zero metres ($$x_0=0\text{ m}$$), and we commanded the robot to drive at two metres per second ($$u_{k-1}=2\text{ m/s}$$) for one second ($$\Delta t=1\text{ s}$$). Then our new estimated position of the robot ($$x_1$$) is

$$
x_1 = 0\text{ m} + (2\text{ m/s})(1\text{ s}) = 2\text{ m}.
$$

Now let's say we commanded the same velocity for the next timestep. Then,

$$
x_2 = 2\text{ m} + (2\text{ m/s})(1\text{ s}) = 4\text{ m}.
$$

Super easy, right? It sounds like we're done, but we've forgotten something important. Remember, all of these variables ($$x_k$$, $$x_0$$, $$u_{k-1}$$) are Gaussian random variables with variances. As we discussed above, we already have values for the variances of everything except for $$x_k$$. So we need to figure out, for example, what is the variance of $$x_1$$? Of $$x_2$$? 

Look again at the equation above we used to calculate $$x_k$$. The first thing we need to understand is, what happens when we multiply a Gaussian random variable (in this case $$u_{k-1}$$) by a regular number (in this case $$\Delta t$$). Put differently, if we have 

$$
u \sim \mathcal{N}(\mu_u, \sigma_u^2),
$$

how does multiplying $$u$$ by $$\Delta t$$ affect the mean and variance? Fortunately, for Gaussian random variables, this is very straightforward. 

---
**Multiplying a Gaussian random variable by a scalar (regular number)**: Given a Gaussian random variable $$a\sim\mathcal{N}(\mu_a,\sigma^2_a)$$, multiplying it by a scalar $$s$$ results in the Gaussian random variable $$as\sim\mathcal{N}(\mu_as, \sigma^2_as^2)$$.

---

So it turns out $$u_{k-1}\Delta t$$ is itself a Gaussian random variable with variance $$\sigma_u^2\Delta t^2$$. Great! We're almost there. Returning to our original problem, remember we are trying to figure out the variance of $$x_k$$, where

$$
x_k = x_{k-1} + u_{k-1}\Delta t.
$$

We just figured out that the second term in the sum is a Gaussian random variable and we know its variance. Now we need to figure out what happens when we add two Gaussian random variables together (in our case $$x_{k-1} + u_{k-1}\Delta t$$). Again, this is fortunately very straightforward for Gaussian random variables.

---
**Adding two Gaussian random variables together**: Given two Gaussian random variables $$a\sim\mathcal{N}(\mu_a,\sigma^2_a)$$ and $$b\sim\mathcal{N}(\mu_b,\sigma^2_b)$$, their sum $$a + b$$ is also a Gaussian random variable, where $$(a+b)\sim\mathcal{N}(\mu_a + \mu_b,\sigma^2_a + \sigma^2_b)$$.

---

Ah, quite straightforward. It turns out $$x_k$$ is a Gaussian random variable, and its variance is just the sum of the variances of $$x_{k-1}$$ and $$u_{k-1}\Delta t$$. When $$k=1$$ (i.e., the first timestep), this means that

$$
\sigma_{x_1}^2 = \sigma_{x_0}^2 + \sigma_{u_0}^2\Delta t^2
$$

Recall that $$\sigma_{x_0}^2$$ is just the variance of the initial position, which we know beforehand is $$0.09\text{ m}^2$$. Similarly, $$\sigma_{u_0}^2$$ is just the variance of our joystick command, which we also know beforehand is $$0.04\text{ m}^2/\text{s}^2$$. And finally, we said the length of our timestep is $$\Delta t=1\text{ s}$$. Putting this all together and we get

$$
\sigma_{x_1}^2 = 0.09\text{ m}^2 + \left(0.04\text{ m}^2/\text{s}^2\right)\left(1\text{ s}\right)^2 = 0.13\text{ m}^2
$$

And how do we calculate the variance of the robot's position at the next timestep (i.e., at $$k=2$$)? Well, we just bump up $$k$$ in the variance equation above, that is

$$
\sigma_{x_2}^2 = \sigma_{x_1}^2 + \sigma_{u_1}^2\Delta t^2
$$

and since we just calculated $$\sigma_{x_1}^2=0.13\text{ m}^2$$, we have all the terms on the right hand side. So,

$$
\sigma_{x_2}^2 = 0.13\text{ m}^2 + \left(0.04\text{ m}^2/\text{s}^2\right)\left(1\text{ s}\right)^2 = 0.17\text{ m}^2.
$$

Perhaps you're starting to see a pattern here? If we just continue to estimate the robot's position purely by using the velocity commanded by the joystick, the variance in our estimate in our robot's position will increase at every timestep. That is, we become less and less certain where our robot is over time. Imagine doing this for a long, long time. At some point, you will have very little confidence in the robot's position. When all seems hopeless and you're completely lost, you suddenly see the wall. We're saved! You measure it with your sensor and *correct* your position since the uncertainty of your sensor measurement is much smaller than all the uncertainty you've accumulated.

---
**Key point**: The prediction step of a Kalman filter predicts what the state will be at the end of the current timestep. It also estimates the variance of the state, which will always *increase* relative to the previous timestep.

---

Writing this reminded me of a time when I was kid and slept over at my new friend's house. We slept in the basement, and I remember needing to get up to go to the washroom in the middle of the night. It was pitch dark and I was unfamiliar with the layout of the room. I remember carefully feeling my way around until I was hopelessly lost. I had literally had no idea where I was when suddenly *ouch* I kicked the bottom stair and knew exactly where I was. Every step of my pitiful navigation in the dark was increasing the uncertainty of my position until I measured the known position of something in the environment, at which point my uncertainty drastically decreased. At its core, this is what a Kalman filter does, putting numbers to all these things and calculating the best estimate of the state and its variance given the information available. We'll see how we calculate the state and its variance after the measurement of the environment in the next section.

### The correction step

The correction step of the Kalman filter is where we estimate the position of the robot using the sensor and merge it with the estimate we got from the command in the prediction step. Recall from the prediction step that after one timestep ($$k=1$$), we had

$$
x_1 = 2\text{ m}, \quad \sigma_{x_1}^2=0.13\text{ m}^2.
$$

Now suppose the position of the wall is at $$w=10\text{ m}$$, with $$\sigma_w^2=0.01\text{ m}^2$$ as we stated above. So we activate our trusty (but noisy) sensor and measure the position of the wall from our current estimated position $$x_1$$ and we get $$z_1=8.5\text{  m}$$. Well we know the wall is about $$10\text{ m}$$ away from the start, and now we've measured it to be $$8.5\text{ m}$$ away, so our sensor is telling us the robot's position is $$10-8.5=1.5\text{ m}$$. More generally, the sensor says that

$$
x_k = w - z_k.
$$

And what about the variance of the sensor's estimate of $$x_k$$? Well, recall from above that when you add two Gaussian random variables together, the resulting variance is the sum of variances (and also note that subtraction is just addition by a negative number). And once again, we know the variances of the two Gaussian random variables on the right hand side of this equation. The first is the uncertainty in the position of the wall ($$0.01\text{ m}^2$$), and the second is the noise in the sensor measurement ($$0.49\text{ m}^2$$). So according to the sensor,

$$
x_1 = 1.5\text{ m}, \quad \sigma_{x_1}^2=0.01\text{ m}^2 + 0.49\text{ m}^2 = 0.50\text{ m}^2
$$

To summarize, we have two competing estimates of the current position of the robot. One from the command, and one from the sensor. As you may have guessed, the correction step of the Kalman filter calculates a weighted averge of these two estimates, using their variances as their weights. This means that the result of the correction step will give an estimate somewhere between the command's prediction and the sensor's measurement. One way to formulate this is

$$
x_1 = x_{1,\text{command}} + K\left(x_{1,\text{sensor}} - x_{1,\text{command}}\right),
$$

where $$K$$ is some number between $$0$$ and $$1$$. Let's think about some hypothetical values of $$K$$ to convince ourselves that this makes sense. First, imagine $$K=0$$, which would simplify the equation to

$$
x_1 = x_{1,\text{command}}.
$$

In other words, $$K=0$$ means we believe the command completely and ignore the sensor. Conversely, imagine $$K=1$$, which would give us

$$
x_1 = x_{1,\text{sensor}}.
$$

In other words, $$K=1$$ means we believe the sensor completely and ignore the command. Finally, substituting $$K=0.5$$ gives us

$$
x_1 = x_{1,\text{command}} + 0.5\left(x_{1,\text{sensor}} - x_{1,\text{command}}\right),
$$

which essentially moves the command estimate halfway towards the sensor measurement. That is, it's the exact average of the two estimates. Hopefully these three examples convince you that all that's left to do is calculate the appropriate value for $$K$$.

So what is a good value for $$K$$ in our example? Well, recall we want $$K$$ to be close to zero to indicate "screw the sensor, let's just believe the commands". Well a good time to do that would be when the command noise is close to zero; that is, your joystick commands are close to the true speed of the robot. On the other hand, we want $$K$$ to be close to one when the opposite is true; that is, our commands are nowhere near the true speed of the robot. An equation for $$K$$ that handles both of these cases is

$$
K = \frac{\sigma_{x_1,\text{command}}^2}{\sigma_{x_1,\text{command}}^2 + \sigma_{x_1,\text{sensor}}^2}.
$$

Try imagining the case where the command uncertainty is way smaller than the sensor uncertainty (i.e., $$\sigma_{x_1,\text{command}}^2 \ll \sigma_{x_1,\text{sensor}}^2$$) and you'll see that $$K$$ approaches zero, as desired. Similarly, imagining the case where command uncertainty is way larger than the sensor uncertainty (i.e., $$\sigma_{x_1,\text{command}}^2 \gg \sigma_{x_1,\text{sensor}}^2$$) produces a $$K$$ that approaches one.

Substituting our values for the variances lets us calculate $$K$$ for this timestep. We get

$$
K_1 = \frac{0.13\text{ m}^2}{0.13\text{ m}^2 + 0.50\text{ m}^2} \approx 0.206,
$$

giving us the corrected estimate of the robot's position at $$k=1$$ of

$$
x_1 =  2.0\text{ m} + 0.206\left(1.5\text{ m} - 2.0\text{ m}\right) \approx 1.90\text{ m}.
$$

I think you'll agree this makes a lot of sense. The estimate moved a small amount towards the sensor estimate from the command estimate (about 21% of the way there) because the command's uncertainty was smaller. It's important to note that this new estimate is *better* than each individual estimate, which we'll show below when we calculate the variance of the new estimate.

I'd also like to highlight the role of the sensor in this scenario. As we discussed above, if you were to rely completely on the commands, the growth in uncertainty is completely **unbounded**. It will just grow, grow, grow over time. On the other hand, the sensor noise is a constant that does not increase over time. As a result, it **bounds** the uncertainty of the estimate. Even though the correction step "believed" the command estimate more, the correction from the sensor removes that unbounded growth of uncertainty and will actually make the uncertainty eventually reach a steady state value (assumining we are always able to take a measurement of the wall with the sensor).

### The real correction step

Got ya! Ok, those of you who have some previous knowledge of Kalman filters can hold off on the angry emails. I was a little dishonest in the previous section about how the correction step of a Kalman filter works. What we did was possible because our example is a special case where we can perfectly estimate the robot's position given a single sensor measurement. This is not always the case for different sensors. I decided to introduce the correction step as I did above because it really highlights that all you're doing is combining your estimate from the prediction step with the measurement by calculating a weight. You'll see that the actual Kalman filter correction step is quite similar, but changes the point of view in which the prediction is compared to the sensor measurement.

In my initial description of the correction step above, we compared the prediction estimate and the sensor estimate by transforming the sensor measurement ($$z_k$$) into a state measurement ($$x_k$$). If you remember, we did this via the equation

$$
x_k = w - z_k.
$$

In other words, we calculated the answer to the question "if the sensor really did measure the position of the wall, where would the robot be?". The Kalman filter actually does this the other way around. That is, it transforms the prediction estimate into an *expected measurement*. Put differently, it calculates the answer to the question "if the robot really did move as the prediction suggested, what would you expect the measurement to be?". For our example, the answer to this question is a straightforward manipulation of the above equation. That is,

$$
z_k = w - x_k,
$$

where we can now calculate the expected measurement from the prediction estimate. If you recall the values above, this means our expected measurement is

$$
z_k = 10\text{ m} - 2\text{ m} = 8\text{ m}.
$$

So instead of having two position estimates to compare, we instead have two measurement estimates to compare: the real one from the sensor (which has uncertainty), and the expected measurement from our prediction estimate (which also has uncertainty). A key thing to realize here is that the difference between the two position estimates (in my first explanation of the correction step) and the difference between the two measurement estimates (the actual sensor measurement and the expected measurement) is **exactly** the same. The illustration below helps show why that is true.

![Driving a robot towards a wall](/images/correction_example.png)

In the illustration, the value $$s$$ is the same whether you're comparing the position estimates or the measurements. And you may recognize that value of $$s$$ as 



<br/><br/> <br/><br/> <br/><br/>

Let's start this section with a simple example. Suppose that after the prediction step, your estimate of the robot's position is

$$
\mu_{x,k} = 7.5\text{ m}, \quad \sigma^2_{x,k} = 0.04\text{ m}^2.
$$

Your robot now uses its sensor to measure the distance to the wall, giving the measurement

$$
\mu_{z,k} = 2.62\text{ m}, \quad \sigma^2_{z,k} = 0.10\text{ m}^2.
$$

As mentioned in the problem setup, you know the position of the wall relative to the start. Let's say it is $$w = 10$$ m. We now have three choices for the estimate of the position of the robot:

1. Ignore the sensor and use the prediction ($$\mu_{x,k} = 7.5$$ m, $$\sigma^2_{x,k} = 0.04$$ m$$^2$$).
2. Ignore the prediction and use sensor measurement. Since we know the position of the wall, we can estimate the position of the robot based purely on our sensor measurement. This estimate is $$\mu_{x,k} = 10 - 2.62 = 7.38$$ m, $$\sigma^2_{x,k} = (-1)^2 0.10 = 0.10$$ m$$^2$$. Note that this function (10 - $$z_k$$) is a linear function applied to a Gaussian random variable, so the result is also a Gaussian random variable.
3. Somehow combine the prediction with the sensor measurement.

The correction step of a Kalman filter performs choice #3, and does so in the *best possible way given the information available*. That's what makes the Kalman filter so useful!

Let's intuitively think about how we might mix the prediction and the sensor measurement. In the above example, when we ignored the sensor, we got $$\mu_{x,k} = 7.5$$, and when we ignored the prediction, we got $$\mu_{x,k} = 7.38$$. So it would make sense that our combined estimate is somewhere between these two values. Why are these two estimates $$0.12$$ m apart? One way to look at it is by comparing the sensor measurement with *what we'd expect the measurement to be* given the current prediction. In other words, before we even took a sensor measurement, what would be the best guess of what our sensor would tell us? The answer is quite intuitive:

$$
\hat{z}_k = w - x_k,
$$

where $$\hat{z}_k$$ is called the *expected measurement* and this equation is called the *measurement model*. Keeping in mind that we are applying linear operations to Gaussian random variables, let's plug in the numbers from our example:

$$
\mu_{\hat{z}, k} = 10 - 7.5 = 2.5\text{ m}, \quad
\sigma^2_{\hat{z}, k} = (-1)^2 0.04 = 0.04\text{ m}^2.
$$

Now check this out: the difference $$s_k$$ between the actual measurement $$z_k$$ and the expected measurement $$\hat{z}_k$$ is

$$
\begin{align}
\mu_{s,k} &= \mu_{z,k} - \mu_{\hat{z},k} = 2.62 - 2.5 = 0.12 \text{ m} \\
\sigma^2_{s,k} &= (1)^2\sigma^2_{z,k} + (-1)^2\sigma^2_{\hat{z},k} = 0.10 + 0.04 = 0.14\text{ m}^2.
\end{align}
$$

In other words, *the difference between the actual and expected measurement is directly related to the difference between the prediction-only and sensor-only position estimates*. In this example, this difference *is* the difference between the estimates, but that's not always the case. For example, let's say instead the sensor measured the angle between the robot and the top of the wall (i.e., as you get closer to the wall, this angle gets larger). In this scenario, we can compare the expected and actual measurements of the angle, and their difference will be directly related (but not equal to) the difference between the prediction-only and sensor-only estimates. Coming back to our example, here is an illustration describing what's going on:

So in our example, we can clearly see how $$s$$ is both the difference between the actual and expected measurements and difference between the prediction-only and sensor-only position estimates (once again, these are normally directly related but not necessarily the same).

From the above figure, note that if we want to combine the prediction-only and sensor-only position estimates, we can do so by calculating some fraction of $$s$$ and adding it to the sensor-only measurement. However, the usual convention of the Kalman filter has us adding a fraction of $$s$$ to the *prediction-only* measurement; i.e.,

$$
x_{\text{pred.},k} \leftarrow x_{\text{pred.},k} + Ks_k,
$$

where $$K$$ is called the *Kalman gain*. For this correction to work, we'd expect $$-1 \leq K \leq 0$$. If $$K = 0$$, we'll just get the prediction-only estimate, and if $$K = -1$$, we'll just get the sensor-only estimate. So how in the world do be pick $$K$$? Let's just say it's a good thing we've been keeping track of variances. Recall that we have two "measurements": the expected measurement $$\hat{z}_k$$ and the actual measurement $$z_k$$. We know that their difference is directly related to the difference between the prediction-only and sensor-only position estimates, and we know the variances of these measurements (we calculated the expected measurement variance above, and the actual measurement variance is known from the sensor):

$$
\sigma^2_{\hat{z},k} = 0.04\text{ m}^2, \quad \sigma^2_{z,k} = 0.10\text{ m}^2.
$$

The value of $$K$$ is the *relative size of the expected measurement variance compared to the correction variance*. In other words,

$$
K = (-1)\frac{\sigma^2_{\hat{z},k}}{\sigma^2_{\hat{z},k} + \sigma^2_{z,k}} = \frac{-\sigma^2_{\hat{z},k}}{\sigma^2_{s,k}} = \frac{-0.04}{0.14} \approx -0.2857.
$$

It's worth breaking down the above equation to really understand where it came from before we move on.





<!---
The correction step of  uses a *measurement model* to correct the prediction by using a sensor measurement. More specifically, the correction step compares the sensor measurement with *what we'd expect the measurement to be* given our current estimate of the robot's position. The measurement model calculates this expected measurement. For our robot, the measurement model is

$$
\hat{z}_k = w - x_k,
$$

where $$\hat{z}_k$$ is the expected measurement. Remember that because $$x_k$$ is a Gaussian random variable, $$\hat{z}_k$$ is one too (with mean $$\mu_{\hat{z},k}$$ and variance $$\sigma^2_{\hat{z},k}$$) because it is the result of performing linear operations on a Gaussian random variable.

Let's do a simple example. Suppose that after the prediction our estimate is $$\mu_{x,k} = 7.5$$ m with variance $$\sigma^2_{x,k} = 0.04$$ m$$^2$$. If the position of the wall is $$w = 10$$ m, our *expected measurement* would be

$$
\mu_{\hat{z}, k} = 10 - 7.5 = 2.5\text{ m}, \quad
\sigma^2_{\hat{z}, k} = (-1)^2 0.04 = 0.04\text{ m}^2.
$$


$$10 - 7.5 = 2.5$$ m. Now suppose we use our sensor to get an *actual* measurement of the wall, and we get

$$
\mu_{z,k} = 2.62, \quad \sigma^2_{z,k} = 0.10.
$$

(Remember that the sensor measurements are modelled as Gaussian random variables.) We now have three choices for the estimate of the position of the robot:

1. Ignore the sensor and use the prediction ($$\mu_{x,k} = 7.5$$ m, $$\sigma^2_{x,k} = 0.04$$ m$$^2$$).
2. Ignore the prediction and use sensor measurement ($$\mu_{x,k} = 10 - 2.62 = 7.38$$ m, $$\sigma^2_{x,k} = 0.10$$ m$$^2$$). Note that the uncertainty of the robot's position in this case is the variance of the sensor measurement.
3. Somehow combine the prediction with the sensor measurement.

The correction step of a Kalman filter performs choice #3, and does so in the *best possible way given the information available*. That's what makes the Kalman filter so useful! More specifically, it combines the prediction and sensor measurement by using the following correction:

$$
x_k \leftarrow x_k + \underbrace{K(z_k - \hat{z}_k)}_{\text{correction}}.
$$

In other words, it adjusts the prediction by the difference between the actual and predicted measurements, scaled by some value $$K$$. Let's take a look at a few scenarios to see how this works:

- $$K = 0$$. The "corrected" prediction is just the prediction itself. The sensor measurement has no effect on the prediction. Put differently, setting $$K$$ to zero says we completely trust our prediction.
- $$K = 1$$. The correction is equal to the difference between the actual and predicted measurements. This actually makes the corrected prediction equal to the measurement. Put differently, setting $$K$$ to one says we completely trust our measurement.
- $$0 < K < 1$$. The correction is equal to some fraction of the difference between the actual and predicted measurements.

So it seems that this equation can satisfy all three of our scenarios, and I've already told you that the Kalman filter combines the prediction and the sensor measurement. It does so by choosing the *best* value of $$K$$.

-->

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

-->


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

<!---
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
-->
