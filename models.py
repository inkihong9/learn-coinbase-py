from dataclasses import dataclass
from typing import Optional
from datetime import datetime


def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    if dt_str is None:
        return None
    try:
        # Handles both with and without microseconds
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        return None

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

    @classmethod
    def from_dict(cls, d: dict) -> "Account":
        return cls(
            uuid=d.get("uuid", ""),
            name=d.get("name", ""),
            currency=d.get("currency", ""),
            available_balance=float(d.get("available_balance").get("value")),
            default=bool(d.get("default", False)),
            active=bool(d.get("active", False)),
            created_at=parse_datetime(d.get("created_at")),
            updated_at=parse_datetime(d.get("updated_at")),
            deleted_at=parse_datetime(d.get("deleted_at")),
            type=d.get("type", ""),
            ready=bool(d.get("ready", False)),
            hold=float(d.get("hold").get("value")),
            retail_portfolio_id=d.get("retail_portfolio_id", ""),
            platform=d.get("platform", "")
        )
    

@dataclass
class Order:
    order_id: str
    product_id: str
    user_id: str
    # order_configuration: OrderConfiguration
    side: str
    client_order_id: str
    status: str
    time_in_force: str
    created_time: datetime
    completion_percentage: float
    filled_size: float
    average_filled_price: float
    fee: str
    number_of_fills: int
    filled_value: float
    pending_cancel: bool
    size_in_quote: bool
    total_fees: float
    size_inclusive_of_fees: bool
    total_value_after_fees: float
    trigger_status: str
    order_type: str
    reject_reason: str
    settled: bool
    product_type: str
    reject_message: str
    cancel_message: str
    order_placement_source: str
    outstanding_hold_amount: float
    is_liquidation: bool
    last_fill_time: Optional[datetime]
    # edit_history: List[EditHistoryEntry]
    leverage: str
    margin_type: str
    retail_portfolio_id: str
    originating_order_id: str
    attached_order_id: str
    # attached_order_configuration: Optional[Any]
    # current_pending_replace: Optional[Any]
    # commission_detail_total: Optional[Any]
    # workable_size: float
    workable_size_completion_pct: str

    @staticmethod
    def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except Exception:
            return None

    @classmethod
    def from_dict(cls, d: dict) -> "Order":
        return cls(
            order_id=d.get("order_id", ""),
            product_id=d.get("product_id", ""),
            user_id=d.get("user_id", ""),
            # order_configuration=OrderConfiguration.from_dict(d.get("order_configuration", {})),
            side=d.get("side", ""),
            client_order_id=d.get("client_order_id", ""),
            status=d.get("status", ""),
            time_in_force=d.get("time_in_force", ""),
            created_time=cls.parse_datetime(d.get("created_time")),
            completion_percentage=float(d.get("completion_percentage", 0)),
            filled_size=float(d.get("filled_size", 0)),
            average_filled_price=float(d.get("average_filled_price", 0)),
            fee=d.get("fee", ""),
            number_of_fills=int(d.get("number_of_fills", 0)),
            filled_value=float(d.get("filled_value", 0)),
            pending_cancel=bool(d.get("pending_cancel", False)),
            size_in_quote=bool(d.get("size_in_quote", False)),
            total_fees=float(d.get("total_fees", 0)),
            size_inclusive_of_fees=bool(d.get("size_inclusive_of_fees", False)),
            total_value_after_fees=float(d.get("total_value_after_fees", 0)),
            trigger_status=d.get("trigger_status", ""),
            order_type=d.get("order_type", ""),
            reject_reason=d.get("reject_reason", ""),
            settled=bool(d.get("settled", False)),
            product_type=d.get("product_type", ""),
            reject_message=d.get("reject_message", ""),
            cancel_message=d.get("cancel_message", ""),
            order_placement_source=d.get("order_placement_source", ""),
            outstanding_hold_amount=float(d.get("outstanding_hold_amount", 0)),
            is_liquidation=bool(d.get("is_liquidation", False)),
            last_fill_time=cls.parse_datetime(d.get("last_fill_time")),
            # edit_history=[EditHistoryEntry.from_dict(eh) for eh in d.get("edit_history", [])],
            leverage=d.get("leverage", ""),
            margin_type=d.get("margin_type", ""),
            retail_portfolio_id=d.get("retail_portfolio_id", ""),
            originating_order_id=d.get("originating_order_id", ""),
            attached_order_id=d.get("attached_order_id", ""),
            # attached_order_configuration=d.get("attached_order_configuration"),
            # current_pending_replace=d.get("current_pending_replace"),
            # commission_detail_total=d.get("commission_detail_total"),
            # workable_size=float(d.get("workable_size", 0)),
            workable_size_completion_pct=d.get("workable_size_completion_pct", "")
        )