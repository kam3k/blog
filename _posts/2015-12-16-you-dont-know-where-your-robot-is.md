---
layout: post
title:  You don't know where your robot is
comments: true
date:   2015-12-16
---

If you are learning about probabilistic robotics, it is always important to remember that you are working with *random variables*. In other words, you need to realize that---no matter how well you measured it---you are uncertain about the state of your robot. No matter what you do, you cannot know precisely where your robot is, how fast it is moving, or how it is oriented. What you can do, however, is quantify your ignorance. In other words, you can estimate just how well (or how badly) you know things.

## Motivating example

To better explain why random variables are used in robotics, let's look at an example. Suppose we are driving a robot down a road towards a wall, like in the image below.

![Driving a robot towards a wall](/images/random_variable_example.png)

In this example, you are standing somewhere with a joystick. When you push the joystick forward, it commands the robot to move forward at some speed $$u$$. The robot has a sensor (e.g., laser rangefinder, camera, sonar) that can measure the distance to the wall $$z$$. You know the distance to the wall from the start $$w$$ because you measured it earlier with a measuring tape. So here is the big question: what is $$x$$, the position of the robot?

Listed below are a few reasons why you cannot solve for an *exact* answer for $$x$$.

* Let's say you're clever and you timed how long the robot has been driving (let's say it was exactly ten seconds), and you commanded the robot to drive at 1 m/s with your joystick. So since you've driven for ten seconds at 1 m/s, you say "Aha!, $$x$$ is 10 m!". However, how sure are you that you drove for ten seconds (and not 10.001 seconds)? How sure are you that your command of 1 m/s actually resulted in the robot moving at 1 m/s (and not 0.996 m/s)? How is the robot transforming your command of 1 m/s into how fast it turns the wheels?

* Suppose your sensor says the robot is 4.5 m from the wall, and you know from using your measuring tape that $$w$$ is 10 m (i.e., the distance to the wall from the start). Therefore, the position of the robot is just (10 - 4.5) m = 5.5 m, right? Well how good is that sensor? Can it tell the difference between 4.5 m and 4.52 m? How accurately did you know the position of the wall to begin with (with your measuring tape)?

* In this example, the wall is modelled as a straight, vertical surface. What if the actual wall has a door or window? What if it has wooden trim, or pictures hanging from it? What if someone got angry that they couldn't calculate $$x$$ exactly and they punched the wall, leaving a deep dent? 

* How frequently is your joystick sending the signal to the robot to move? Five times per second? 100 times per second? How quickly does a change in command result in the robot actually changing speed? How often does your measurement of the wall update? What happens if you're driving really fast and then slam the brakes? Does your robot slide?

Now that we've accepted that we're never going to know what $$x$$ is, we can do the next best thing: represent $$x$$ as a *continuous random variable*.

## Continuous random variables

A continuous random variable is something that can take on any of an infinite number of possible values (e.g., the height of a pine tree, the time it takes you to read this sentence). In our above example, the position of the robot can be modelled as a continuous random variable. In other words, an infinite number values for $$x$$ are possible, such as <nobr>10.02 m</nobr>, <nobr>11.93321 m</nobr>, <nobr>9.0001 m</nobr>, <nobr>9.0000000000001 m</nobr>, and so on. What we are interested in is representing the *likelihood* of a value of $$x$$ occurring. 

For example, suppose the true position of the robot in the above example is <nobr>5.113 m</nobr> (remember, we can't know this). If we have a good representation of the likelihood of $$x$$, then it should tell us that $$x$$ is much more likely to be <nobr>5 m</nobr> then <nobr>10 m</nobr>. By far the most common representation of the likelihood of a variable in probabilistic robotics is the normal (or Gaussian) distribution, which looks something like this: 

![The probability density function of a normal distribution.](/images/normal_pdf.png)

Don't worry about what $$f(x)$$ is just yet. A normal distribution can be specified by two numbers: $$\mu$$ and $$\sigma$$. The *mean* of the distribution is $$\mu$$ (it is also the median and mode, but don't worry about this for now), which is the most likely estimate of the random variable (in other words, it is the peak of the curve). The *standard deviation* of the distribution is $$\sigma$$, which specifies how spread out ("wide") the curve is.

Returning to our robot example, suppose we used our sensors to model the position of the robot as a random variable with a normal distribution. If our sensors are pretty good, we might get something like $$\mu = $$ <nobr>5.2 m</nobr> and $$\sigma = $$ <nobr>0.1 m</nobr> (remember, the true position is <nobr>5.113 m</nobr>). If are sensors are a little worse, maybe we'll get something closer to $$\mu = $$ <nobr>5.1 m</nobr> and $$\sigma = $$ <nobr>0.3 m</nobr>. Note that our sensors getting worse makes $$\sigma$$ bigger (and the curve in the above plot "wider").

## Probability density functions

The *probability density function* (PDF) of the distribution of a random variable $$x$$ calculates the likelihood of $$x$$. In other words, it is the function $$f(x)$$ on the y-axis in the above plot for normal distributions. Mathematically,

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}
$$

Don't worry too much about why the $$f(x)$$ takes this form. Just know that given the mean $$\mu$$ and standard deviation $$\sigma$$ of a random variable, $$f(x)$$ results in the above plot when you plug values of $$x$$. 

We can use the PDF to compare the relative likelihood of the robot being at different positions. For example, given $$\mu = $$ <nobr>5.1 m</nobr> and $$\sigma = $$ <nobr>0.2 m</nobr>, how much more likely is the position of the robot <nobr>5.2 m</nobr> compared to <nobr>5.5 m</nobr>? The answer is simply the ratio of their likelihoods; i.e.,

$$
f(5.2) = f(5.1 + 0.1) = f(\mu + 0.5\sigma) \approx 1.760
$$

$$
f(5.5) = f(5.1 + 0.4) = f(\mu + 2\sigma) \approx 0.270
$$

$$
\frac{f(5.2)}{f(5.5)} \approx 6.521
$$

In other words, the position <nobr>5.2 m</nobr> is approximately 6.521 more likely than <nobr>5.5 m</nobr>.

## Probability

The *probability* of a particular range of values of $$x$$ is an absolute measure of how likely it is that the true $$x$$ is in that range. A probability is a number between 0 (no chance of occurring) and 1 (is absolutely known to occur). For example, one might say "the probability that $$x$$ is between 4.5 and 5.5 is 0.87654".

PDFs have the very important property that the area under the curve between two values of $$x$$ is the probability of that range of $$x$$. As you may guess, this means that the area under the full curve (i.e., between $$x=-\infty$$ and $$x=\infty$$), the area under the PDF is 1. More interesting is the area between non-infinite values of $$x$$, such as the example shown below.

![The probability density function of a normal distribution.](/images/normal_pdf_area.png)

Suppose that in the above PDF, $$\mu = $$ <nobr>5.1 m</nobr> and $$\sigma = $$ <nobr>0.2 m</nobr>. Then the highlighted area is the probability that $$x$$ is between <nobr>4.7 m</nobr> (i.e., $$\mu - 2\sigma$$) and <nobr>4.9 m</nobr> (i.e., $$\mu - \sigma$$). Recall from first year calculus that the area under a curve is calculated using integration. For the above curve, the probability of $$x$$ being in the given range is written as $$p(4.7 \leq x \leq 4.9)$$ and is the definite integral of the PDF; i.e.,

$$
p(4.7 \leq x \leq 4.9) = \int_{4.7}^{4.9} \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}} dx
$$

Substituting in $$\mu = $$ <nobr>5.1 m</nobr> and $$\sigma = $$ <nobr>0.2 m</nobr>, we get

$$
p(4.7 \leq x \leq 4.9) = \int_{4.7}^{4.9} 1.995e^{-\frac{(x-5.1)^2}{0.08}} dx = 0.27
$$

In other words, there is a 27% chance that $$4.7 \leq x \leq 4.9$$.

## You know where your robot may be

I started off this post by emphasizing the fact that you don't know where your robot is. The best you can do is quantify your ignorance. Parameterizing the unknown quantity (e.g., the position of the robot) as a continuous random variable is one way to do this. In probabilistic robotics, normal distributions are the most common distribution used to represent random variables, which are commonly described by its mean $$\mu$$ and standard deviation $$\sigma$$. I should note that the variance $$\sigma^2$$ of a normal distribution is often stated in place of its standard deviation (i.e., it is literally the squared standard deviation).

So assuming you are using a normal distribution to represent the position of a robot, if someone asks "what is the position of the robot?", some appropriate equivalent answers are:

* "I estimate its mean position to be <nobr>11.6 m</nobr> with a standard deviation of <nobr>0.5 m</nobr>."
* "I am about 95% certain it is between <nobr>10.6 m</nobr> and <nobr>12.6 m</nobr>."
* "I believe it is at <nobr>11.6 m</nobr> with a variance of 0.25 m$$^2$$."

Note that for the second answer, the integral between $$\mu - 2\sigma$$ and $$\mu + 2\sigma$$ is approximately 0.95 for the PDF of a normal distribution. Some insufficient answers are:

* "It is approximately 11.6 m." (Missing information about uncertainty.)
* "11.6 $$\pm$$ 0.5 m." (Is 0.5 m the standard deviation?)
* "I believe it is at <nobr>11.6 m</nobr> with a variance of 0.25 m." (The units of variance should be m$$^2$$, making this statement confusing.)

Note that a common fallacy is people mistaking the estimated mean position being close to the true position as your estimate being "good". For example, suppose your current estimate of the robot's position is $$\mu = $$ <nobr>10.1 m</nobr> and $$\sigma = $$ <nobr>5.5 m</nobr>. Now you take out a measuring tape and measure the robot's position to be <nobr>10.02 m</nobr>. Awesome estimate right? Not necessarily! A good estimate requires that both the mean *and* the standard deviation to be a good representation of your current knowledge of the robot's position. If you had great sensors, perhaps $$\mu = $$ <nobr>10.1 m</nobr> and $$\sigma = $$ <nobr>0.15 m</nobr> is actually a more appropriate estimate of the robot's position.

Always keep in mind, *you don't know where your robot is!*
