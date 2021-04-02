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
with the two object's locations as the start and end.
I did this, and my implementation was this:
```
def distance(start, end):
    return np.sqrt(np.sum((start - end) ** 2))
```
Wait! I've calculated the force, but not what direction it is going toward!
Okay, how am I going to implement that? (This was actually the hardest part of the whole project).
Well, it would be proportional (albeit negatively proportional) to the square of the distance from the two objects.
So, I just have to make a "force-matrix" of where the force would go to.
What if I just make the force-matrix times the force equal the force in 3D?
Well, for that to work, the sum of the force-matrix would be 1.
How would I calculate that? Well, if I take the distance right before the `np.sum` operation, I have the correct formula, except that the sum is equivalent to the square of the distance.
