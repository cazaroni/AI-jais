# AI-jais
repo for uploading my notes and projects done for my AI class

# AI - March 18th

Created: March 18, 2025 12:49 PM
Class: AI

# Bullet points for today

- Elaborating further on MDP - what goes into it?
- Blackjack as an example for a MDP
- Initial state for MDP class - we need a simulation state function and legal actions
- The MDP on the whiteboard is a bit complicated due to the sheer amount of states that would be required to run this game, including its transition functions.  It’s easier to escalate these kind of situations by creating simulations for general scenarios
- How do we evaluate a “politica”? Refer to the photos I took
-

# AI - March 11th

Created: March 11, 2025 12:51 PM
Class: AI

# Bullet points for today

- We’re looking into Mathematical Models for Decisions under Certainty (MDPs)
- Waissman thinks he’s yapping too much but I think he’s lecturing just the same way as he has done before, which would be a good thing in his case.
- Dice game (refer to pdf)

# AI - March 10th

Created: March 10, 2025 1:07 PM

## Happy birthday Cat!

Bullet points for today!

- We’re still talking about probability and distribution of values
- Markov chains (read up on them you dunce)
- We need matrices to define some graphics (and normalize some values along the way)
-

# AI - March 6th

Created: March 3, 2025 12:49 PM
Class: AI

# Bullet points for today

- Oh wow we’re suddenly in a Probability class, what’s up
- P ( Y = y | X = x) = (P (Y = y ^ X = x) / P (X = x) and vice versa if we were to swap the values
- Actually hold on, what’s going on?

# AI - feb 28th

Created: February 28, 2025 1:06 PM

# Bullet points for today

- Analyzing the kinds of AI that work with different programming languages (Symbolic and Subsymbolic)
- {E_x, J, A, R, G, U} will be our mathematical model to follow todal
- J_s will feature two players starting in state s
- E_0,

# AI - Feb 20th

Created: February 20, 2025 12:47 PM
Class: AI

# Bullet points for today!

- Solution cost ≥ Admissible heuristics
- Uniform cost search, greedy algo, and A* are three methods typically deployed to solve problems
- Admissible heuristics only count if their cost is less than or equal to n state for all Ns (g* = C* ≤ g.cost for all g)
- A* is also known as the branch and bound algo
- Heuristics can be categorized under trivial and dominant, depending on the problem
- (Tokenizer!) Use Klause * for tokenizing emojis

# AI - Feb 19th

Created: February 19, 2025 1:04 PM
Class: AI

# Bullet points for today

- Costs on Actions and knowing how to reach goals (alongside the least amount of resources spent)
- Search Heuristics and combining them with base costs (also accounting for any obstacles)
- When does the greedy search fuck up?

# AI - Feb 17th

Created: February 17, 2025 12:49 PM
Class: AI

# Bullet points for today

- Clarifying 3rd exercise from assignment #3
- General Tree Search cont. (which includes Depth/Breadth First Search)
- DFS tends to be better whenever we actually know the depth level, otherwise, go with BFS
- IDS is a different way to approach this matter, seems to be inefficient on the first go

# AI - Feb 3rd

Created: February 4, 2025 1:11 PM

# Linear Regression!

Bullet points for today

- General concepts [ hypothesis class, loss function, optimization ]
- Training data parameters and guidelines [ attribute extraction ]
- Mathematical aspects to consider
- Convex Functions

# AI - Jan 29th

Created: January 30, 2025 1:09 PM
Class: AI

# The Essence of Machine Learning

Bullet points for today, expand later

- The demand for generative AI related skills
- Job prospecting post-generative AI (2023)
- Machine learning’s shortcomings

## What’s machine learning all about, anyways?

Machine learning has always been conceptualized of an algorithm improving upon itself through analyzing the results it creates and, depending on it’s purpose, either predicts a certain outcome based on the data alone or is instructed by the programmer themself to ignore said outcome and discard it. Of course, this is an oversimplification of the field and it tends to be a whole lot more complicated than that. So how relevant is it in today’s age? Jesus Christ is that even a valid question to ask in this major?

###

# AI - Jan 27th

Created: January 28, 2025 9:32 AM
Class: AI

I haven’t been to at least two weeks worth of lectures, so where do I go from here? Reading the past few presentations and catching up to speed, of course.

# Artificial Intelligence - Decision Tree

The concept of binary search trees has been teased since my Teoria de la Computacion class (which is probably translated to Theory of Computation since Computational Theory apparently leads to another topic every time I google it) and we had programmed a version of it in our Data Structure class. At the time it didn’t seem like there was a whole lot going on for it other than unnecessarily long and bloated algorithms, but it did open the path for exploring back-tracing.

Decision trees seems to be expanding upon this idea and implements new concepts to digest. As I’m still trying to catch up with everything I’ve missed out so far, I’ll just scribble down what I was able to understand from both the lecture and the PowerPoint slides.

## Decisions to make

Typically demonstrated with this concept is recursion (and tons of it). Let’s say we needed to find the cheapest way to get from Point A to point J, the greedy algorithm is a shining example of how to begin employing recursion. Of course, establishing a base case is essential to be able to properly adapt this algorithm for our purposes.

On the more mathematical side of things, we assign attributes to the variables found on decision trees, alongside classes that we can assign to the “leaf”. These two form together to create hypotheses for the tree and present the possible inputs and outputs of a function.

## Entropies and Antelopes

In decision trees, entropy is a measure of impurity or disorder in a dataset. It quantifies how mixed the classes are at any given node. The formula for entropy is:

H(S) = -Σ p(i) log₂ p(i)

where p(i) is the proportion of class i in the dataset. A perfectly pure node (all samples belong to the same class) has entropy = 0, while maximum impurity (equal distribution of classes) has the highest entropy.

This concept is crucial for decision tree algorithms as it helps determine the best attributes for splitting nodes. The goal is to reduce entropy (increase information gain) with each split, leading to more organized and meaningful classifications.

(I used AI to generate the summary above me! Just wanted to see if the Notion AI was good at simplifying my long notes or not.)
