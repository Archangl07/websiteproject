from flask import Flask, request, render_template
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
    #     dynamodb_ctbl.create_table()
    #     return 'Table created successfully'
    # except Exception as e:
    #     return 'Error occurred: ' + str(e)
    return render_template('signup.html')
        
@app.route('/login')
def login():
    return render_template('login.html')  

@app.route('/signup')
def signup():
    return render_template('signup.html')
    
    
 
    


if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')

