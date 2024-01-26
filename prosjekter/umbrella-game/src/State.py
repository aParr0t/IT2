class State:
    def __init__(self):
        self.isEditing = True
        self.isFrozen = False

        self.visible_variables = set(
            [
                "isEditing",
                "isFrozen",
            ]
        )

        self.shortcut_variables = {
            "e": "isEditing",
            "f": "isFrozen",
        }

    def is_visible(self, name):
        return name in self.visible_variables
