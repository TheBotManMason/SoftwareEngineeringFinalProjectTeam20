from . import orders, order_items, inventory, customers, menu_items, promotions, reviews

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_items.Base.metadata.create_all(engine)
    inventory.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
