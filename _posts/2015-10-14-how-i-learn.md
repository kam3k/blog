---
layout: post
title:  How I learn
date:   2015-10-14
---

Everyone learns differently. As a result, there is no universal "best way" to learn about new topics, despite what click-baity headlines may tell you. In this blog, I write about topics in the way that worked best for me when I was first learning about them. I would characterize the way I start to learn about a new topic as "simplifying the big picture". I have illustrated this approach below.

![How I learn.](/images/how_i_learn_diagram.png)

To summarize, I learn about a simplified version of the problem and slowly remove the simplifications until I get back to the original problem. This may seem like an obvious approach, but in my experience many learners (and teachers) fail for the following reasons:

* *Making too many or too few assumptions*. This is tricky because it is different for everyone. If you make too many assumptions, the topic becomes trivial and you don't end up learning something new. If you make too few assumptions, you can become lost too quickly and give up. I think the latter is more of a problem. On many occasions I've been reading a tutorial when suddenly a magic sentence appears that adds some unexplained information. I really dislike "just accepting" something I don't understand.

* *Making assumptions that change the topic too much*. It is important to maintain a reasonable path back to the original topic. For example, if you are learning about how to navigate a robot, making the assumption that the robot never moves and you can measure its location with a ruler changes the problem into "how well can you use a ruler?".

* *Not understanding why you are learning something*. We've all been there. Sitting in math class and thinking "when will I ever use this?". On many occasions I have thought to myself "I wish I could go back and pay more attention in linear algebra class". Maybe I would have if I knew how important (and interesting) it is when it comes to robot navigation.

* *Paying too much attention to details early on and missing the big picture*. This is a big one for me. When learning something complicated like "how does a car work", I find it extremely helpful to quickly try and understand a high-level answer to that question, before getting into details. That is, understand the path between your foot pressing the gas pedal to the car moving before trying to understand how internal combustion engines work.

Now for an example. Let's say you are interested in simultaneous localization and mapping (SLAM), and you want to use a robot to build a cool 3D map like the one below (image courtesy of the [OctoMap library](https://octomap.github.io)).

![3D map](/images/octomap.png)

Now suppose you have no experience in mapping with a robot. If you really want to understand how it works (and not just download software and use it without any understanding), you need to start small. If I were teaching someone from scratch, I would start with something like this:

![Simplified SLAM](/images/simple_slam.png)

The key components are still there. A robot drives through an environment and measures objects in that environment with a sensor. After understanding that, I would remove some simplications and learn how to handle something like this:

![Less simplified SLAM](/images/less_simple_slam.png)

I have shifted things from 1D into 2D. The sensor used by the robot gets more complex (in this case, it is a laser scanner), and there are many more objects. 

So by now you might be asking, "but how do I know what are reasonable simplifications to make when I don't understand the topic?". That's a great question, and it is exactly what I am trying to address in this blog. I am trying to help first-time learners understand the big picture of how different topics work by laying out the path of simplified problems. I hope this approach works for you.
