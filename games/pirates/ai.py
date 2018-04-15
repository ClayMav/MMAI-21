# This is where you build your AI for the Pirates game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> 
# you can add additional import(s) here
from collections import OrderedDict
from .utils import pathing
from termcolor import colored


WATER = 'water'
LAND = 'land'
SHIP = 'ship'
CREW = 'crew'
# <<-- /Creer-Merge: imports -->>


class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

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
        print(colored('[+]', 'red'), "Turn #{}".format(self.game.current_turn))

        if not self.player.units:
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)
        elif self.player.units[0].ship_health == 0:
            self.player.port.spawn(SHIP)
        else:
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)
            self.player.port.spawn(CREW)

        if self.get_neutrals():
            self.capture_ship([self.player.units[0]], self.get_neutrals())

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
        start, path = pathing.find_path(src, dst)
        if not path:
            return False
        unit = start.unit
        while path and not any(unit.tile.has_neighbor(t) for t in dst):
                if not unit.move(path.pop(0)):
                    return False
        return True

    # <<-- /Creer-Merge: functions -->>
