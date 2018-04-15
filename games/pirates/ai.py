# This is where you build your AI for the Pirates game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> 
# you can add additional import(s) here

import heapq

from .utils import pathing

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

        if not self.player.units:
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)
        elif self.player.units[0].ship_health == 0:
            self.player.port.spawn(SHIP)
        elif self.get_neutrals():
            self.capture_ship([self.player.units[0]], self.get_neutrals())
        if self.player.units:
            print("   {}".format(self.player.units[0].crew))

        for u in self.player.units[1:]:
            if u.tile:
                self.heal(u)

        return True
        # <<-- /Creer-Merge: runTurn -->>
    
    # <<-- Creer-Merge: functions -->> 
    # if you need additional functions for your AI you can add them here

    def get_neutrals(self):
        """
        Filters `game.units` to find units with no owner (merchants and empty ships).
        """
        return [u for u in self.game.units if u.owner is None]

    def attack_ship(self, units, targets):
        """
        Makes progress toward attacking a target ship.

        Once this function returns successfully, one of the targets will be destroyed.

        :param units: The friendly units available to attack.
        :param targets: The list of units to try to attack.

        :returns: True if the action has been completed, False if still in progress.
        :rtype: bool
        """
        if not self.move([u.tile for u in units], [t.tile for t in targets]):
            return False
        
        for unit in units:
            for target in targets:
                if unit.tile.has_neighbor(target.tile):
                    unit.attack(target.tile, SHIP)
                    return True
        return False

    def capture_ship(self, units, targets, split=1):
        """
        Makes progress toward capturing a target ship.
        
        Once this function returns successfully, the captured unit will be owned by the player.

        :param units: The friendly units available to capture.
        :param target: The list of units to try to capture.
        :param split: How many units should be placed on the captured ship.

        :returns: True if the action has been completed, False if still in progress.
        :rtype: bool
        """

        if not self.move([u.tile for u in units], [t.tile for t in targets]):
            return False

        for unit in units:
            for target in targets:
                if unit.tile.has_neighbor(target.tile):
                    if target.crew > 0:
                        unit.attack(target.tile, CREW)
                        break
                    else:
                        b = unit.split(target.tile, split)
                        return b

        return False

    def heal(self, unit):
        """
        Moves a target to the port and heals it back to full health.

        :param unit: The unit to heal.
        
        :returns: True if the action has been completed, False if still in progress.
        :rtype: bool
        """
        if not self.move([unit.tile], [self.player.port.tile]):
            return False

        if unit.tile.has_neighbor(self.player.port.tile):
            unit.rest()
            return unit.ship_health == 20 and unit.crew_health == 4 * unit.crew
        return False

    def move(self, src, dst):
        """
        Finds the minimal-cost path from one of the src to one of dst and moves those units.
        
        :param src: A list source tiles containing units.
        :param dst: A list of destination tiles.

        :returns: True if the action has been completed, False if still in progress.
        :rtype: bool
        """
        start, path = self.find_path(src, dst)
        if not path:
            return False
        unit = start.unit
        while path and not any(unit.tile.has_neighbor(t) for t in dst):
                if not unit.move(path.pop(0)):
                    return False
        return True

    def get_tile_neighbors(self, tile):
        """
        Collects all of neighbors surrounding a tile with no restrictions.
        """
        return [x for x in tile.get_neighbors() 
            if x.type == "water" and (x.port == None or self.player.port == x.port)]

        # return tile.get_neighbors()

    def find_path(self, start_tiles, goal_tiles, 
            get_neighbors=None,
            g_func=lambda x, y: 1, f_func=lambda x, y: 0):
        """
        Given a list of starting locations and a list of ending locations,
        find the shortest path between them. Uses a priority queue to
        do Uniform Cost Search (think Breadth First Search, but with movement
        cost included).
        """
        if not get_neighbors:
            get_neighbors = self.get_tile_neighbors
        path = []
        frontier = [(0, x) for x in start_tiles]
        path_from = dict()
        closed = set()

        g_score = {x: 0 for x in start_tiles}
        f_score = {x: g_score[x] + f_func(x, goal_tiles) for x in start_tiles}
        heapq.heapify(frontier)

        while frontier:
            _weight, working_tile = heapq.heappop(frontier)

            if working_tile in goal_tiles:
                current = working_tile
                path = [current]

                while path_from.get(current):
                    current = path_from.get(current)
                    if current not in start_tiles:
                        path.append(current)
                path.reverse()

                return current, path

            closed.add(working_tile)

            for neighbor in get_neighbors(working_tile):
                if neighbor in closed:
                    continue

                new_g = g_score[working_tile] + g_func(working_tile, neighbor)

                if new_g < g_score.get(neighbor, 1000000):
                    g_score[neighbor] = new_g
                    f_score[neighbor] = new_g + f_func(working_tile, goal_tiles)
                    path_from[neighbor] = working_tile
                    heapq.heappush(frontier, (f_score[neighbor], neighbor))
        return None, []

    # <<-- /Creer-Merge: functions -->>
