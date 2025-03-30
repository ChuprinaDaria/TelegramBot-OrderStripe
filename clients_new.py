from db_new import add_order

def create_contract(user_id, username, order_details, amount):
    contract = f"Контракт для користувача {username} на суму {amount}$. Деталі замовлення: {order_details}"
    add_order(user_id, username, order_details, amount, 'pending', '')
    return contract

def confirm_contract(user_id, order_id):
    # Logic to confirm the contract
    # Update the order status to 'confirmed' in the database
    pass