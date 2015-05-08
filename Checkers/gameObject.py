# Generated by Creer at 09:17PM on May 08, 2015 UTC, git hash: '2071c4d66324aad8188edf8c95f4eff08dbda001'
# This is a simple class to represent the GameObject object in the game. You can extend it by adding utility functions here in this file.

from baseGameObject import BaseGameObject

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add addtional require(s) here
# <<-- /Creer-Merge: imports -->>

class GameObject(BaseGameObject):
    """ The class representing the GameObject in the Checkers game.

    An object in the game. The most basic class that all game classes should inherit from automatically.
    """

    def __init__(self, data):
        """ initializes a GameObject with basic logic as provided by the Creer code generator

        Args:
            data (dict): initialization data
        """
        BaseGameObject.__init__(self, data)

        # The following values should get overridden when delta states are merged, but we set them here as a reference for you to see what variables this class has.

        # Any strings logged will be stored here when this game object logs the strings. Intended for debugging.
        self.logs = []
        # A unique id for each instance of a GameObject or a sub class. Used for client and server communication. Should never change value after being set.
        self.id = ""



    def log(self, message):
        """ adds a message to this game object's log. Intended for debugging purposes.

        Args:
            message (str): A string to add to this GameObject's log. Intended for debugging.
        """
        return self._run_on_server('log', message=message)


    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you want to add any client side logic (such as state checking functions) this is where you can add them
    # <<-- /Creer-Merge: functions -->>