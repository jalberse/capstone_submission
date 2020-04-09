# Deployment

We take a modular approach to deployment, deploying the API and the frontend separately. This approach allows for the reuse of the API for other projects easily. This is desirable, as the task the API is accomplishing - autocomplete and sentiment analysis - are useful in a wide variety of tasks applicable at Tailwind. 

## Guide to deploying API using Google App Engine

Refer to: https://cloud.google.com/appengine/docs/standard/python3/building-app

Caveats and special considerations are listed below. 

Ignore venv/env commands in Google documentation - we use Pipenv for this purpose. 

However, app engine does not like Pipfiles and will not deploy if they are present.. To fix this, add the following lines to your .gitignore file:

```
Pipfile
Pipfile.lock
```

To update requirements.txt from Pipfile, use the command:

```
pipenv run pip freeze > requirements.txt
```

app.yaml should contain:

```
runtime: python37 
entrypoint: python main.py
Instance_class: F4
```

We must ensure that we override the default instance class F1 for F4. This allows us to use more memory, which our data heavy app requires. If you are encountering a 500 error while testing the deployment, the instance class likely needs to be updated. See: https://cloud.google.com/appengine/docs/standard/#instance_classes 


Be sure that main.py contains:

```
app.run(host='0.0.0.0', port=8080)
```

Note that this deployment uses Flask's built-in server. It should be updated to gunicorn when used in production. This would be configured via the entrypoint in app.yaml. 

To test deployment, run the bash scripts in tests/ directory. Ensure that they are calling the correct URLs.

## Deploying the Frontend Application


