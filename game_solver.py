#solver for rush hour:

#load current board,
#loop over all the cars in the board and find if they are moveable,
#as soon as you find the first moveable car, move it in one of the directions and store as new game state
#update the move made into a steps list
#maybe sth like [new game state, next step made]
#recurse on this game state 
#if solution found then return the steps list 
#if no solution found move on to next direction of movement for car
#if not possible or no solution then move onto next car
#lastly return None


#for board generation:
#place the 'bug' at the rightmost on the third row,
#place cars A-I in the board wherever possible randomly
#shuffle them around by selecting one car at random and making one random move 
#set difficulty by putting an upper bound on the number of moves,
#if number of moves not reachable regenerate? until you reach the move counrt and intitalise it as your first state.

#maybe save the states so it can be used as the solver too??

#eventually try adding cutouts(blocks) into the board, maybe as part of another level
