# An Explanation

## Gravity

How does my gravity formula work, you ask.
Well, it's made up of many parts.
My initial plan was to iterate over each object.
Then, each object would iterate over every other object, calculate the force between them, and add that to its momentum.
Finally, the object's location would be incremented by its momentum
Okay, so let's implement that ...
```
def gravity(self, m1, m2, r):
    return r, G * m1 * m2 / (r ** 2)
```
Okay, but there is another problem: `r` uses distance, but how will I get that from the 3D coordinates?
Well, I can use the Distance Function for N Dimensions:
<img src="https://latex.codecogs.com/svg.latex?\Large&space;d(s,%20e)=\sqrt{(s_0-e_0)^2+(s_1-e_1)^2+...+(s_d-e_d)^2}" title="My formula"/>
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
Well, for that to work, the sum of the force-matrix would need to be 1.
How would I get that? Well, if I take the distance right before the `np.sum` operation, I have the correct formula, except that the sum is equivalent to the square of the distance. That means I just have to divide each x, y, and z value by the x+y+z. Okay, but when I square the numbers, all negatives are canceled out. I'll have to "save" the negatives by useing `np.copysign`.
So, in N dimentions, the formula looks like this:
```
direction = (self.location + ([self.gsize()/2] * 2 + [0])) - (locs + self.gsize_all(masses)/2)
force = self.gravity(masses, self.get_distance(direction))
direction_matrix = np.copysign(direction ** 2, -direction).T / np.sum(direction ** 2, 1)
self.momentum += np.sum(direction_matrix * force, 1) / data.SPEED
self.location += self.momentum / data.SPEED
```
