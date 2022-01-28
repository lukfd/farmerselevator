# Guide and notes for the deployment to AWS

This guide will direct to references and guide you to how to deploy to AWS.

# Commands

Run command `docker buildx build --platform=linux/amd64 -t farmerselevator-image .`

`aws lightsail push-container-image --region us-east-2 --service-name farmerselevator --label beta --image farmerselevator-image:latest`

### Errors

My stack overflow questions: [Error deploying flask application in Elastic Beanstalk: option --bind not recognized](https://stackoverflow.com/questions/69441814/error-deploying-flask-application-in-elastic-beanstalk-option-bind-not-recogn)

Some of the stack overflow posts that talks about how to deploy large flask structure.

- [Flask Error in Python: "Could not import webapp"](https://stackoverflow.com/questions/62585946/flask-error-in-python-could-not-import-webapp)

- [Deploying Flask app on Elastic Beanstalk: No module named 'application'](https://stackoverflow.com/questions/64000856/deploying-flask-app-on-elastic-beanstalk-no-module-named-application)

- [How to deploy structured Flask app on AWS elastic beanstalk](https://stackoverflow.com/questions/20558747/how-to-deploy-structured-flask-app-on-aws-elastic-beanstalk)

- [Running flask as package in production](https://stackoverflow.com/questions/47757167/running-flask-as-package-in-production)