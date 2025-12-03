from . import orders, ingredients, customers, menu_items, order_items, promotions, reviews


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(ingredients.router)
    app.include_router(customers.router)
    app.include_router(menu_items.router)
    app.include_router(order_items.router)
    app.include_router(promotions.router)
    app.include_router(reviews.router)

