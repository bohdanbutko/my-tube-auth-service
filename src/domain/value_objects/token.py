from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class Token:
    access_token: str
    token_type: str = field(default="bearer")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
