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
