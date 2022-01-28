# Flask set up guide

To set up the environment
```
export FLASK_APP=farmerselevator_production
export FLASK_ENV=production
```

Then to run the server
```
flask run
```

To run in a different port
```
export FLASK_RUN_PORT=8000
```

Read about deployment: [https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/](https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/)

# Flask production deployment Dockerfile

1. create Dockerfile
2. `docker build -t flask-container . `
3. docker images
4. `aws lightsail push-container-image --region us-east-2 --service-name test --label flaskapp --image flaskapp:latest`

# Flask production deployment vanilla

[Deploy to production](https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/)