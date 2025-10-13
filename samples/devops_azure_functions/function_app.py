import azure.functions as func
import logging
import arcgis

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="hello")
def hello(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed `hello` request.')
    return func.HttpResponse(f"Hello from Azure Functions using ArcGIS API for Python {arcgis.__version__}!")
