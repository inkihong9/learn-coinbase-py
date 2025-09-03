from enum import Enum as PyEnum
from coinbase.rest.types.orders_types import Order
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, Enum as SQLEnum
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from dateutil import parser

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
    created_time = Column(TIMESTAMP(fsp=6))
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
    last_fill_time = Column(TIMESTAMP(fsp=6))
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
        self.side = CbOrderSide(o.side)  # Good, assuming o.side is a valid enum value
        self.client_order_id = o.client_order_id
        self.status = CbOrderStatus(o.status)  # Good, assuming o.status is a valid enum value
        self.time_in_force = CbTimeInForce(o.time_in_force)  # Good, assuming o.time_in_force is a valid enum value

        # created_time: Make sure o.created_time is not empty string or None (o.created_time is ALWAYS in UTC timezone)
        self.created_time = (
            None if not o.created_time
            else parser.isoparse(o.created_time)
        )

        # completion_percentage: Handle empty string or None
        self.completion_percentage = (
            float(o.completion_percentage) if o.completion_percentage not in (None, '') else None
        )

        self.filled_size = float(o.filled_size) if o.filled_size not in (None, '') else None
        self.average_filled_price = float(o.average_filled_price) if o.average_filled_price not in (None, '') else None
        self.number_of_fills = int(o.number_of_fills) if o.number_of_fills not in (None, '') else None
        self.filled_value = float(o.filled_value) if o.filled_value not in (None, '') else None

        # pending_cancel, size_in_quote, size_inclusive_of_fees, settled, is_liquidation: If these can be None, handle accordingly
        self.pending_cancel = o.pending_cancel if o.pending_cancel is not None else False
        self.size_in_quote = o.size_in_quote if o.size_in_quote is not None else False
        self.total_fees = float(o.total_fees) if o.total_fees not in (None, '') else None
        self.size_inclusive_of_fees = o.size_inclusive_of_fees if o.size_inclusive_of_fees is not None else False
        self.total_value_after_fees = float(o.total_value_after_fees) if o.total_value_after_fees not in (None, '') else None

        self.trigger_status = CbTriggerStatus(o.trigger_status) if o.trigger_status else None

        # order_type, reject_reason, product_type, order_placement_source, margin_type: If these are enums, wrap as above
        self.order_type = CbOrderType(o.order_type) if o.order_type else None
        self.reject_reason = CbRejectReason(o.reject_reason) if o.reject_reason else None
        self.settled = o.settled if o.settled is not None else False
        self.product_type = CbProductType(o.product_type) if o.product_type else None

        # reject_message, cancel_message, leverage: If these can be None, handle accordingly
        self.reject_message = o.reject_message if o.reject_message not in (None, '') else None
        self.cancel_message = o.cancel_message if o.cancel_message not in (None, '') else None
        self.order_placement_source = CbOrderPlacementSource(o.order_placement_source) if o.order_placement_source else None
        self.outstanding_hold_amount = float(o.outstanding_hold_amount) if o.outstanding_hold_amount not in (None, '') else None
        self.is_liquidation = o.is_liquidation if o.is_liquidation is not None else False

        # last_fill_time: Handle None or empty string (o.last_fill_time is ALWAYS in UTC timezone)
        self.last_fill_time = (
            None if not o.last_fill_time
            else parser.isoparse(o.last_fill_time)
        )

        self.leverage = o.leverage if o.leverage not in (None, '') else None
        self.margin_type = CbMarginType(o.margin_type) if o.margin_type else None
        self.retail_portfolio_id = o.retail_portfolio_id if o.retail_portfolio_id not in (None, '') else None
        self.originating_order_id = o.originating_order_id if o.originating_order_id not in (None, '') else None
        self.attached_order_id = o.attached_order_id if o.attached_order_id not in (None, '') else None

        self.workable_size = int(o.workable_size) if o.workable_size not in (None, '') else None
        self.workable_size_completion_pct = (
            float(o.workable_size_completion_pct) if o.workable_size_completion_pct not in (None, '') else None
        )


# Create engine
engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(bind=engine)
