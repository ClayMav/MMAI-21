# This is where you build your AI for the Pirates game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> 
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    def get_name(self):
        # <<-- Creer-Merge: get-name -->> 
        return "btw_i_use_arch"
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        # <<-- Creer-Merge: start -->> 
        # replace with your start logic
        pass
        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        # <<-- Creer-Merge: game-updated -->> 
        # replace with your game updated logic
        pass
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        # <<-- Creer-Merge: end -->> 
        # replace with your end logic
        pass
        # <<-- /Creer-Merge: end -->>

    def run_turn(self):
        # <<-- Creer-Merge: runTurn -->> 
        # Put your game logic here for runTurn

        return True
        # <<-- /Creer-Merge: runTurn -->>

    def find_path(self, start, goal, unit):

        if start == goal:
            # no need to make a path to here...
            return []

        # queue of the tiles that will have their neighbors searched for 'goal'
        fringe = []

        # How we got to each tile that went into the fringe.
        came_from = {}

        # Enqueue start as the first tile to have its neighbors searched.
        fringe.append(start)

        # keep exploring neighbors of neighbors... until there are no more.
        while len(fringe) > 0:
            # the tile we are currently exploring.
            inspect = fringe.pop(0)

            # cycle through the tile's neighbors.
            for neighbor in inspect.get_neighbors():
                # if we found the goal, we have the path!
                if neighbor == goal:
                    # Follow the path backward to the start from the goal and return it.
                    path = [goal]

                    # Starting at the tile we are currently at, insert them retracing our steps till we get to the starting tile
                    while inspect != start:
                        path.insert(0, inspect)
                        inspect = came_from[inspect.id]
                    return path
                # else we did not find the goal, so enqueue this tile's neighbors to be inspected

                # if the tile exists, has not been explored or added to the fringe yet, and it is pathable
                if neighbor and neighbor.id not in came_from and neighbor.is_pathable(unit):
                    # add it to the tiles to be explored and add where it came from for path reconstruction.
                    fringe.append(neighbor)
                    came_from[neighbor.id] = inspect

        # if you're here, that means that there was not a path to get to where you want to go.
        #   in that case, we'll just return an empty path.
        return []

    # <<-- Creer-Merge: functions -->> 
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>
