# An Explanation

## Gravity

How does my gravity formula work, you ask.
Well, it's made up of many parts.
My initial plan was to iterate over each object.
Then, each object would iterate over every other object, calculate the force between them, and add that to its momentum.
Finally, the objects location would be incremented by its momentum
Okay, so let's implement that ...
```
def gravity(self, m1, m2, r):
    return r, G * m1 * m2 / (r ** 2)
```
Wait! Hold on! `r` uses distance, but how will I get that?
Well, I can use the Distance Function for N dimensions
<img src="https://latex.codecogs.com/svg.latex?\Large&space;d(s,%20e)=\sqrt{(s_0-e_0)^2+(s_1-e_1)^2+...+(s_d-e_d)^2}" title="\Large&space;d(s,%20e)=\sqrt{(s_0-e_0)^2+(s_1-e_1)^2+...+(s_d-e_d)^2}"/>
with the
