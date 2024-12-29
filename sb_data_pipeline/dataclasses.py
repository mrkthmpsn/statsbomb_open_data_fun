"""
Dataclasses for Statsbomb data 'pipeline'

Most of this file is devoted to creating a custom kloppy EventFactory (which sadly required custom versions of all kloppy dataclasses)
"""

from dataclasses import dataclass
from enum import Enum

from kloppy.domain import EventFactory, create_event
from kloppy.domain import (
    PassEvent,
    ShotEvent,
    GenericEvent,
    TakeOnEvent,
    RecoveryEvent,
    MiscontrolEvent,
    CarryEvent,
    DuelEvent,
    InterceptionEvent,
    ClearanceEvent,
    FormationChangeEvent,
    BallOutEvent,
    PlayerOnEvent,
    PlayerOffEvent,
    FoulCommittedEvent,
    CardEvent,
    SubstitutionEvent,
    GoalkeeperEvent,
)
from kloppy.domain.models.event import PressureEvent


# With the exception of shot events, the dataclass and event factory code are
# replications of the kloppy standard code, with the addition of `possession`
# as an integer field/kwarg
@dataclass(repr=False)
class StatsBombPassEvent(PassEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombShotEvent(ShotEvent):
    possession: int = None
    statsbomb_xg: float = None


@dataclass(repr=False)
class StatsBombGenericEvent(GenericEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombRecoveryEvent(RecoveryEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombMiscontrolEvent(MiscontrolEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombTakeOnEvent(TakeOnEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombCarryEvent(CarryEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombInterceptionEvent(InterceptionEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombClearanceEvent(ClearanceEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombDuelEvent(DuelEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombFormationChangeEvent(FormationChangeEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombBallOutEvent(BallOutEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombPlayerOnEvent(PlayerOnEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombPlayerOffEvent(PlayerOffEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombCardEvent(CardEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombFoulCommittedEvent(FoulCommittedEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombSubstitutionEvent(SubstitutionEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombGoalkeeperEvent(GoalkeeperEvent):
    possession: int = None


@dataclass(repr=False)
class StatsBombPressureEvent(PressureEvent):
    possession: int = None


class StatsBombEventFactory(EventFactory):
    def build_pass(self, **kwargs) -> StatsBombPassEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombPassEvent, **kwargs)

    def build_shot(self, **kwargs) -> StatsBombShotEvent:
        kwargs["statsbomb_xg"] = (
            kwargs["raw_event"].get("shot", {}).get("statsbomb_xg", 0)
        )
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombShotEvent, **kwargs)

    def build_generic(self, **kwargs) -> StatsBombGenericEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombGenericEvent, **kwargs)

    def build_recovery(self, **kwargs) -> StatsBombRecoveryEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombRecoveryEvent, **kwargs)

    def build_miscontrol(self, **kwargs) -> StatsBombMiscontrolEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombMiscontrolEvent, **kwargs)

    def build_take_on(self, **kwargs) -> StatsBombTakeOnEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombTakeOnEvent, **kwargs)

    def build_carry(self, **kwargs) -> StatsBombCarryEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombCarryEvent, **kwargs)

    def build_interception(self, **kwargs) -> StatsBombInterceptionEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombInterceptionEvent, **kwargs)

    def build_clearance(self, **kwargs) -> StatsBombClearanceEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombClearanceEvent, **kwargs)

    def build_duel(self, **kwargs) -> StatsBombDuelEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombDuelEvent, **kwargs)

    def build_formation_change(self, **kwargs) -> StatsBombFormationChangeEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombFormationChangeEvent, **kwargs)

    def build_ball_out(self, **kwargs) -> StatsBombBallOutEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombBallOutEvent, **kwargs)

    def build_player_on(self, **kwargs) -> StatsBombPlayerOnEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombPlayerOnEvent, **kwargs)

    def build_player_off(self, **kwargs) -> StatsBombPlayerOffEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombPlayerOffEvent, **kwargs)

    def build_card(self, **kwargs) -> StatsBombCardEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombCardEvent, **kwargs)

    def build_foul_committed(self, **kwargs) -> StatsBombFoulCommittedEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombFoulCommittedEvent, **kwargs)

    def build_substitution(self, **kwargs) -> StatsBombSubstitutionEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombSubstitutionEvent, **kwargs)

    def build_goalkeeper_event(self, **kwargs) -> StatsBombGoalkeeperEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombGoalkeeperEvent, **kwargs)

    def build_pressure_event(self, **kwargs) -> StatsBombPressureEvent:
        kwargs["possession"] = kwargs["raw_event"]["possession"]
        return create_event(StatsBombPressureEvent, **kwargs)


class StatsbombPlayerPosition(Enum):

    def __init__(self, statsbomb_position, general_position, position_group):
        self.statsbomb_position = statsbomb_position
        self.general_position = general_position
        self.position_group = position_group

    LEFT_CENTER_BACK = ("Left Center Back", "Center Back", "Defender")
    RIGHT_CENTER_FORWARD = ("Right Center Forward", "Center Forward", "Forward")
    LEFT_BACK = ("Left Back", "Full Back", "Defender")
    RIGHT_CENTER_BACK = ("Right Center Back", "Center Back", "Defender")
    LEFT_CENTER_MIDFIELD = ("Left Center Midfield", "Center Midfield", "Midfielder")
    RIGHT_CENTER_MIDFIELD = ("Right Center Midfield", "Center Midfield", "Midfielder")
    LEFT_CENTER_FORWARD = ("Left Center Forward", "Center Forward", "Forward")
    RIGHT_BACK = ("Right Back", "Full Back", "Defender")
    GOALKEEPER = ("Goalkeeper", "Goalkeeper", "Goalkeeper")
    RIGHT_MIDFIELD = ("Right Midfield", "Wide Midfielder", "Midfielder")
    LEFT_MIDFIELD = ("Left Midfield", "Wide Midfielder", "Midfielder")
    LEFT_WING = ("Left Wing", "Winger", "Forward")
    RIGHT_WING = ("Right Wing", "Winger", "Forward")
    CENTER_DEFENSIVE_MIDFIELD = (
        "Center Defensive Midfield",
        "Defensive Midfielder",
        "Midfielder",
    )
    CENTER_FORWARD = ("Center Forward", "Center Forward", "Forward")
    RIGHT_DEFENSIVE_MIDFIELD = (
        "Right Defensive Midfield",
        "Defensive Midfielder",
        "Midfielder",
    )
    LEFT_DEFENSIVE_MIDFIELD = (
        "Left Defensive Midfield",
        "Defensive Midfielder",
        "Midfielder",
    )
    CENTER_ATTACKING_MIDFIELD = (
        "Center Attacking Midfield",
        "Attacking Midfielder",
        "Midfielder",
    )
    CENTER_MIDFIELD = ("Center Midfield", "Center Midfielder", "Midfielder")
    CENTER_BACK = ("Center Back", "Center Back", "Defender")
    LEFT_WING_BACK = ("Left Wing Back", "Wing Back", "Defender")
    RIGHT_WING_BACK = ("Right Wing Back", "Wing Back", "Defender")
    RIGHT_ATTACKING_MIDFIELD = (
        "Right Attacking Midfield",
        "Attacking Midfielder",
        "Midfielder",
    )
    LEFT_ATTACKING_MIDFIELD = (
        "Left Attacking Midfield",
        "Attacking Midfielder",
        "Midfielder",
    )
    NONE = ("None", "NA", "NA")
