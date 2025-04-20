@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400
            
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            session.permanent = True
            session['user_id'] = user.id
            return jsonify({
                'message': 'Login successful',
                'user_id': user.id
            }), 200
        
        return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({
            'id': user.id,
            'username': user.username
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
