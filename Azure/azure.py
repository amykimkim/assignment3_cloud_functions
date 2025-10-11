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


#BASE_URL = "https://python-test-dev1-g6bth0chgyegdtaf.canadacentral-01.azurewebsites.net"
#FUNCTION = "http_trigger1"
#KEY = "yMFPEoOI7xDw9sxUFqoeeThk02uSase4uOervOJ6mYkqAzFu9TeNZw=="  # function or host key

#url = f"https://crp-checker-test-h8g3g2d5dhbzfwdp.eastus-01.azurewebsites.net/api/http_trigger1?code=yMFPEoOI7xDw9sxUFqoeeThk02uSase4uOervOJ6mYkqAzFu9TeNZw=="
#params = {"crp_value": "9", "code": "yMFPEoOI7xDw9sxUFqoeeThk02uSase4uOervOJ6mYkqAzFu9TeNZw=="}

#print(url)
#print(params)

#azure_response = requests.get(url, params=params, timeout=10)

#print(azure_response.text)