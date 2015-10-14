---
layout: post
title:  Random variables
date:   2015-10-10
---

If you are learning about probabilistic robotics, it is always important to remember that you are working with *random variables*. In other words, you need to realize that---no matter how good your sensor is, or no matter how well you measured it---you are uncertain about the state of your robot. There is no such thing as the perfect sensor. No matter what you do, you cannot know precisely where your robot is, how fast it is moving, or how it is oriented. What you can do, however, is quantify your ignorance. In other words, you can keep estimate just how well (or how badly) you know things.

Robotics often deals with *continuous random variables*. A continuous random variable is something that can take on any value (e.g., the distance you can run in five minutes, the height of a pine tree). But wait, if it can be any value, why can't I run ten kilometres in five minutes? And why aren't there pine trees that are three kilometres tall? This is because each continuous random variable has what is called a *probability density function* that describes the relative likelihood that the random variable will be a certain value (more on that later).

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
