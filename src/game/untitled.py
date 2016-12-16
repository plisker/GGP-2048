def heuristic(grid):
	score = 0
	for corner in ["top-left","top-right","bottom-left","bottom-right"]:
		corner_score = 0
		for i in range(len(grid) - 1):
			for j in range(len(grid[0]) - 1):
				if grid[i][j] == 0:
					score += EMPTYCONSTANT
				if corner == "top-left":
					if grid[i][j] >= grid[i][j+1]:
						score += 1
					if grid[i][j] >= grid[i+1][j]:
						score += 1
				elif corner == "top-right":
					if grid[i][j] <= grid[i][j+1]:
						score += 1
					if grid[i][j] >= grid[i+1][j]:
						score += 1
				elif corner == "bottom-left":
					if grid[i][j] >= grid[i][j+1]:
						score += 1
					if grid[i][j] <= grid[i+1][j]:
						score += 1
				elif corner == "bottom-right":
					if grid[i][j] <= grid[i][j+1]:
						score += 1
					if grid[i][j] <= grid[i+1][j]:
						score += 1

		score = max([corner_score,score])

	score = score * HEURISTICCONSTANT
	# print "heuristic called: " + str(score)
	return score
