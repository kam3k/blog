---
layout: post
title:  You don't know where your robot is
comments: true
date:   2015-10-21
---

If you are learning about probabilistic robotics, it is always important to remember that you are working with *random variables*. In other words, you need to realize that---no matter how good your sensor is, or no matter how well you measured it---you are uncertain about the state of your robot. No matter what you do, you cannot know precisely where your robot is, how fast it is moving, or how it is oriented. What you can do, however, is quantify your ignorance. In other words, you can estimate just how well (or how badly) you know things.

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

A continuous random variable is something that can take on any of an infinite number of possible values (e.g., the height of a pine tree, the time it takes you to read this sentence). But wait, if it can be any value, why aren't there pine trees that are three kilometres tall? This is because 

Continuing with our pine tree example, let's call our random variable describing its height as $$H$$. The way we write the phrase "the probabilty that the height of a pine tree ($$H$$) is three kilometres tall" is

$$
p(H=3~\text{km}).
$$

And as you might have guessed,

$$
p(H=3~\text{km}) = 0.
$$

However, the reason why $$p(H=3~\text{km})=0$$ is not for the reason you may have guessed (i.e., its not because you've never seen a colossal pine tree). In fact, it might surprise you that

$$
p(H = 30~\text{m}) = 0
$$

when surely you've seen pine trees that are about 30 m tall. Re-read that last sentence, I put a clue in it that explains all this nonsense. Here it is again: "...when surely you've seen pine trees that are *about* 30 m tall". A-ha! Note that I didn't write

$$
p(H = \text{about}~30~\text{m}) = 0.
$$

It turns out that the probability that a pine tree is any *exact* height is zero. If you go out and find me a 30 m tall pine tree, I'll ask you if it's 30.00 m tall. And if it is, I'll ask you if its 30.0000 tall. I can go all day.

Alright we're getting too deep in the woods here. Let's explain our result with the help of a probability density function (PDF), before bringing all this discussion back to random variables in the context of robotics. By far the most common PDF you'll encounter when studying probabilistic robotics is the one for normal distributions (sometimes called Gaussian distributions). If the height of a pine tree is well described by a normal distribution (it turns out it is), its PDF is

$$
p(H = h) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(h-\mu)^2}{2\sigma^2}}
$$

where $$\mu$$ is the *mean* (average) height of a pine tree, and $$\sigma$$ is the standard deviation (how certain we are of the mean). Don't worry too much about the equation for now. A plot of this equation looks like this:

<div>
    <a href="https://plot.ly/~ckaiwu/105/" target="_blank" title="prices" style="display: block; text-align: center;"><img src="https://plot.ly/~ckaiwu/105.png" alt="prices" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="ckaiwu:105"  src="https://plot.ly/embed.js" async></script>
</div>

The point I want to make is that you can use the PDF to calculate the likelihood that a pine tree will be within a certain interval of heights (e.g., 35 to 40 m) can be calculated using the PDF. For example,

$$
p(35~\text{m} \leq H \leq 40~\text{m}) = \int_{35}^{40} \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(h-\mu)^2}{2\sigma^2}} dh.
$$
