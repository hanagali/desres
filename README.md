# DESRES code sample
Submission of code sample to DESRES application


the prompt: Please include a link to your GitHub or GitLab page or another non-proprietary code sample., and please highlight a section of your code that you particularly enjoyed writing and explain why.


This repo contains a short sample (relevant lines: 27-70) from my summer work on "Efficient simulation of 3D reaction-diffusion" in 2021, that generates one of the paper figures that show wave propagation over time on a 3D cell model. What makes the figure particularly interesting is the fact that there is curvature in the wave showing that the reaction-diffusion process that happens in the cell truly does happen in 3D and that the spatial distribution of (here, calcium) concentration is significant and non-negligible. 

I enjoyed working on this small piece of code not because it was easy, but because it proved to be much harder than anticipated. The simulations took significant computing time and power, finding the right cell model to show this effect, figuring out how to set up the reaction-diffusion itself (the wave), and then how to time it properly so that the aforementioned effects were visually clear, all took effort and excruciating wait. It amplified my appreciation for algorithm optimization (I was informed that the process I got to use here was new and recent -- the simulations took exponentially longer before it was optimized) and efficiency. It also amplified my appreciation for making neuroscience (or, in general biology/chemistry-related science) computational, because other than some computing power and server time (and my own patience), nothing was wasted, ruined, or endangered, including resources. 
Ultimately, I struck the right balance for the parameters of the function, got the right formatting, and got to show reaction/concentration behavior over time at any point in a cell model. 

