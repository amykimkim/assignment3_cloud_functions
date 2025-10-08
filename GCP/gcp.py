import json
import functions_framework

@functions_framework.http
def hello_http(request):
   
    # Prefer JSON body; fall back to query parameters for convenience
    data = request.get_json(silent=True) or {}
    args = request.args or {}

    crp = data.get("CRP", args.get("CRP"))

    # Presence check
    if crp is None:
        return (
            json.dumps({"error": "CRP is required."}),
            400,
            {"Content-Type": "application/json"},
        )

    # Type/convert check
    try:
        crp_val = float(crp)
    except (TypeError, ValueError):
        return (
            json.dumps({"error": "'CRP' must be a number."}),
            400,
            {"Content-Type": "application/json"},
        )

    status = "normal" if (crp_val < 8.0) else "abnormal"
    category = "Normal (<8.0)" if status == "normal" else "Elevated (simplified)"

    payload = {
        "CRP": crp_val,
        "status": status,
        "category": category,
    }

    return json.dumps(payload), 200, {"Content-Type": "application/json"}