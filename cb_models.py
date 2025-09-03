from enum import Enum as PyEnum
from coinbase.rest.types.orders_types import Order
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

import os

Base = declarative_base()

# Pull from environment variables set in docker-compose.yml
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# SQLAlchemy connection URL for MySQL (using pymysql driver)
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"


class CbOrderSide(PyEnum):
    BUY = 'BUY'
    SELL = 'SELL'


class CbOrderStatus(PyEnum):
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


class CbTimeInForce(PyEnum):
    UNKNOWN_TIME_IN_FORCE = 'UNKNOWN_TIME_IN_FORCE'
    GOOD_UNTIL_DATE_TIME = 'GOOD_UNTIL_DATE_TIME'
    GOOD_UNTIL_CANCELLED = 'GOOD_UNTIL_CANCELLED'
    IMMEDIATE_OR_CANCEL = 'IMMEDIATE_OR_CANCEL'
    FILL_OR_KILL = 'FILL_OR_KILL'


class CbTriggerStatus(PyEnum):
    UNKNOWN_TRIGGER_STATUS = 'UNKNOWN_TRIGGER_STATUS'
    INVALID_ORDER_TYPE = 'INVALID_ORDER_TYPE'
    STOP_PENDING = 'STOP_PENDING'
    STOP_TRIGGERED = 'STOP_TRIGGERED'


class CbOrderType(PyEnum):
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


class CbRejectReason(PyEnum):
    REJECT_REASON_UNSPECIFIED = 'REJECT_REASON_UNSPECIFIED'
    HOLD_FAILURE = 'HOLD_FAILURE'
    TOO_MANY_OPEN_ORDERS = 'TOO_MANY_OPEN_ORDERS'
    REJECT_REASON_INSUFFICIENT_FUNDS = 'REJECT_REASON_INSUFFICIENT_FUNDS'
    RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED'


class CbProductType(PyEnum):
    UNKNOWN_PRODUCT_TYPE = 'UNKNOWN_PRODUCT_TYPE'
    SPOT = 'SPOT'
    FUTURE = 'FUTURE'


class CbOrderPlacementSource(PyEnum):
    UNKNOWN_PLACEMENT_SOURCE = 'UNKNOWN_PLACEMENT_SOURCE'
    RETAIL_SIMPLE = 'RETAIL_SIMPLE'
    RETAIL_ADVANCED = 'RETAIL_ADVANCED'


class CbMarginType(PyEnum):
    CROSS = 'CROSS'
    ISOLATED = 'ISOLATED'
    UNKNOWN_MARGIN_TYPE = 'UNKNOWN_MARGIN_TYPE'


# go to link https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/orders/get-order
# and see response section for details
# all fields that are commented out are different types of objects, not primitive data types, will come back to them later
class CbOrder(Base):
    __tablename__ = "cb_order"

    order_id = Column(String(36), primary_key=True, index=True)
    product_id = Column(String(16))
    user_id = Column(String(36))
    # order_configuration = special object, i'll come back to this later
    side = Column(SQLEnum(CbOrderSide))
    client_order_id = Column(String(36))
    status = Column(SQLEnum(CbOrderStatus))
    time_in_force = Column(SQLEnum(CbTimeInForce))
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
    trigger_status = Column(SQLEnum(CbTriggerStatus))
    order_type = Column(SQLEnum(CbOrderType))
    reject_reason = Column(SQLEnum(CbRejectReason))
    settled = Column(Boolean)
    product_type = Column(SQLEnum(CbProductType))
    reject_message = Column(Text)
    cancel_message = Column(Text)
    order_placement_source = Column(SQLEnum(CbOrderPlacementSource))
    outstanding_hold_amount = Column(Float)
    is_liquidation = Column(Boolean)
    last_fill_time = Column(DateTime)
    # edit_history = list of some object
    leverage = Column(Text)
    margin_type = Column(SQLEnum(CbMarginType))
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
        self.product_id = o.product_id
        self.user_id = o.user_id
        self.side = o.side
        self.client_order_id = o.client_order_id
        self.status = o.status
        self.time_in_force = o.time_in_force
        self.created_time = None if o.created_time is None else datetime.strptime(o.created_time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        self.completion_percentage = o.completion_percentage
        self.filled_size = o.filled_size
        self.average_filled_price = o.average_filled_price
        self.number_of_fills = o.number_of_fills
        self.filled_value = o.filled_value
        self.pending_cancel = o.pending_cancel
        self.size_in_quote = o.size_in_quote
        self.total_fees = o.total_fees
        self.size_inclusive_of_fees = o.size_inclusive_of_fees
        self.total_value_after_fees = o.total_value_after_fees
        self.trigger_status = o.trigger_status
        self.order_type = o.order_type
        self.reject_reason = o.reject_reason
        self.settled = o.settled
        self.product_type = o.product_type
        self.reject_message = o.reject_message
        self.cancel_message = o.cancel_message
        self.order_placement_source = o.order_placement_source
        self.outstanding_hold_amount = o.outstanding_hold_amount
        self.is_liquidation = o.is_liquidation
        self.last_fill_time = None if o.last_fill_time is None else datetime.strptime(o.last_fill_time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        self.leverage = o.leverage
        self.margin_type = o.margin_type
        self.retail_portfolio_id = o.retail_portfolio_id
        self.originating_order_id = o.originating_order_id
        self.attached_order_id = o.attached_order_id
        self.workable_size = o.workable_size
        self.workable_size_completion_pct = o.workable_size_completion_pct


# Create engine
engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(bind=engine)
