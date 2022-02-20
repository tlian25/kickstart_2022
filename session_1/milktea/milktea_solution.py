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
Step 1.
S_0 = ""
Runtime O(1)

Step 2.
for each binary string b_i in S_n-1, add b_i+"0" and b_i+"1" to S_n
Runtime O(M)

Step 3.
Filter out the best M+1 teas in S_n 
Runtime O(M(NP + logM))
    a. score binary string in S_n
        Runtime O(MNP)
    b. Sort binary strings and select M+1 of them
        Runtime O(M logM)

Step 4.
Repeat 2-3 until i reaches P (length of binary)


Step 5. 
Find best tea in S_p not in forbiddens set 
Runtime O(NMP)


Total Runtime O(MP(NP + logM))


N = size of preferences set
M = size of forbiddens set
P = length of binary string

Runtime: O(2^n)
'''

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



# Compare all teas in list
def score(prefix:str, teas:list) -> int:

    difference = 0
    for t in teas:
        difference += compare(prefix, t)

    return difference



# expand tea by appending 0 and 1
def expand(scoredteas:list, prefix:str, teas:list):
    zero = prefix + '0'
    one = prefix + '1'

    scoredteas.append(ScoredTea(score(zero, teas), zero))
    scoredteas.append(ScoredTea(score(one, teas), one))



def count_complaints(teas, forbiddens):

    L = len(teas[0])
    forbiddens = set(forbiddens)


    queue = [ ScoredTea(0, "") ]

    # Loop L times for length of tea string
    for _ in range(L):
        
        next = []

        for t in queue:
            expand(next, t.tea, teas)

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
