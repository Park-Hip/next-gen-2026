"""The simulated ("giả lập") org tree and the people who ask."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    id: str
    name: str
    unit: str
    company: str
    path: tuple[str, ...]
    roles: tuple[str, ...]
    hr: str


@dataclass(frozen=True)
class Org:
    parent: dict[str, str | None]
    hr: dict[str, str]

    def path(self, unit: str) -> tuple[str, ...]:
        path = []
        while unit is not None:
            path.insert(0, unit)
            unit = self.parent[unit]
        return tuple(path)

    def hr_unit(self, unit: str) -> str:
        """The nearest unit on the path with an HR contact; the card's company name."""
        for name in reversed(self.path(unit)):
            if name in self.hr:
                return name
        raise ValueError(f"{unit}: no HR contact on its path")

    def hr_for(self, unit: str) -> str:
        return self.hr[self.hr_unit(unit)]
