# lines 3 to 80 are what i did

# from dataclasses import dataclass
# from datetime import datetime

# @dataclass
# class Order:

#     order_id: str
#     product_id: str
#     user_id: str

#     # "order_configuration": {
#     #     "limit_limit_gtc": {
#     #         "base_size": "1.94417846",
#     #         "limit_price": "4031",
#     #         "post_only": true,
#     #         "rfq_disabled": false,
#     #         "reduce_only": false
#     #     }
#     # },
#     side: str
#     client_order_id: str
#     status: str
#     time_in_force: str
#     created_time: datetime
#     completion_percentage: float
#     filled_size: float
#     average_filled_price: float
#     # "fee": "",
#     # "number_of_fills": "5",
#     filled_value: float
#     pending_cancel: bool
#     size_in_quote: bool
#     total_fees: float
#     size_inclusive_of_fees: bool
#     total_value_after_fees: float
#     trigger_status: str
#     order_type: str
#     reject_reason: str
#     settled: bool
#     product_type: str
#     reject_message: str
#     cancel_message: str
#     order_placement_source: str
#     # "outstanding_hold_amount": "0",
#     is_liquidation: bool
#     last_fill_time: datetime
#     # "edit_history": [
#     #     {
#     #         "price": "4035",
#     #         "size": "1.94417846",
#     #         "replace_accept_timestamp": "2025-08-08T22:21:52.059381473Z"
#     #     },
#     #     {
#     #         "price": "4031",
#     #         "size": "1.94417846",
#     #         "replace_accept_timestamp": "2025-08-08T22:22:57.505168083Z"
#     #     }
#     # ],
#     # "leverage": "",
#     margin_type: str
#     retail_portfolio_id: str
#     originating_order_id: str
#     attached_order_id: str
#     # "attached_order_configuration": null,
#     # "current_pending_replace": null,
#     # "commission_detail_total": null,
#     # "workable_size": "0",
#     workable_size_completion_pct: str

#     def __init__(self, order_id, customer_name, items):
#         self.order_id = order_id
#         self.customer_name = customer_name
#         self.items = items

#     def __init__(self, d):
#         self.order_id = d.get('order_id')
#         self.customer_name = d.get('customer_name')
#         self.items = d.get('items', [])


from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Account:
    uuid: str
    name: str
    currency: str
    available_balance: float
    default: bool
    active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    type: str
    ready: bool
    hold: float
    retail_portfolio_id: str
    platform: str

    @staticmethod
    def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
        if dt_str is None:
            return None
        try:
            # Handles both with and without microseconds
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except Exception:
            return None

    @classmethod
    def from_dict(cls, d: dict) -> "Account":
        return cls(
            uuid=d.get("uuid", ""),
            name=d.get("name", ""),
            currency=d.get("currency", ""),
            available_balance=float(d.get("available_balance").get("value")),
            default=bool(d.get("default", False)),
            active=bool(d.get("active", False)),
            created_at=cls.parse_datetime(d.get("created_at")),
            updated_at=cls.parse_datetime(d.get("updated_at")),
            deleted_at=cls.parse_datetime(d.get("deleted_at")),
            type=d.get("type", ""),
            ready=bool(d.get("ready", False)),
            hold=float(d.get("hold").get("value")),
            retail_portfolio_id=d.get("retail_portfolio_id", ""),
            platform=d.get("platform", "")
        )