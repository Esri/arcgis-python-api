# docker

Some useful docker images for utilizing the ArcGIS API for Python in your workflows

## LambdaBaseImage

#### ghcr.io/esri/arcgis-python-api-lambda:latest

To use this image, setup your dockerfile like:
```
FROM ghcr.io/esri/arcgis-python-api-lambda:latest
COPY app.py ${LAMBDA_TASK_ROOT}
```

your app.py should have a handler method:
```
import arcgis

def handler(event, context):
    """
    AWS Lambda Handler
    """
    print(f"Hello from AWS Lambda using ArcGIS API for Python {arcgis.__version__}!")
```

Push to your _private_ AWS ECR instance, and configure lambda to run from this container image.  As of this writing, public AWS ECR instances are not supported for lambda.

## AzureFunctionsBaseImage

The AzureFunctionsBase image has been deprecated in favor of using the standard runtime for Azure Functions development.

See `samples/devops_azure_functions` for a sample using the standard runtime deployment.