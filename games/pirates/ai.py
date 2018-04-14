# This is where you build your AI for the Pirates game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> 
# you can add additional import(s) here
CREW = 'crew'
SHIP = 'ship'
# <<-- /Creer-Merge: imports -->>


class AI(BaseAI):
    def get_name(self):
        # <<-- Creer-Merge: get-name -->> 
        return "btw_i_use_arch"
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        # <<-- Creer-Merge: start -->> 
        # replace with your start logic
        self.ship = None
        self.target = None
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
        print(self.game.current_turn)

        if not self.player._units:
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)
        elif self.player._units[0]._ship_health == 0:
            self.player.port.spawn(SHIP)
        elif self.get_merchants():
            self.capture_ship(self.player._units[0], [self.nearest_merchant(self.player._units[0])])
        if self.player._units:
            print("   {}".format(self.player._units[0]._crew))

        return True
        # <<-- /Creer-Merge: runTurn -->>

    def sq_distance(self, a, b):
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


    def nearest_merchant(self, unit):
        ms = self.get_merchants()
        if not ms:
            return None

        x = self.sq_distance(unit.tile, ms[0].tile)
        result = ms[0]
        for m in ms[1:]:
            d = self.sq_distance(unit.tile, m.tile)
            if d < x:
                x = d
                result = m

        return result
        

    def get_merchants(self):
        return [u for u in self.game.units if u.owner is None]

    def attack_ship(self, unit, targets):
        pass

    def capture_ship(self, unit, targets):
        """
        Makes progress toward capturing a target ship.

        :param unit: The friendly unit.
        :param target: The list of units to try to capture.

        :returns: True if the action has been completed, False if still in progress.
        :rtype: bool
        """

        path = self.find_path(unit.tile, [t.tile for t in targets][0], unit)
        while path and not any(unit.tile.has_neighbor(t.tile) for t in targets):
            if not unit.move(path.pop(0)):
                return False

        for target in targets:
            if unit.tile.has_neighbor(target.tile):
                if target.crew > 0:
                    unit.attack(target.tile, CREW)
                    break
                else:
                    b = unit.split(target.tile, 1)
                    print(b)
                    return b

        return False

    def heal(self, unit):
        pass

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
