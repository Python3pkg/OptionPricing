import numpy as np


class American:

	'''
	S: current stock price
	X: strike price
	r: risk-free rate
	sigma: volatility
	T: Time until maturity
	d: dividend yield
	'''

	def __init__(self, S, X, r, sigma, T, d = 0):
		self.X = X
		self.S = float(S)
		self.r = r
		self.sigma = sigma
		self.T = T
		self.d = d
		self.b = self.r - self.d


	# Cox-Ross-Rubenstein Binomial Pricing
	def CRR(self, option, steps):
		self.T = float(self.T)
		dt = round(self.T/steps, 5)
		v = self.r - self.d
		up = np.exp(self.sigma * np.sqrt(dt))
		down = np.exp(-self.sigma * np.sqrt(dt))
		p = (np.exp(v * dt) - down)/(up - down)

		# Binomial Price Tree
		val = np.zeros((steps + 1, steps + 1))
		val[0, 0] = self.S
		for i in range(1, steps + 1):
			val[i, 0] = val[i - 1, 0] * up
			for j in range(1, i + 1):
				val[i, j] = val[i - 1, j - 1] * down

		# Option value at each node
		price = np.zeros((steps + 1, steps + 1))
		for i in range(steps + 1):
			if option.lower() == "call":
				price[steps, i] = max(0, val[steps, i] - self.X)
			elif option.lower() == "put":
				price[steps, i] == max(0, self.X - val[steps, i])

		# Backward recursion for option price
		for i in range(steps - 1, -1, -1):
			for j in range(i + 1):
				if option.lower() == "call":
					price[i, j] = max(self.X-val[i,j], np.exp(-self.r*dt)*(p*price[i+1,j] + (1-p)*price[i+1,j+1]))
				elif option.lower() == "put":
					price[i, j] = max(val[i,j]-self.X, np.exp(-self.r*dt)*(p*price[i+1,j] + (1-p)*price[i+1,j+1]))

		return price[0, 0]

	# Quadratic Approximation
	def QuadApprox(self, option):
		return 0

	def FiniteDifference(self, option):
		return 0