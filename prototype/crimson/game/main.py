import pydantic
import networkx as nx
from enum import Enum

from sunshot.models import Account
from crimson.models import Contract
from crimson.game.cards import Card
from crimson.game import cards

# Starting Game Conditions

STARTING_DECK: list[Card] = ([]
    + [cards.REACTOR_CARD] * 3
    + [cards.THRUSTER_CARD] * 2
    + [cards.DEFENSE_CARD] * 2
    + [cards.DAMAGE_CARD] * 2
    + [cards.MISS_CARD] * 1
)

STARTING_CREDITS = 2

MAX_OPEN_CONTRACTS = 8

class ShipUpgrade:
    """A component added to the ship."""




class State(Enum):
    """Phases of a player's turn."""

    DECIDE_TO_DEFEND_OR_CONTRACT = 0 # Player decides to

    CONTRACT_SELECTION_PHASE = 1 # Player can pick a contract or stay in base
    CONTRACT_REWARD_OFFER_PHASE = 2 # Player can offer rewards to other players in return for their assistance
    CONTRACT_EXECUTION_PHASE = 3 # Player begins playing from their hand
    CONTRACT_PARTNER_EXECUTION_PHASE = 4 # Partners who agreed to join now play their hand
    BUY_PHASE = 5 # Player can purchase crew, ship parts, etc.

    SELECT_SECRET_OBJECTIVE = 6 # Player can pick a secret objective for staying at base.

class Action(Enum):
    """Actions players can take."""

    PURSUE_CONTRACT = 0 # Player decides to pursue contract
    DEFEND_BASE = 1 # Player decides to stay at base
    PAY_TO_TERMINATE_CONTRACT = 2 # Player can pay to terminate a contract from board


class PhaseData(pydantic.BaseModel):
    """Information about the next move."""

    target_player: list[int] # A stack for stuff like negotiation
    phase: State
    possible_actions: list[Action]


# Create a graph where the nodes are game state, and the edges are actions
# players can perform to get to different game state. Starting point is always
# DECIDE_TO_DEFEND_OR_CONTRACT. The edge's method attribute is the string name
# of a method of GameInstance to perform.
STATE_ACTION_GRAPH = nx.DiGraph()
STATE_ACTION_GRAPH.add_nodes_from(list(State))
# TODO: fill out the rest



class GameInstance:
    """A running instance of the game."""

    def __init__(self, players: list[Account]):

        # Order of players + player hands
        self.players = players
        self.scores: dict[Account, int] = {player: 0 for player in players}
        self.credits: dict[Account, int] = {player: STARTING_CREDITS for player in players}
        self.ship_states: dict[Account, list[ShipUpgrade]] = {player: [] for player in players}
        self.decks: dict[Account, list[Card]] = {player: STARTING_DECK.copy() for player in players}
        self.discard: dict[Account, list[Card]] = {player: [] for player in players}
        self.trash: dict[Account, list[Card]] = {player: [] for player in players}
        self.hands: dict[Account, list[Card]] = {player: [] for player in players}

        # Contracts
        self.closed_contracts: list[Contract] = list(Contract.objects.filter(playable=True).order_by('?')[:100]) # TODO: handle paywalls
        self.open_contracts: list[Contract] = [self.closed_contracts.pop() for _ in range(MAX_OPEN_CONTRACTS)]

        # Game State
        self.phase_number = 0 # Turn # = phase number // len(players)

        self.current_phase: PhaseData = PhaseData(
            target_player=[0],
            phase=State.DECIDE_TO_DEFEND_OR_CONTRACT,
            possible_actions=[Action.PURSUE_CONTRACT, Action.DEFEND_BASE, Action.PAY_TO_TERMINATE_CONTRACT]
        )


    def get_next_move(self, action: Action) -> bool:
        """Get information about what player , etc."""
        if action not in self.current_phase.possible_actions:
            return False

        action_state_map: dict[Action, list[State]] = {
            Action.PURSUE_CONTRACT: [State.CONTRACT_SELECTION_PHASE],
            Action.DEFEND_BASE: [State.SELECT_SECRET_OBJECTIVE, State.BUY_PHASE]
        }
