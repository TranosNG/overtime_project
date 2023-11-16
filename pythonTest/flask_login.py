# from flask import Flask, request, jsonify, make_response
# # from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# import datetime
# # import pyodbc
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# # # 👇️ <class 'collections.abc.Mapping'>
# # print(Mapping)


# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'TRANOS.NG'
# jwt = JWTManager(app)

# @app.route('/unprotected')
# def unprotected():
#     return ''

# @app.route('/protected', methods=['GET'])
# def protected():
#     current_user = get_jwt_identity()
#     return f'Protected route for user: {current_user}'

# @app.route('/login', methods=['POST'])
# def login():
#     employeeNo = request.json.get('employeeNo')
#     password = request.json.get('password')
#     # auth = request.authorization
#     # if auth and auth.password == 'password':
#     #     token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)})
#     # return jsonify({'token' : token.decode('UTF-8')})
#     # return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm = "Login Required"'})
#     access_token = create_access_token(identity=employeeNo)
#     return jsonify(access_token = access_token), 200

# # login()
# if __name__ == '__main__':
#     app.run(debug=True) 
# from flask_login import UserMixin, login_user, loginManager, login_required, logout_user, current_user

 
# from flask import Flask, request, jsonify, make_response, render_template, session

# import jwt
# from datetime import datetime, timedelta
# from functools import wraps

# app = Flask(__name__)
# app.config['SECRET_KEY'] = ' \xe6\x80d\xd0\xa0\xea,\xff"\x98V' 
# #  jwt = JWTManager(app)
# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = request/args.get('token')
#         if not token:
#             return jsonify({'Alert': 'Token is missing'})
#         try:
#             payload = jwt.decode(token, app.config['SECRET_KEY'])
#         except:
#             return jsonify({'Alert': 'Invalid Token'})
#         return decorated



# @app.route("/")
# def home():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         return 'logged in currently'
    
# @app.route('/public')
# def public():
#     return 'For public'

# @app.route('/auth')
# @token_required
# def auth():
#     return 'JWT is verified. Welcome to your dashboard'   
    
# @app.route('/login', methods=['POST'])
# def login():
#     if request.form["name"] and request.form["password"] == '123456':
#         session["logged_in"] = True
#     token = jwt.encode({
#         'name': request.form["username"],
#         "expiration": str(datetime.utcnow() + timedelta(seconds=120))
#     },
#         app.config['SECRET_KEY'])
#     return jsonify({'token': token.decode('utf-8')})
    
#     # return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm = "Login Required"'})

#     return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed!"'})


# if __name__ == "__main__":
#     app.run(debug=True)