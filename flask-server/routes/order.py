from flask import request, jsonify
from models import db, Order, Customer
from datetime import datetime


def register_order_routes(app):

    def with_read_committed():
        # Set the isolation level for the current request
        db.session.connection(execution_options={"isolation_level": "READ COMMITTED"})
   
    @app.route('/orders/', methods=['GET'])
    def get_all_orders():
        # Query for Order and Customer joined on Order.customer_id = Customer.id
        with_read_committed()
        orders_with_customers = db.session.query(Order, Customer).join(Customer, Customer.id == Order.customer_id).order_by(Order.order_time).all()
       
        valid_orders = [
            {
                'order_id': order.id,
                'order_time': str(order.order_time),
                'order_size': order.order_size,
                'sale_value': order.sale_value,
                'customer_name': customer.name,
                'customer_company': customer.company
            }
            for order, customer in orders_with_customers
        ]
       
        return jsonify(valid_orders)


    @app.route('/orders/<int:id>', methods=['GET'])
    def get_order(id):
        # Query for Order and Customer joined on Order.customer_id = Customer.id
        with_read_committed()
        orders_with_customers = db.session.query(Order, Customer).join(Customer, Customer.id == Order.customer_id).order_by(Order.order_time).all()
        valid_orders = [
            {
                'order_id': order.id,
                'order_time': str(order.order_time),
                'order_size': order.order_size,
                'sale_value': order.sale_value,
                'customer_name': customer.name,
                'customer_company': customer.company
            }
            for order, customer in orders_with_customers if order.id == id
        ]
       
        return jsonify(valid_orders)

    @app.route('/orders/add', methods=['POST'])
    def add_order():
        with_read_committed()
        data = request.get_json()
        customer = None
        if 'customer_id' in data:
            customer = Customer.query.get(data['customer_id'])

        order_time_stripped = datetime.strptime(data['order_time'], "%Y-%m-%d %H:%M:%S")
    
        new_order = Order(
            customer_id=customer.id,  
            order_time=order_time_stripped,
            order_size=data['order_size'],
            sale_value=data['sale_value']
        )

        db.session.add(new_order)
        db.session.commit()  
  
        return jsonify({
            "message": "Order added successfully",
            "order_id": new_order.id,
            "customer_id": new_order.customer_id, 
            "order_details": {
                "order_size": new_order.order_size,
                "sale_value": new_order.sale_value
            }
        })


    @app.route('/orders/update/<int:id>', methods=['PUT'])
    def update_order(id):
        with_read_committed()
        order = Order.query.get(id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        data = request.get_json()
        if 'order_size' in data:
            order.order_size = data['order_size']
        if 'sale_value' in data:
            order.sale_value = data['sale_value']

        db.session.commit()
        return jsonify({"message": "Order updated successfully"})


    @app.route('/orders/delete/<int:id>', methods=['DELETE'])
    def delete_order(id):
        with_read_committed()
        order = Order.query.get(id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"})
