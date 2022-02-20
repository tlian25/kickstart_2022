# Milktea Solution
#
# For each bit position, take the most occuring bit
# It might fall into forbidden group
# Each bit decision is independent from each other

# Build up bits one by one
# Generate L-th bit without consider previous L-1 part

# Avoiding forbiddens
# Forbidden set size M
# If we make M+1 teas, at least 1 tea is not in the forbiddens set

'''
Optimization of scoring

Preconstruct 2d array capturing number of 0's and 1's at the i-th element across all teas
When scoring, we can just accumulate counts
For Zero branch -> add number of 1s
For One branch -> add number of 0s


'''

from distutils.command.build_clib import build_clib


class ScoredTea:
    
    def __init__(self, score:int, tea:str):
        self.score = score
        self.tea = tea


    def __eq__(self, other):
        return self.score == other.score

    def __lt__ (self, other):
        return self.score < other.score

    def __repr__(self):
        return f"({self.tea},{self.score})"



def compare(prefix:str, tea:str) -> int:

    difference = 0
    for i in range(len(prefix)):
        if prefix[i] != tea[i]:
            difference += 1

    return difference



def buildScores(teas):

    # scores[i] = [#of0s, #of1s] at i-th position across all teas
    scores = [[0, 0] for _ in range(len(teas[0]))]

    for i in range(len(scores)):
        for t in teas:
            if t[i] == '0':
                scores[i][0] += 1
            else:
                scores[i][1] += 1

    return scores

# Compare all teas in list
'''
def score(prefix:str, teas:list) -> int:

    difference = 0
    for t in teas:
        difference += compare(prefix, t)

    return difference
'''


# expand tea by appending 0 and 1
def expand(scoredteas:list, prevTea:str, teas:list, scores:list):
    zero = prevTea.tea + '0'
    one = prevTea.tea + '1'
    i = len(zero)-1

    scoredteas.append(ScoredTea(prevTea.score + scores[i][1], zero))
    scoredteas.append(ScoredTea(prevTea.score + scores[i][0], one))



def count_complaints(teas, forbiddens):

    L = len(teas[0])
    forbiddens = set(forbiddens)

    scores = buildScores(teas)


    queue = [ ScoredTea(0, "") ]

    # Loop L times for length of tea string
    for _ in range(L):
        
        next = []

        for t in queue:
            expand(next, t, teas, scores)

        next.sort()
        queue = next[:len(forbiddens)+1]
    

    # Find lowest score not in forbidden
    for t in queue:
        if t.tea not in forbiddens:
            return t.score






if __name__ == '__main__':
    # Read number of test cases
    num_cases = int(input())

    for tc in range(1, num_cases + 1):
        # Read number of friends, number of forbidden teas, and number of options
        num_friends, num_forbidden, num_options = map(int, input().split())

        # Read the friends' preferences
        teas = [input().replace('\r', '') for _ in range(num_friends)]

        # Read the forbidden teas
        forbiddens = [input().replace('\r', '') for _ in range(num_forbidden)]

        print("Case #%d: %d" % (tc, count_complaints(teas, forbiddens)))
