from . import customers, ingredients, menu_items, orders, order_items, promotions, reviews
from ..dependencies.database import engine

def index():
    customers.Base.metadata.create_all(engine)
    ingredients.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    order_items.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)