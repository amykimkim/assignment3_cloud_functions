import functions_framework

@functions_framework.http
def hello_http(request):
    request_args = request.args

    if request_args and 'crp' in request_args:
        response_crp = request_args['crp']
    else:
        response_crp = 'You did not enter a CRP into the argument'

    crp_abnormal_normal = 'abnormal' if response_crp != 'N/A' and (float(response_crp) > 8.0) else 'normal'

    response = f"Response: CRP level is {response_crp}; CRP status is {crp_abnormal_normal}"

    return response