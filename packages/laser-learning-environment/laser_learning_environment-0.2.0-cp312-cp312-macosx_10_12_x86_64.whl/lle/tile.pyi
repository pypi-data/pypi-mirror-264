from typing import Optional, final
from .direction import Direction
from .types import AgentId

class Tile:
    agent: Optional[int]
    """The id of the agent currently standing on the tile, if any."""

@final
class Gem(Tile):
    is_collected: bool
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

@final
class Laser(Tile):
    is_on: bool
    is_off: bool
    agent_id: AgentId
    """The id of the agent that can block the laser."""
    direction: Direction
    """The direction of the laser beam."""
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

@final
class LaserSource(Tile):
    agent_id: AgentId
    """The id of the agent that can block the laser."""
    direction: Direction
    """The direction of the laser beam.."""
    def set_agent_id(self, agent_id: AgentId):
        """Change the 'colour' of the laser to the one of the agent given as argument."""
    def turn_on(self):
        """Turn the laser on."""
    def turn_off(self):
        """Turn the laser off."""
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
