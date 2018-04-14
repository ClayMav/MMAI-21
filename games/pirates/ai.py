# This is where you build your AI for the Pirates game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> 
# you can add additional import(s) here
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
        elif self.get_merchants():
            self.capture_ship([self.player.units[0]], [self.nearest_merchant(self.player.units[0])])
        if self.player.units:
            print("   {}".format(self.player.units[0].crew))

        for u in self.player.units[1:]:
            self.heal(u)

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

    def capture_ship(self, units, targets, split=1):
        """
        Makes progress toward capturing a target ship.

        :param unit: The friendly unit.
        :param target: The list of units to try to capture.

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
        if not self.move([unit.tile], [self.player.port.tile]):
            return False

        if unit.tile.has_neighbor(self.player.port.tile):
            return not unit.rest()

    def move(self, src, dst):
        start, path = pathing.find_path(src, dst)
        if not path:
            return False
        unit = start.unit
        while path and not any(unit.tile.has_neighbor(t) for t in dst):
                if not unit.move(path.pop(0)):
                    return False
        return True

    # <<-- Creer-Merge: functions -->> 
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>
