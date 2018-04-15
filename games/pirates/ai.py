# This is where you build your AI for the Pirates game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->>
# you can add additional import(s) here
from huepy import info, bad, good, run, bg
import heapq

WATER = 'water'
LAND = 'land'
SHIP = 'ship'
CREW = 'crew'
# <<-- /Creer-Merge: imports -->>


class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        # <<-- Creer-Merge: get-name -->>
        return "btw_i_use_arch"
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        # <<-- Creer-Merge: start -->>
        # replace with your start logic
        self.sea_men = []
        self.land_men = []
        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        # <<-- Creer-Merge: game-updated -->>
        # replace with your game updated logic
        self.sea_men = [
            x for x in self.player.units
            if x.tile and x.ship_health > 0
        ]
        self.land_men = [
            x for x in self.player.units
            if x.tile and x.ship_health == 0
        ]
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        # <<-- Creer-Merge: end -->>
        # replace with your end logic
        pass
        # <<-- /Creer-Merge: end -->>

    def print_stats(self):
        print(run(bg("Turn #{}".format(self.game.current_turn))))
        self.player.output_stats()

    def run_turn(self):
        # <<-- Creer-Merge: runTurn -->>
        # Put your game logic here for runTurn
        self.print_stats()

        self.sea_starter()

        self.matey_maintenence()

        self.pirate_propagate()

        self.all_aboard()

        return True
        # <<-- /Creer-Merge: runTurn -->>

    # <<-- Creer-Merge: functions -->>
    # if you need additional functions for your AI you can add them here

    def sea_starter(self):
        if not self.player.units:
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)
        elif self.player.units[0].ship_health == 0:
            self.player.port.spawn(SHIP)
        else:
            for _ in range(self.player.gold//200):
                self.player.port.spawn(CREW)

        if self.get_neutrals():
            self.capture_ship([self.sea_men[0]], self.get_neutrals())

    def pirate_propagate(self):
        # Add attackers
        attackers = []
        if len(self.sea_men) > 1:
            for pawn in self.sea_men[1:]:
                attackers.append(pawn)
            print(info("There are {} attackers".format(len(attackers))))

        for fighter in attackers:
            fighter.log("Yar har!")
            enemy_units = [u for u in self.player.opponent.units]
            self.attack_ship([fighter], enemy_units)

    def matey_maintenence(self):
        for pawn in self.sea_men:
            if pawn.ship_health < 10:
                self.heal(pawn)
                pawn.log("Healing time!")
            if pawn.gold >= 600:
                self.drop_off(pawn)
                pawn.log("Dropping dosh!")

    def all_aboard(self):
        # Move units to adjacent ships
        port_crew = [x for x in self.land_men if x.tile.port]
        port_ships = [
            x for x in self.sea_men
            if x.tile in self.player.port.tile.get_neighbors()
        ]
        if port_ships:
            least_ship = port_ships[0]
            for x in port_ships[1:]:
                if x.crew < least_ship.crew:
                    least_ship = x.crew
            for crew in port_crew:
                crew.move(least_ship.tile)

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
        target_tiles = [t.tile for t in targets if t.tile is not None]
        target_neighbors = [n for t in target_tiles for n in t.get_neighbors()]

        if not self.move([u.tile for u in units], target_neighbors):
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
        target_tiles = [t.tile for t in targets]
        target_neighbors = [n for t in target_tiles for n in t.get_neighbors()]

        if not self.move([u.tile for u in units], target_neighbors):
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
        Also deposits currency.

        :param unit: The unit to heal.

        :returns: True if the action has been completed, False if still in progress.
        :rtype: bool
        """
        if self.move_to_port(unit):
            unit.rest()
            return unit.ship_health == 20 and unit.crew_health == 4 * unit.crew
        return False

    def drop_off(self, unit):
        if self.move_to_port(unit):
            unit.deposit()
            return True
        return False

    def move_to_port(self, unit):
        """
        Moves a target to the port.

        :param unit: The unit to move.

        :returns: True if the action has been completed, False if still in progress.
        :rtype: bool
        """
        port_neighbors = [t for t in self.player.port.tile.get_neighbors()]

        if not self.move([unit.tile], port_neighbors):
            return False

        if unit.tile.has_neighbor(self.player.port.tile):
            return True

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
        if start is None:
            return False
        unit = start.unit
        if unit.tile in dst:
            return True
        if unit.acted:
            return False

        for _ in range(unit.moves):
            if not path:
                return True
            if not unit.move(path.pop(0)):
                return False
        return False

    def get_tile_neighbors(self, tile):
        """
        Collects all of neighbors surrounding a tile with no restrictions.
        """
        return [x for x in tile.get_neighbors()
                if x.type == "water"
                and (x.port is None or self.player.port == x.port)
                and not x.unit]

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

    def register_ship(self, crew_required):
        port_unit = self.player.port.tile.unit
        if port_unit and port_unit.ship_health > 0:
            # if ship on port
            crew_needed = crew_required - port_unit.crew
            if crew_needed > 0:
                self.ship_queue[port_unit] = crew_needed
                # returns the ship unit if built all crew needed, False if not
                return self.build()
        else:
            # create ship
            self.player.port.spawn(SHIP)

    # <<-- /Creer-Merge: functions -->>
