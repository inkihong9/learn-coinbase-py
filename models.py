# from dataclasses import dataclass
# from typing import Optional
# from datetime import datetime


# def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
#     if dt_str is None:
#         return None
#     try:
#         # Handles both with and without microseconds
#         return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
#     except Exception:
#         return None

# @dataclass
# class Account:
#     uuid: str
#     name: str
#     currency: str
#     available_balance: float
#     default: bool
#     active: bool
#     created_at: datetime
#     updated_at: datetime
#     deleted_at: Optional[datetime]
#     type: str
#     ready: bool
#     hold: float
#     retail_portfolio_id: str
#     platform: str

#     @classmethod
#     def from_dict(cls, d: dict) -> "Account":
#         return cls(
#             uuid=d.get("uuid", ""),
#             name=d.get("name", ""),
#             currency=d.get("currency", ""),
#             available_balance=float(d.get("available_balance").get("value")),
#             default=bool(d.get("default", False)),
#             active=bool(d.get("active", False)),
#             created_at=parse_datetime(d.get("created_at")),
#             updated_at=parse_datetime(d.get("updated_at")),
#             deleted_at=parse_datetime(d.get("deleted_at")),
#             type=d.get("type", ""),
#             ready=bool(d.get("ready", False)),
#             hold=float(d.get("hold").get("value")),
#             retail_portfolio_id=d.get("retail_portfolio_id", ""),
#             platform=d.get("platform", "")
#         )