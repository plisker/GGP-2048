/*
 * TODO
 * - Turn this into a proper MCTS-UCB program
 *      > Right now multiRandomRun simply runs by running a given 'n' number of
 *        of simulations on all of the children of the root node. This program
 *        doesn't implement the tree-building, exploration-exploitation
 *        tradeoffs, or back-propagation features of MCTS
 *			 
 *			(1) Implement tree structure, where nodes contain at least the info
 *				`numRuns`, (cumulative?) `score`, and children generation (that
 * 				 should be trivial, since all children are just the results of 
 *				 four moves the )
 *					(A) Through all iterations, we need to somehow save the info
 *						of what our expanded tree so far is
 *					(B) Save path chosen by treePolicy at each iteration of MCTS
 *						for the backpropagation step
 *					(C) Figure out best thing to do in the expansion step of the algorithm
 *
 *
 */


function randomMove () {
	return Math.floor(Math.random() * 4
}

// Constructor for node object for our MCTS search tree, each of which contains 
// a state (a grid), the number of times it has been selected for simulations,
// its value, and a method for retrieving its children.
function Node (grid) {
    this.grid = grid;
    this.numSimulations = 0;
    this.value = 0;
    this.expandedChildren = [];
    this.getChild = function(move) {
    	child = new Node(moveAndAddRandomTiles(this.grid, move));
    	return child
    };
    this.getAllChildren = function() {
    	children = []
    	for(i=0;i<4;i++){
    		children.push(this.getChild(i))
    	}
    	return children
    };
}

// MCTS with UCB tree policy
// `runs` now defines total simulations, regardless of which move.
function mcts(grid, runs, debug) {
	rootNode = new Node(grid)
	numSimulations = 0
	for (i=0;i<runs;i++){
		selection = UCT(rootNode)

		selection.node.expandChildren = selection.node.getAllChildren()

		result = randomRun(selection.node.grid, randomMove())

		for node in selection.path {

		}
	}
}

function UCB(node,totalNumSimulations){
	if (node.numSimulations == 0) {
		return Infinity
	}
	else {
		return node.value + Math.sqrt((2 * Math.log(totalNumSimulations))/node.numSimulations)
	}
}

// return selected node and path to that node
function UCT(rootNode, totalNumSimulations) {

}



/*******************************************************************************	
	getBestMove runs 'runs' random-move simulations on each of the four valid moves
	and returns the move with the highest score and said score.
*******************************************************************************/
function getBestMove(grid, runs, debug) {
		
	// Highest scoring move so far. Initialize to dummy value -1.
	var bestMove = -1;
	
	// Highest score so far
	var bestScore = 0;

	// Run simulations for each of the four valid moves
	for (var i=0; i<4; i++) {
		
		// Run `runs` random-move simulations starting with move `i`
		var result = multiRandomRun(grid, i, runs);
		
		// Save if best score so far. Higher moves win ties.
		if (result.score >= bestScore) {
			bestScore = result.score;
			bestMove = i;
			bestAvgMoves = result.avg_moves;
		}
		
		// Debugging print
		if (debug) {
			console.log('Move ' + moveName(i) + ": Extra score - " + score);
		}
	}

	// More debugging prints
	if (debug) {
		console.log('Move ' + moveName(bestMove) + ": Extra score - " + bestScore + " Avg number of moves " + bestAvgMoves);
		if(!grid.movesAvailable()) {
			console.log('bug2');	
		}	
		if (debug && bestMove == -1) {
			console.log('ERROR...'); 
			errorGrid = grid.clone();
		} 
	}			
	
	return {move: bestMove, score: bestScore};
}

/*******************************************************************************	
	multiRandomRun implements `runs` number of random-move simulations 
	starting from current state `grid` until terminal state, i.e. the game ends.
	Returns the average score and the average number of moves in the simulation.
*******************************************************************************/
function multiRandomRun(grid, move, runs) {
	var total = 0.0;
	var min = 1000000;
	var max = 0;
	var total_moves = 0;
	
	for (var i=0; i<runs; i++) {
		var result = randomRun(grid, move);
		var score = result.score;
		if (score == -1) return -1;
			
		total += score;
		total_moves += result.moves;
		if (score < min) min = score;
		if (score > max) max = score;
	}
	
	var avg = total / runs;
	var avg_moves = total_moves / runs;

	return {score: avg, avg_moves:avg_moves};
}

/*******************************************************************************
  randomRun runs one random-move game simulation starting from start state 
  `grid` until game finishes.
 ******************************************************************************/
function randomRun(grid, move) {	
	var g = grid.clone();
	var score = 0;
	var result = moveAndAddRandomTiles(g, move);
	if (!result.moved) {
		return -1; // can't start
	}	
	score += result.score;

	// run til we can't
	var moves=1;
	while (g.movesAvailable()) {

		var result = g.move(Math.floor(Math.random() * 4));
		if (!result.moved) continue;
		
		score += result.score;
		g.addRandomTile();
		moves++;
	}

	return {score:score, moves:moves};
}

function moveAndAddRandomTiles(grid, direction) {
	var result = grid.move(direction);
	if (result.moved) grid.addRandomTile();
	return result;
}

function AI_getBest(grid, debug) {
	var runs = document.getElementById('run-count').value;
    return getBestMove(grid, runs, debug);  
}

/*******************************************************************************
	moveName returns English version of numerically encoded moves
	Valid moves up, right, down, left, are mapped to integers 0, 1, 2 ,3 respectively
*******************************************************************************/
function moveName(move) {
 return {
    0: 'up',
    1: 'right',
    2: 'down',
    3: 'left'
  }[move];
}