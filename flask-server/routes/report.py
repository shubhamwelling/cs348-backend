from flask import request, jsonify
from models import db, Order, Customer
from sqlalchemy import text
from datetime import datetime

def register_report_routes(app):

    def with_serializable():
        # Set the isolation level for the current request
        db.session.connection(execution_options={"isolation_level": "SERIALIZABLE"})

    @app.route('/reports/generate', methods=['GET'])
    def generate_report():
        with_serializable()
        start_date_str = request.args.get('start_date', type=str)
        end_date_str = request.args.get('end_date', type=str)
        min_order_size = request.args.get('min_order_size', type=float, default=0)
        min_sale_value = request.args.get('min_sale_value', type=float, default=0)

        if not start_date_str or not end_date_str:
            return jsonify({"error": "Please provide both start_date and end_date."}), 400

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400

        params = {
            'start_date': start_date,
            'end_date': end_date,
            'min_order_size': min_order_size,
            'min_sale_value': min_sale_value
        }

        with db.engine.connect() as conn:
            # Detailed orders query
            orders_query = text("""
                SELECT o.id AS order_id, o.order_time, o.order_size, o.sale_value, 
                       c.name AS customer_name, c.company AS customer_company
                FROM orders o
                JOIN customer c ON o.customer_id = c.id
                WHERE o.order_time BETWEEN :start_date AND :end_date
                AND o.order_size >= :min_order_size
                AND o.sale_value >= :min_sale_value
            """)
            orders_rows = conn.execute(orders_query, params).fetchall()

            if not orders_rows:
                return jsonify({
                    "message": "No orders found in the given date range with the specified filters."
                }), 200

            order_data = []
            for row in orders_rows:
                order_data.append({
                    'order_id': row.order_id,
                    'order_time': str(row.order_time),
                    'order_size': row.order_size,
                    'sale_value': row.sale_value,
                    'customer_name': row.customer_name,
                    'customer_company': row.customer_company
                })

            # Aggregate queries
            avg_order_size_query = text("""
                SELECT AVG(o.order_size) AS avg_order_size
                FROM orders o
                JOIN customer c ON o.customer_id = c.id
                WHERE o.order_time BETWEEN :start_date AND :end_date
                AND o.order_size >= :min_order_size
                AND o.sale_value >= :min_sale_value
            """)
            avg_order_size = conn.execute(avg_order_size_query, params).scalar()

            avg_sale_value_query = text("""
                SELECT AVG(o.sale_value) AS avg_sale_value
                FROM orders o
                JOIN customer c ON o.customer_id = c.id
                WHERE o.order_time BETWEEN :start_date AND :end_date
                AND o.order_size >= :min_order_size
                AND o.sale_value >= :min_sale_value
            """)
            avg_sale_value = conn.execute(avg_sale_value_query, params).scalar()

            avg_age_query = text("""
                SELECT AVG(c.age) AS avg_age
                FROM orders o
                JOIN customer c ON o.customer_id = c.id
                WHERE o.order_time BETWEEN :start_date AND :end_date
                AND o.order_size >= :min_order_size
                AND o.sale_value >= :min_sale_value
                AND c.age IS NOT NULL
            """)
            avg_age = conn.execute(avg_age_query, params).scalar()

            num_orders_query = text("""
                SELECT COUNT(*) AS order_count
                FROM orders o
                JOIN customer c ON o.customer_id = c.id
                WHERE o.order_time BETWEEN :start_date AND :end_date
                AND o.order_size >= :min_order_size
                AND o.sale_value >= :min_sale_value
                AND c.age IS NOT NULL
            """)
            order_count = conn.execute(num_orders_query, params).scalar()

        detailed_response = {"orders": order_data}
        aggregate_response = {
            "average_order_size": round(avg_order_size, 2) if avg_order_size else None,
            "average_sale_value": round(avg_sale_value, 2) if avg_sale_value else None,
            "average_age_of_customer": round(avg_age, 2) if avg_age else None,
            "total_orders": order_count
        }

        return jsonify({
            "detailed_orders": detailed_response,
            "aggregate_statistics": aggregate_response
        }), 200
