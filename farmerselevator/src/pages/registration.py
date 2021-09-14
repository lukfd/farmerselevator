from farmerselevator import application
from farmerselevator.src.helper import *


@application.route('/signin')
def signin():
    if 'username' in session:
        closeSession()
    return '''
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <link rel="stylesheet" type="text/css" href="/static/css/internal.css">
    <div class="header">
        <h1>Farmers & Elevators</h1>
    </div>
    <div class="page">
        <form action="/signin-form" method="post">
            <label>Username:</label>
            <input type="text" name="username"/>
            <label>Password:</label>
            <input type="password" name="password"/>
            <label>elevator?</label>
            <input type="checkbox" name="elevator"/>
            <button type="submit" class="button">Singin</button>
        </form>
        </div>
            <a href="/signup">Don't have an account yet? Sign Up</a>
        <div>
    </div>    
    '''

@application.route('/signup')
def signup():
    return '''
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <h1>Farmers & Elevators</h1>
	<form action="/signup-form" method="post">
		<label>Email:</label>
		<input type="email" name="email"/>
		<label>Username:</label>
		<input type="text" name="username"/>
		<label>Password:</label>
		<input type="password" name="password"/>
		<label>retype Password:</label>
		<input type="password"/>
		<label>elevator?</label>
		<input type="checkbox" name="elevator"/>
		<button type="submit">sign-up</button>
	</form>
    <a href="/signin">Already have an account? Sign in</a>
    '''