from typing import Optional, Dict, Any

from pydantic.dataclasses import dataclass

from looqbox.config.pydantic_configuration import PydanticConfiguration


@dataclass(config=PydanticConfiguration.Config)
class ResponseUser:
    id: int
    login: str
    group_id: int
    sso_attributes: Optional[Dict[str, Any]] = None
    language: Optional[str] = "pt-br"
    dec_separator: Optional[str] = ","
    date_format: Optional[str] = "dd/mm/yyyy"

    def to_dict(self):
        return {
            "id": self.id,
            "login": self.login,
            "group_id": self.group_id,
            "language": self.language,
            "dec_separator": self.dec_separator,
            "date_format": self.date_format,
            "sso_attributes": self.sso_attributes
        }
