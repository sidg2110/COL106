import random
import math

# To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

# Pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

	'''
	In the worst case, q = N < (m/eps)^2.
	Therefore, in the worst case, log(q) < 2*log(m/eps)

	Therefore, space = O(k + n * log(m/eps))
			   time = O(n * log(m/eps))
	'''

# Pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)
	
	'''
	In the worst case, q = N < (m/eps)^2.
	Therefore, in the worst case, log(q) < 2*log(m/eps)

	Therefore, space = O(k + n * log(m/eps))
			   time = O(n * log(m/eps))
	'''

# Return appropriate N that satisfies the error bounds
def findN(eps,m):
	'''
	Consider the 26-nary representation of pattern to be S
	Consider the 26-nary representation of substring of text at position i to be T
	Consider a prime q belonging to set {2, 3, ...., N}
	Given that S != T, we need to find N such that the probability of (S mod q) = (P mod q) is less than eps
	Proof:
		S != T and S mod q = T mod q
	=>	|S - T| mod q = 0
	=>	prob <= (# (prime divisors of |S - T|)) / (pi(N)) <= eps
	=> 	(log(|S-T|)) / (N/(2*log(N))) <= eps

		Note that |S-T| <= 26^m
	
	=> (log(|S-T|)) / (N/(2*log(N))) <= (m * log(26)) / (N/(2*log(N))) = (2 * m * log(N) *log(26)) / (N) <= eps
	=> N/log(N) >= (2 * m * log(26)) / (eps)
	=> N/log(N) >= (10 * m)/(eps)
	

		N^(1/N) <= 2^(eps/10m)

		Now we need a function N(m, eps) which will satisfy the above inequality.
		Observing the required efficiencies and the inequality, I assume that the function contains terms of the form m/eps
		I first tried N = 10 * m/eps which fails the inequality
		I then tried N = 100 * (m/eps) which fails the inequality
		I then tried N = 100 * (m/eps)^2 which fails the inequality
		I then tried N = (100 * (m/eps))^2 which satisfies the inequality
		To tighten the bound, I then tried N = 100 * (m/eps) * log(100 * (m/eps)) which satisfies the inequality

		Therefore, I finally used N = 100 * (m/eps) * log(100 * (m/eps))

		Also, note that N is an integer. Thus, we take floor of the value. 
	
	=>	N = floor(100 * (m/eps) * log(100 * (m/eps))) + 1
	'''
	float_ans = 100*(m/eps)*math.log((100*(m/eps)), 2)
	return (math.floor(float_ans) + 1)

	# O(log(m/eps)) space and time

# Return sorted list of starting indices where p matches x
def modPatternMatch(q, p, x):
	n = len(x)				# O(log(n)) space
	m = len(p)				# O(log(m)) space
	ans = []
	pattern_hash = 0
	text_hash = 0
	# At any time, pattern_hash and text_hash take O(log(q)) space

	# To calculate the hash function of pattern and the hash function of m length substring [0,m-1] of text
	for i in range (0, m):	# This loop runs m times
		# ord() returns the ASCII code of character. To get the integer associated with any letter, we subtract the ASCII code of A. Therefore, A=0, B=1 and so on.	
		pattern_hash = (26 * pattern_hash + int(ord(p[i]) - ord('A'))%q)%q
		text_hash = (26*text_hash + int(ord(x[i]) - ord('A'))%q)%q
	# This loop takes O(m*log(q)) time

	# Text = ABCDEF
	# PAtterm = ABC
	# ABC = 26^2*A + 26^1 *B +26^0 * C
	# BCD

	if pattern_hash == text_hash:
		ans.append(0)
	
	k = (26 ** (m-1))%q		# O(log(q)) space	# O(log(m)) time
	
	# Iterating over the text and checking the equality of hash values at each index
	for i in range (1, n-m+1):		# Loop runs (n-m) times
		
		# Hash value at index i is calculated using hash value at index i-1. We "subtract" the letter at index i and "add" the letter at index i+m-1 
		
		subtract = (k * (int(ord(x[i-1]) - ord('A')))%q)%q		# Value associated with letter to be subtracted
		
		add = (int(ord(x[i+m-1]) - ord('A')))%q					# Value associated with letter to be added
		
		text_hash = ((26 * (text_hash - subtract)%q)%q + add)%q
		
		if text_hash == pattern_hash:
			ans.append(i)	
	# This loop takes O((n-m)*log(q)) space and since n > m, takes O(n*log(q)) time

	return ans

	'''
		Space Complexity: We are storing n, m, pattern_hash, text_hash, iterator, add, subtract and ans.
	=>	O(log(n) + log(m) + log(q) + log(q) + log(q) + log(q) + log(n) + k) space where k is the length of ans list
	=>	O(log(n) + log(q) + k) space (since n > m)

		Time Complexity: First loop takes O(m * log(q)) time and second loop takes O(n * log(q)) time
	=>	Since n > m, function takes O(n * log(q)) time
	'''

# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):

	n = len(x)		# O(log(n)) space
	m = len(p)		# O(log(m)) space
	ans = []
	pattern_hash = 0
	text_hash = 0

	# At any time, pattern_hash and text_hash take O(log(q)) space

	index = 0		# Index in the pattern at which the '?' is present. Let it be 0 initially
	
	# To calculate the hash function of pattern and the hash function of m length substring [0,m-1] of text
	# While calculating the hash value, we consider the '?' to be associated with 0 (i.e we skip this letter)	
	for i in range (0, m): # This loop runs m times
		if p[i] != '?':
			pattern_hash = (26*pattern_hash + int(ord(p[i]) - ord('A'))%q)%q
			text_hash = (26*text_hash + int(ord(x[i]) - ord('A'))%q)%q
		else:
			pattern_hash = 26 * pattern_hash
			text_hash = 26 * text_hash
			index = i
	# This loop takes O(m*log(q)) time

	if pattern_hash == text_hash:
		ans.append(0)

	'''
		Algorithm Idea:
		While calculating hash value of text substring we skip over the letter that occurs at 'index' position. 
	'''

	# k1, k2, k3 take O(log(q)) space

	if index != 0 and index != m-1:		# '?' does not appear at the start or end
		k1 = (26 ** (m-1))%q
		k2 = (26 ** (m-index))%q
		k3 = (26 ** (m-index-2))%q
	
		# In the current hash value of text,
		# Add: last letter of new substring and the skipped letter of previous substring
		# Subtract: first letter of previous substring and the letter to be skipped in the new substring
		
		for i in range (1, n-m+1):
			subtract = ((k1 * (int(ord(x[i-1]) - ord('A')))%q)%q + (k3 * (int(ord(x[i+index]) - ord('A')))%q))%q
			add = ((k2 * int(ord(x[i+index-1]) - ord('A'))%q)%q + int(ord(x[i+m-1]) - ord('A'))%q)%q
			text_hash = (26*((text_hash - subtract)%q)%q + add)%q
			if pattern_hash == text_hash:
				ans.append(i)
	
	elif index == 0:					# '?' appears at the start
		k3 = (26 ** (m-index-2))%q

		# In the current hash value of text,
		# Add: last letter of new substring
		# Subtract: letter to be skipped in the new substring
		
		for i in range (1, n-m+1):
			subtract = (k3 * (int(ord(x[i+index]) - ord('A')))%q)%q
			add = (int(ord(x[i+m-1]) - ord('A'))%q)
			text_hash = (26*((text_hash - subtract)%q)%q + add)%q
			if pattern_hash == text_hash:
				ans.append(i)

	elif index == m-1:					# '?' appears at the end
		k1 = (26 ** (m-1))%q
		k2 = (26 ** (m-index))%q
		
		# In the current hash value of text,
		# Add: skipped letter of previous substring
		# Subtract: first letter of previous substring
		
		for i in range (1, n-m+1):
			subtract = ((k1 * (int(ord(x[i-1]) - ord('A')))%q))%q
			add = ((k2 * int(ord(x[i+index-1]) - ord('A'))%q))%q
			text_hash = (26*((text_hash - subtract)%q)%q + add)%q
			if pattern_hash == text_hash:
				ans.append(i)

	# In every case,
	# Loop takes O((n-m)*log(q)) space and since n > m, takes O(n*log(q)) time

	return ans

	'''
		Space Complexity: We are storing n, m, pattern_hash, text_hash, iterator, add, subtract and ans.
	=>	O(log(n) + log(m) + log(q) + log(q) + log(q) + log(q) + log(n) + k) space where k is the length of ans list
	=>	O(log(n) + log(q) + k) space (since n > m)

		Time Complexity: First loop takes O(m * log(q)) time and second loop takes O(n * log(q)) time
	=>	Since n > m, function takes O(n * log(q)) time
	'''

print(modPatternMatch(1000000007, 'CD', 'ABCDE'))