from flask import request, jsonify
from models import Order, db, Customer

def register_customer_routes(app):

    def with_read_committed():
        # Set the isolation level for the current request
        db.session.connection(execution_options={"isolation_level": "READ COMMITTED"})

    @app.route('/customers/', methods=['GET'])
    def get_all_customers():
        with_read_committed()
        customers = Customer.query.all()
        return jsonify([{'id': c.id, 'name': c.name, 'company': c.company, 'email': c.email, 'phone': c.phone, 'age': c.age} for c in customers])
    
    @app.route('/customers/<int:id>', methods=['GET'])
    def get_customer(id):
        with_read_committed()
        customer = Customer.query.get(id)
        if customer:
            return jsonify({'id': customer.id, 'name': customer.name, 'company': customer.company, 'email': customer.email, 'phone': customer.phone, 'age': customer.age})
        else:
            return jsonify({"message": "Customer not found"}), 404

    @app.route('/customers/add', methods=['POST'])
    def add_customer():
        with_read_committed()
        data = request.get_json()
        new_customer = Customer(name=data['name'], email=data['email'], company=data['company'], phone=data['phone'], age=data['age'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"message": "Customer added successfully", "customer_id": new_customer.id})
    
    @app.route('/customers/update/<int:id>', methods=['PUT'])
    def update_customer(id):
        with_read_committed()
        customer = Customer.query.get(id)

        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        data = request.get_json()

        if 'name' in data:
            customer.name = data['name']
        if 'email' in data:
            customer.email = data['email']
        if 'company' in data:
            customer.company = data['company']
        if 'phone' in data:
            customer.phone = data['phone']
        if 'age' in data:
            customer.age = data['age']

        db.session.commit()
        return jsonify({"message": "Customer updated successfully"})

    @app.route('/customers/delete/<int:customer_id>', methods=['DELETE'])
    def delete_customer(customer_id):
        with_read_committed()
        customer = Customer.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()

            return jsonify({"message": "Customer deleted successfully"})
        return jsonify({"error": "Customer not found"}), 404
