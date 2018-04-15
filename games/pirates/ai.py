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

        self.skwardly_dogs = [
            x for x in self.player.opponent.units
            if x.type == "ship" and x.ship_health != 0
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

        self.matey_maintenence()

        self.sea_starter()

        self.booty_bodyguard()

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
        elif self.sea_men[0].crew == 1:
            self.sea_men[0].log('Restocking!')
            if self.move([self.sea_men[0]], [self.player.port.tile]):
                self.player.port.spawn(CREW)
                self.player.port.spawn(CREW)
                self.player.port.spawn(CREW)
                self.player.port.tile.unit.move(self.sea_men[0].tile)
        elif self.get_neutrals():
            self.capture_ship([self.sea_men[0]], self.get_neutrals())
            self.sea_men[0].log("Recruiting!")
        else:
            merchant_ports = [
                n for p in self.game.ports
                for n in p.tile.get_neighbors()
                if p.owner is None
            ]
            self.move([self.sea_men[0]], merchant_ports)

    def pirate_propagate(self):
        # Add attackers
        attackers = self.sea_men[1:]
        if attackers:
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
                    least_ship = x
            for crew in port_crew:
                crew.move(least_ship.tile)

    def booty_bodyguard(self):
        pass

    def get_neutrals(self):
        """
        Filters `game.units` to find units with no owner (merchants and empty
        ships).
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

        if not self.move(units, target_neighbors):
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
        target_tiles = [t.tile for t in targets if not t.tile.port]
        target_neighbors = [n for t in target_tiles for n in t.get_neighbors()]

        self.move(units, target_neighbors)

        for unit in units:
            for target in targets:
                if unit.tile.has_neighbor(target.tile):
                    if target.crew > 0:
                        unit.attack(target.tile, CREW)
                        break
                    else:
                        b = unit.split(target.tile, split)
                        return b
                elif unit.tile.in_range(target.tile, 3):
                    unit.attack(target.tile, SHIP)

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

    def move_to_port(self, unit, **kwargs):
        """
        Moves a target to the port.

        :param unit: The unit to move.

        :returns: True if the action has been completed, False if still in progress.
        :rtype: bool
        """
        port_neighbors = [t for t in self.player.port.tile.get_neighbors()]

        if not self.move([unit], port_neighbors, **kwargs):
            return False

        if unit.tile.has_neighbor(self.player.port.tile):
            return True

        return False

    def move(self, units, dst, **kwargs):
        """
        Finds the minimal-cost path from one of the src to one of dst and moves those units.

        :param src: A list source tiles containing units.
        :param dst: A list of destination tiles.

        :returns: True if the action has been completed, False if still in progress.
        :rtype: bool
        """
        kwargs.setdefault("g_func", self.ships_in_range)
        for unit in units:
            start, path = unit.find_path(dst, **kwargs)
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

    def ships_in_range(self, start, end):
        counter = 1
        for ship in self.skwardly_dogs:
            if start.in_range(ship.tile, 3):
                counter = counter + 2

        return counter

    # <<-- /Creer-Merge: functions -->>
