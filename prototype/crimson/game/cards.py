import pydantic

class Card(pydantic.BaseModel):
    """A card in a deck."""
    damage_provided: int = 0
    defense_provided: int = 0
    thruster_provided: int = 0
    reactor_provided: int = 0
    crew_provided: int = 0

    def effect(self):
        self.default_effect()

    def default_effect(self):
        """Default effect of playing this card."""
        if self.defense_provided:
            # Reduce damage by same ammount
            pass
        if self.thruster_provided:
            # Draw 3 cards
            pass
        if self.reactor_provided:
            # Add 2 more actions to current user
            pass


# Cards

DAMAGE_CARD = Card(damage_provided=1)
DEFENSE_CARD = Card(defense_provided=1)
THRUSTER_CARD = Card(thruster_provided=1)
REACTOR_CARD = Card(reactor_provided=1)
MISS_CARD = Card()
