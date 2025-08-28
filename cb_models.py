from enum import Enum
from coinbase.rest.types.orders_types import Order
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CbOrderSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class CbOrderStatus(Enum):
    PENDING = 'PENDING'
    OPEN = 'OPEN'
    FILLED = 'FILLED'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'
    FAILED = 'FAILED'
    UNKNOWN_ORDER_STATUS = 'UNKNOWN_ORDER_STATUS'
    QUEUED = 'QUEUED'
    CANCEL_QUEUED = 'CANCEL_QUEUED'
    EDIT_QUEUED  = 'EDIT_QUEUED '


class CbTimeInForce(Enum):
    UNKNOWN_TIME_IN_FORCE = 'UNKNOWN_TIME_IN_FORCE'
    GOOD_UNTIL_DATE_TIME = 'GOOD_UNTIL_DATE_TIME'
    GOOD_UNTIL_CANCELLED = 'GOOD_UNTIL_CANCELLED'
    IMMEDIATE_OR_CANCEL = 'IMMEDIATE_OR_CANCEL'
    FILL_OR_KILL = 'FILL_OR_KILL'


class CbTriggerStatus(Enum):
    UNKNOWN_TRIGGER_STATUS = 'UNKNOWN_TRIGGER_STATUS'
    INVALID_ORDER_TYPE = 'INVALID_ORDER_TYPE'
    STOP_PENDING = 'STOP_PENDING'
    STOP_TRIGGERED = 'STOP_TRIGGERED'


class CbOrderType(Enum):
    UNKNOWN_ORDER_TYPE = 'UNKNOWN_ORDER_TYPE'
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'
    STOP = 'STOP'
    STOP_LIMIT = 'STOP_LIMIT'
    BRACKET = 'BRACKET'
    TWAP = 'TWAP'
    ROLL_OPEN = 'ROLL_OPEN'
    ROLL_CLOSE = 'ROLL_CLOSE'
    LIQUIDATION = 'LIQUIDATION'


class CbRejectReason(Enum):
    REJECT_REASON_UNSPECIFIED = 'REJECT_REASON_UNSPECIFIED'
    HOLD_FAILURE = 'HOLD_FAILURE'
    TOO_MANY_OPEN_ORDERS = 'TOO_MANY_OPEN_ORDERS'
    REJECT_REASON_INSUFFICIENT_FUNDS = 'REJECT_REASON_INSUFFICIENT_FUNDS'
    RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED'


class CbProductType(Enum):
    UNKNOWN_PRODUCT_TYPE = 'UNKNOWN_PRODUCT_TYPE'
    SPOT = 'SPOT'
    FUTURE = 'FUTURE'


class CbOrderPlacementSource(Enum):
    UNKNOWN_PLACEMENT_SOURCE = 'UNKNOWN_PLACEMENT_SOURCE'
    RETAIL_SIMPLE = 'RETAIL_SIMPLE'
    RETAIL_ADVANCED = 'RETAIL_ADVANCED'


class CbMarginType(Enum):
    CROSS = 'CROSS'
    ISOLATED = 'ISOLATED'
    UNKNOWN_MARGIN_TYPE = 'UNKNOWN_MARGIN_TYPE'


# go to link https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/orders/get-order
# and see response section for details
# all fields that are commented out are different types of objects, not primitive data types, will come back to them later
class CbOrder(Base):
    __tablename__ = "cb_order"

    order_id = Column(String(36), primary_key=True)
    product_id = Column(String(16))
    user_id = Column(String(36))
    # order_configuration
    side = Column(Enum(CbOrderSide))
    client_order_id = Column(String(36))
    status = Column(Enum(CbOrderStatus))
    time_in_force = Column(Enum(CbTimeInForce))
    created_time = Column(DateTime)
    completion_percentage = Column(Float)
    filled_size = Column(Float)
    average_filled_price = Column(Float)
    # fee = probably Float, but this field is deprecated so ignore it
    number_of_fills = Column(Integer)
    filled_value = Column(Float)
    pending_cancel = Column(Boolean)
    size_in_quote = Column(Boolean)
    total_fees = Column(Float)
    size_inclusive_of_fees = Column(Boolean)
    total_value_after_fees = Column(Float)
    trigger_status = Column(Enum(CbTriggerStatus))
    order_type = Column(Enum(CbOrderType))
    reject_reason = Column(Enum(CbRejectReason))
    settled = Column(Boolean)
    product_type = Column(Enum(CbProductType))
    reject_message = Column(String)
    cancel_message = Column(String)
    order_placement_source = Column(Enum(CbOrderPlacementSource))
    outstanding_hold_amount = Column(Float)
    is_liquidation = Column(Boolean)
    last_fill_time = Column(DateTime)
    # edit_history = list of some object
    leverage = Column(String)
    margin_type = Column(Enum(CbMarginType))
    retail_portfolio_id = Column(String(36))
    originating_order_id = Column(String(36))
    attached_order_id = Column(String(36))
    # attached_order_configuration = some object
    # current_pending_replace = some object
    # commission_detail_total = some object
    workable_size = Column(Integer)
    workable_size_completion_pct = Column(Float)

    def __init__(self, o: Order):
        self.order_id = o.order_id
