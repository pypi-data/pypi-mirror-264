import uuid
import requests
from datetime import datetime

def capture_api_info(req, res, next):
    request_id = str(uuid.uuid4())  # Generate a unique ID for the request

    base_api_url = req.url_root  # Get the base URL from the request

    request_info = {
        'requestId': request_id,
        'method': req.method,
        'url': req.url,
        'headers': dict(req.headers),
        'body': req.json if callable(getattr(req, 'json', None)) else req.get_json(),
        'query': req.args.to_dict(),
        'timestamp': datetime.now().isoformat(),
        'baseApiUrl': base_api_url
    }

    # Capture request information
    print('API Request:', request_info)

    # Attach the requestId to the response headers
    res.headers['X-Request-ID'] = request_id

    # Capture response information
    def capture_response():
        response_info = {
            'requestId': request_id,
            'statusCode': res.status_code,
            'headers': dict(res.headers),
            'body': res.get_json(),
            'timestamp': datetime.now().isoformat()
        }
        print('API Response:', response_info)

        # Send request information to the API endpoint
        try:
            api_key = os.environ.get('APISECURITYENGINE_API_KEY')  # Get the API key from the environment variable
            request_payload = {
                'api_key': api_key,
                'the_request': request_info
            }
            response = requests.post('https://backend.apisecurityengine.com/api/v1/mirroredScans/sendRequestInfo', json=request_payload)
            response.raise_for_status()
            print('Request information sent successfully.')
        except Exception as e:
            print('Error sending request information:', e)

    # Capture response information when the response is finished
    res.call_on_close(capture_response)

    # Pass control to the next middleware
    return next()

