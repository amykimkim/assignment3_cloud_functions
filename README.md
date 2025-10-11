# assignment3_cloud_functions
504 assignment 3 - cloud functions

Link to recording: https://youtu.be/SMsNSc7pKyo 

## Lab Rules - C-reactive Protein (CRP)
I chose to use CRP for this assignment. CRP is a lab-value that is an inflammatory marker. It is a protein produced by the liver that increases if the body produces inflammation due to infection. It can be checked via a simple blood test. It is measured in miligrams per liter (mg/L). Results that are > 8 is considered high/abnormal.
Citation:
https://www.mayoclinic.org/tests-procedures/c-reactive-protein-test/about/pac-20385228 

## Google Cloud Platform
Region: europe-west1

Endpoint URL: https://crp-value-checker-872931411598.europe-west1.run.app 

### Deployment commands/steps executed:
```
import functions_framework

@functions_framework.http
def hello_http(request):
    request_args = request.args

    if request_args and 'crp' in request_args:
        response_crp = request_args['crp']
    else:
        response_crp = 'Please enter a CRP value in the argument'

    crp_abnormal_normal = 'abnormal' if response_crp != 'N/A' and (float(response_crp) > 8.0) else 'normal'

    response = f"Response: CRP level is {response_crp}; CRP status is {crp_abnormal_normal}"

    return response
```



#### Screenshot showing functionality that have your custom URLs, along with outputs:
![screenshot](GCP/GCP_cloud_run_screenshot.png)

#### Example requests invocations that work as shown in video:
Normal:
![normal](GCP/GCP_colab_output_normal.png)

Abnormal:
![abnormal](GCP/GCP_colab_output_abnormal.png)

## Azure
Region: east-US

Endpoint URL: https://crp-checker-test-h8g3g2d5dhbzfwdp.eastus-01.azurewebsites.net/api/http_trigger1?code=yMFPEoOI7xDw9sxUFqoeeThk02uSase4uOervOJ6mYkqAzFu9TeNZw==


### Deployment commands/steps executed:
``` 
import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger1")
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    crp_value = None
    try:
        crp_value = req.params.get('crp')
        if not crp_value:
            req_body = req.get_json()
            crp_value = req_body.get('crp')
    except ValueError:
        pass # Could not get JSON body

    output_message = "Please enter a CRP value in the query string or request body."
    status_code = 200

    if crp_value is not None:
        try:
            crp_float = float(crp_value)
            if crp_float <= 8.0:
                output_message = f"CRP level is {crp_value}; CRP less than or equal to 8 is normal"
            else:
                output_message = f"CRP level is {crp_value}; CRP greater than 8 is abnormal"
        except ValueError:
            output_message = f"Invalid input provided for CRP: {crp_value}. Please provide a numeric value."
            status_code = 400 # Bad Request for invalid input

    return func.HttpResponse(
         f"Response: {output_message}",
         status_code=status_code
    )
```

Screenshots showing functionality that have your custom URLs:
![azure_page](Azure/Azure_cloud_run_screenshot.png)

#### Example requests invocations that work as shown in your video:
Normal:
![normal](Azure/Azure_test_output_normal.png)

Abnormal:
![abnormal](Azure/Azure_test_output_abnormal.png)

## Short comparison paragraph of the two clouds
While both Azure Functions and Google Cloud Functions were straightforward to set up and deploy, I found Azure to be slightly more beginner-friendly. A key reason for this was the ability to test the function directly within the same page in the Azure portal, which streamlined the development process. In contrast, testing with Google Cloud Functions often required navigating back and forth between different pages to make changes and then test them, which felt less integrated. Furthermore, for Google Cloud Functions, there seemed to be a longer delay for code changes to be saved and become available for testing in Google Colab after each modification