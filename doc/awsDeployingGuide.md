# Guide and notes for the deployment to AWS

#### Prerequisites

This guide will direct to references and guide you to how to deploy to AWS.

Make sure you have installed docker for desktop in your local machine.

#### Process to deploy

Create a local image:

```
docker buildx build --platform=linux/amd64 -t farmerselevator-image .
```

Create the container and deploy it to aws light sail:

```
aws lightsail push-container-image --region us-east-2 --service-name farmerselevator --label beta --image farmerselevator-image:latest
```

On aws lightsail go the the Deployments page. If another container was already running or deployed, click  Modify and redeploy.

![](doc/example_awslight.png)

#### Running the image locally

Or if you want to create the container locally to test it:

```
docker run -p 8000:8000 farmerselevator-image flask run --host 0.0.0.0
```

![alt text](doc/awslightsail_deployment_screen_settings.png)

#### Github actions



#### Known errors

My stack overflow questions: [Error deploying flask application in Elastic Beanstalk: option --bind not recognized](https://stackoverflow.com/questions/69441814/error-deploying-flask-application-in-elastic-beanstalk-option-bind-not-recogn)

Some of the stack overflow posts that talks about how to deploy large flask structure.

- [Flask Error in Python: "Could not import webapp"](https://stackoverflow.com/questions/62585946/flask-error-in-python-could-not-import-webapp)

- [Deploying Flask app on Elastic Beanstalk: No module named 'application'](https://stackoverflow.com/questions/64000856/deploying-flask-app-on-elastic-beanstalk-no-module-named-application)

- [How to deploy structured Flask app on AWS elastic beanstalk](https://stackoverflow.com/questions/20558747/how-to-deploy-structured-flask-app-on-aws-elastic-beanstalk)

- [Running flask as package in production](https://stackoverflow.com/questions/47757167/running-flask-as-package-in-production)