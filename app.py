from flask import Flask, request, render_template, redirect, jsonify, url_for
import botocore.exceptions
import boto3
import key_config as keys
import dynamodb_create_table as dynamodb_ctbl
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__, static_folder='static')

dynamodb = boto3.resource(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)

@app.route('/')
def index():
    # try:
    #     # Update the existing student table
    #     dynamodb_ctbl.create_table()
    #     return 'Table updated successfully'
    # except Exception as e:
    #     return 'Error occurred: ' + str(e)
        
    return render_template('signup.html')
        
@app.route('/login')
def login():
    return render_template('login.html')
    

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    reg_number = request.form['reg_number']
    degree_program = request.form['degree_program']
    contact = request.form['contact']
    introduction = request.form['introduction']
    current_gpa = request.form['current_gpa']
    skills = request.form['skills']
    
    # Get the table
    table = dynamodb.Table('student')
    
    table.put_item(
        Item={
            'name': name,
            'email': email,
            'password': password,
            'reg_number': reg_number,
            'degree_program': degree_program,
            'contact': contact,
            'introduction': introduction,
            'current_gpa': current_gpa,
            'skills': skills
        }
    )
    
    msg = "Registration Complete. Please login using your credentials"
    
    return render_template('login.html', msg=msg, success=True)

@app.route('/check', methods=['post'])
def check():
    email = request.form['email']
    password = request.form['password']
    
    table = dynamodb.Table('student')
    
    response = table.scan(
        FilterExpression=Attr('email').eq(email)
    )
    
    items = response['Items']
    if len(items)>0:
        user = items[0]
        if password == user['password']:
            return render_template('profile-edit.html', user=user, success=True)
        else:
            msg = "Incorrect password Try again"
    else:
        msg = "Email not found. Please check your email and try again."
            
    return render_template('login.html', msg=msg, success=False)
    
    

@app.route('/save', methods=['POST'])
def save():
    user = {
        'name': request.form['name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'reg_number': request.form['reg_number'],
        'degree_program': request.form['degree_program'],
        'contact': request.form['contact'],
        'introduction': request.form['introduction'],
        'current_gpa': request.form['current_gpa'],
        'skills': request.form['skills']
    }
    
    table = dynamodb.Table('student')
    
    expression_attribute_values = {
        ':n': user['name'],
        ':p': user['password'],
 
        ':d': user['degree_program'],
        ':c': user['contact'],
        ':i': user['introduction'],
        ':g': user['current_gpa'],
        ':s': user['skills']
    }
    
    update_expression = 'SET #attr_name = :n, password = :p, degree_program = :d, contact = :c, introduction = :i, current_gpa = :g, skills = :s'
    
    expression_attribute_names = {
        '#attr_name': 'name'  # Use an expression attribute name to avoid conflict with reserved keyword 'name'
    }
    
    try:
        table.update_item(
            Key={'email': user['email'], 'reg_number': user['reg_number']},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
    except botocore.exceptions.ClientError as e:
        response = {'success': False, 'msg': 'Failed to update account details.'}
        return jsonify(response)
    
    response = {'success': True, 'msg': 'Account details updated successfully.'}
    return jsonify(response)
    
    # table.update_item(
    #     Key={'email': user['email'], 'reg_number': user['reg_number']},
    #     UpdateExpression=update_expression,
    #     ExpressionAttributeNames=expression_attribute_names,
    #     ExpressionAttributeValues=expression_attribute_values
    # )
    
    
    # response = {'success': True, 'msg': 'Account details updated successfully.'}
    
    # return jsonify(response)

@app.route('/profile/<reg_number>')
def profile(reg_number):
    # Retrieve the student's profile information from the database
    table = dynamodb.Table('student')
    response = table.scan(FilterExpression=Attr('reg_number').eq(reg_number))
    items = response['Items']
    if len(items) > 0:
        student = items[0]
        return render_template('profile-view.html', student=student)
    else:
        error_msg = "Student profile not found."
        return render_template('profile-view.html', error_msg=error_msg)
        

if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')