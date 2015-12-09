---
layout: post
title:  You don't know where your robot is
comments: true
date:   2015-10-21
---

If you are learning about probabilistic robotics, it is always important to remember that you are working with *random variables*. In other words, you need to realize that---no matter how well you measured it---you are uncertain about the state of your robot. No matter what you do, you cannot know precisely where your robot is, how fast it is moving, or how it is oriented. What you can do, however, is quantify your ignorance. In other words, you can estimate just how well (or how badly) you know things.

### Motivating example

To better explain why random variables are used in robotics, let's look at an example. Suppose we are driving a robot down a road towards a wall, like in the image below.

![Driving a robot towards a wall](/images/random_variable_example.png)

In this example, you are standing somewhere with a joystick. When you push the joystick forward, it commands the robot to move forward at some speed $$u$$. The robot has a sensor (e.g., laser rangefinder, camera, sonar) that can measure the distance to the wall $$z$$. You know the distance to the wall from the start $$w$$ because you measured it earlier with a measuring tape. So here is the big question: what is $$x$$, the position of the robot?

Listed below are a few reasons why you cannot solve for an *exact* answer for $$x$$.

* Let's say you're clever and you timed how long the robot has been driving (let's say it was exactly ten seconds), and you commanded the robot to drive at 1 m/s with your joystick. So since you've driven for ten seconds at 1 m/s, you say "Aha!, $$x$$ is 10 m!". However, how sure are you that you drove for ten seconds (and not 10.001 seconds)? How sure are you that your command of 1 m/s actually resulted in the robot moving at 1 m/s (and not 0.996 m/s)? How is the robot transforming your command of 1 m/s into how fast it turns the wheels?

* Suppose you're sensor says you are 4.5 m from the wall, and you know from using your measuring tape that $$w$$ is 10 m (i.e., the distance to the wall from the start). Therefore, the position of the robot is just (10 - 4.5) m = 5.5 m, right? Well how good is that sensor? Can it tell the difference between 4.5 m and 4.52 m? How accurately did you know the position of the wall to begin with (with your measuring tape)?

* In this example, the wall is modelled as a straight, vertical surface. What if the actual wall has a door or window? What if it has wooden trim, or pictures hanging from it? What if someone got angry that they couldn't calculate $$x$$ exactly and they punched the wall, leaving a deep dent? 

* How frequently is your joystick sending the signal to the robot to move? Five times per second? 100 times per second? How quickly does a change in command result in the robot actually changing speed? How often does your measurement of the wall update? What happens if you're driving really fast and then slam the brakes? Does your robot slide?

Now that we've accepted that we're never going to know what $$x$$ is, we can do the next best thing: represent $$x$$ as a *continuous random variable*.

### Continuous random variables

A continuous random variable is something that can take on any of an infinite number of possible values (e.g., the height of a pine tree, the time it takes you to read this sentence). In our above example, the position of the robot can be modelled as a continuous random variable. In other words, an infinite number values for $$x$$ are possible, such as <nobr>10.02 m</nobr>, <nobr>11.93321 m</nobr>, <nobr>9.0001 m</nobr>, <nobr>9.0000000000001 m</nobr>, and so on. What we are interested in is representing the *likelihood* of a value of $$x$$ occurring. 

For example, suppose the true position of the robot in the above example is <nobr>5.113 m</nobr> (remember, we can't know this). If we have a good representation of the likelihood of $$x$$, then it should tell us that $$x$$ is much more likely to be <nobr>5 m</nobr> then <nobr>10 m</nobr>. By far the most common representation of the likelihood of a variable in probabilistic robotics is the normal (or Gaussian) distribution, which looks something like this: 

![The probability density function of a normal distribution.](/images/normal_pdf.png)

Don't worry about what $$f(x)$$ is just yet. A normal distribution can be specified by two numbers: $$\mu$$ and $$\sigma$$. The *mean* of the distribution is $$\mu$$ (it is also the median and mode, but don't worry about this for now), which is the most likely estimate of the random variable (in other words, it is the peak of the curve). The *standard deviation* of the distribution is $$\sigma$$, which specifies how spread out ("wide") the curve is.

Returning to our robot example, suppose we used our sensors to model the position of the robot as a random variable with a normal distribution. If our sensors are pretty good, we might get something like $$\mu = $$ <nobr>5.2 m</nobr> and $$\sigma = $$ <nobr>0.1 m</nobr> (remember, the true position is <nobr>5.113 m</nobr>). If are sensors are a little worse, maybe we'll get something closer to $$\mu = $$ <nobr>5.1 m</nobr> and $$\sigma = $$ <nobr>0.3 m</nobr>. Note that our sensors getting worse makes $$\sigma$$ bigger (and the curve in the above plot "wider").

### Probability density functions

The *probability density function* (PDF) of the distribution of a random variable $$x$$ calculates the likelihood of $$x$$. In other words, it is the function $$f(x)$$ on the y-axis in the above plot for normal distributions. Mathematically,

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}
$$

Don't worry too much about why the $$f(x)$$ takes this form. Just know that given the mean $$\mu$$ and standard deviation $$\mu$$ of a random variable $$x$$, $$f(x)$$ results in the above plot when you plug values of $$x$$. 

We can use PDF to compare the relative likelihood of the robot being at different positions. For example, given $$\mu = $$ <nobr>5.1 m</nobr> and $$\sigma = $$ <nobr>0.2 m</nobr>, how much more likely is the position of the robot <nobr>5.2 m</nobr> compared to <nobr>5.5 m</nobr>? The answer is simply the ratio of their likelihoods; i.e.,

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
  

A probability is a number between 0 and 1 that measures the likelihood of something occurring. The sentence

<p style="text-align:center"><i>The probability of rolling a six on a fair die is one in six.</i></p>

is stated mathematically as

$$
p(D = 6) = \frac{1}{6}
$$

where $$D$$ is a random variable representing the outcome of a die. If we were to drive our robot for <nobr>10 s</nobr> at <nobr>1 m/s</nobr>, it is not surprising that

$$
p(X = 200~\text{light years}) = 0.
$$

where $$X$$ is a random variable representing the position of the robot. However, you might be surprised to learn that

$$
p(X = 10~\text{ m}) = 0.
$$

Surely it's possible that the position of the robot is about <nobr>10 m</nobr> after driving at <nobr>1 m/s</nobr> for <nobr>10 s</nobr>? Re-read that last sentence, I put a clue in it that explains all this nonsense. Here is the important part: "...position of the robot is *about* <nobr>10 m</nobr>...". A-ha! Note that I didn't write

$$
p(X = \text{about}~10~\text{m}) = 0.
$$

It turns out that the probability that the robot is at any *exact* position is zero. If you go out and measure the position of the robot as <nobr>10.0 m</nobr>, I'll ask you if its position is 10.00 m. And if it is, I'll ask you if its position is 10.00000. I can go all day. This describes the difference between a *discrete* random variable, which has a finite number of outcomes (e.g., rolling a die), and a *continuous* random variable, which has an infinite number of outcomes (e.g., the position of a robot). So what good are probabilities for continuous random variables if they are all zero? For that we need to learn about probability density functions.

### Probability density functions

Alright we're getting too deep in the woods here. Let's explain our result with the help of a probability density function (PDF), before bringing all this discussion back to random variables in the context of robotics. By far the most common PDF you'll encounter when studying probabilistic robotics is the one for normal distributions (sometimes called Gaussian distributions). If the height of a pine tree is well described by a normal distribution (it turns out it is), its PDF is

$$
p(H = h) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(h-\mu)^2}{2\sigma^2}}
$$

where $$\mu$$ is the *mean* (average) height of a pine tree, and $$\sigma$$ is the standard deviation (how certain we are of the mean). Don't worry too much about the equation for now. A plot of this equation looks like this:

![The probability density function of a normal distribution.](/images/normal_pdf.png)

The point I want to make is that you can use the PDF to calculate the likelihood that a pine tree will be within a certain interval of heights (e.g., 35 to 40 m) can be calculated using the PDF. For example,

$$
p(35~\text{m} \leq H \leq 40~\text{m}) = \int_{35}^{40} \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(h-\mu)^2}{2\sigma^2}} dh.
$$
