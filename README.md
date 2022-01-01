# AOC-2021
Advent of Coding 2021 

Purpose: Pedagogical (Learn types, OOP)

Inspired by: Joel Grus (https://www.youtube.com/c/JoelGrus)

Several neat implementations on subreddit: https://old.reddit.com/r/adventofcode/

Most puzzles are fun to think through. The focus is not only on data structures -- there are puzzles that require some math too. For example, in day17 I had to derive equations and plot family of curves; find patterns is how the roots are arranged: 

<p align="center">
  <img alt="day17: time range for x" src="fig/pxt_time_range.png" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="day17: time range for y" src="fig/pyt_time_range.png" width="45%">
</p>


Some additional thoughts/takeaways:

| Day | Thoughts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   1 | --                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|   2 | --                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|   3 | Iterative binary search; indices go awry every single time.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   4 | --                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|   5 | --                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|   6 | Simultaneously executed two recurrence relations; read a simpler DP solution much later.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|   7 | Saw a fun proof for L1 + L2 Norm minimizer (over integers) ; there is no closed form solution and we need to look for integers that lie in mean-1/2 to mean+1/2 range sort of<br>Credits: https://www.reddit.com/r/adventofcode/comments/rawxad/2021_day_7_part_2_i_wrote_a_paper_on_todays/                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|   8 | Irritating puzzle to code up - easier to solve on paper                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|   9 | Iterative DFS with stack                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|  10 | --                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|  11 | --                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|  12 | First challenging problem; implemented graph class after a while. DFS works when you are typically looking for one path - but if you have to keep track of several paths, its better to go for several DFS runs. So the twist here is do iterative DFS-like code -- with a stack of paths instead. <br>Credits: Joel Grus and https://github.com/DenverCoder1/Advent-of-Code-2021 -- really liked the OOP + documentation + typing here                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|  13 | Learned @classmethod, `__str__` and other dunder methods. Also the difference between `tuple`, `namedtuple`, and `@dataclass`. `namedtuples` are most often better than tuples. If you feel the value you store in `namedtuple` might change later on - better have it as a dataclass.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|  14 | Nice DP puzzle -- whenever you feel things blow up exponentially, there will be some axis along which the exponential counts get classified into. Have dictionary of those classes -- and increase counts for each class. Saves space / no need to store lists/dicts of exponential size.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|  15 | Just like in a diagram (periodic table, subway maps) -- with OOP it becomes easier to identify patterns, areas that need attention, and overall info dissemination. I might not have quickly realized updates for Part-2 with a crude dijkstra implementation (like my [earlier dijkstra code](https://github.com/suryabulusu/CSES-Python/blob/bb827e40ea8e1bf6536b1201925aaadefdccb2d2/Python_Code/Shortest_Routes_I.py)). But with object-oriented implementation, I quickly noticed the 2-3 lines of addition needed for a particular method in class.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|  16 | Irritating long problem -- but showed me how tricky it is to just brute-force bring given text to code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|  17 | fun question - derive equations, draw curves - find extremes to iterate over based on roots. reminded me of JEE cubic roots questions. I did not implement a general solution - restricted answer based on properties of input text. Figures are added in `fig` folder<br><br>Referred in parts to this code: https://github.com/prscoelho/aoc2021/blob/main/a17.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|  18 | Very tough question - implemented binary tree + inorder traversal (using `yield from`) for the first time in Python. Comparing nodes/trees led to recursion limit errors - so I converted them back to string to compare. Though I think a better way would be to write `__eq__` and `hash()` methods. <br>Somewhat learned to use assert statements for better debugging [in earlier problems I just wrote them for vibes].<br>Left debug comments as it is -- I think they will add value when I revisit this code. <br>Struggled with typing -- especially with `Optional[Node]` -- forced me to write several `if node is None` statments to avoid errors<br>Struggled with solving on paper too -- very long set of operations on binary trees<br><br>Credits: Built upon https://www.youtube.com/watch?v=i-XccJenOMw                                                                                                               |
|  19 | Finally force-fit numpy for a puzzle -- not sure if it made things easy. I got the rotation matrix computation wrong (permute `np.eye(3)` and negate each row didn't work - can't visualize why) -- later found on subreddit that scipy spatial already has them precomputed. I'm still not sure if my code is correct - I think the input text was kind. They could have made it very tricky. Again found asserts very useful to debug.<br>I also felt debugging with ipynb was easier -- printing matrices, debugging each scanner loc, orientation made more sense when their state was retained. <br><br>Credits for scipy spatial: https://github.com/marcodelmastro/AdventOfCode2021/blob/main/Day19.ipynb                                                                                                                                                                                                                         |
|  20 | Somewhat easy puzzle - avoided numpy convolution for this one / good old python is enough                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|  21 | Fun puzzle -- it felt somewhat like beam search. I realized HMM-like nature of it early - transition matrix from one position to other; and score matrix from one position to a score. Identifying that the number of scores is limited helped me arrive at this abstraction. `mat[s + final_pos][final_pos] = sum_over_currpos score[s][currpos] * transition[currpos][finalpos]`.<br>I think you can call it DP too - there's memoization, deriving answer from subproblems etc. But it felt good to get an answer with HMM-like abstraction. Aso played with itertools cycle and product.                                                                                                                                                                                                                                                                                                                                              |
|  22 | Tough to visualize -- need to find intersection of cuboids and break into several cuboid parts. I tried solving it via individual dimensions but couldn't build a solution even for 2D. Had to refer to subreddit -- found interesting approaches and visualizations. <br><br>Credits: https://photos.app.goo.gl/UWVG6Widq4zt1Upf9 and https://github.com/juanplopes/advent-of-code-2021/blob/main/day22b.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|  23 | Most definitive question of AOC 2021 imo -- lots of things to learn. The abstraction is a graph of GameStates with non-negative edge weights -- and we need to find the shortest path (dijkstra). Needs `__eq__`, `hash()`, `__lt__` for `heapq` to compare gamestates. Realized the importance of `deepcopy`, importance of hash methods in class [class instance can't be a dictkey without hash], etc. <br>The states quickly blow up -- taking more than 1 minute to empty heap queue. I was too burned out and gave up on speeding things. <br>I should've had Room-stack as a class but didn't recognize it early. Deepcopy (time-consuming) could've been avoided maybe, and also some gamestates. But very satisfied with getting the right answer for both parts -- I didn't expect it would work when states blew up to 20k. <br><br>Referred in parts to: https://github.com/githuib/AdventOfCode/blob/master/year2021/day23/__init__.py |
|  24 | Crack question. I couldn't solve it -- checked subreddit and found an incredibly well written explainer here - https://old.reddit.com/r/adventofcode/comments/rnl0vn/2021_day_24_had_me_for_a_sec/hpuvs50/<br><br>Tried to write the solution in my own words + added some more details over the above solution. I aspire to write such smooth yet detailed explainers from scratch some day.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|  25 | --                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |



