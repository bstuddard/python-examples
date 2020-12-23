# Flask Library Imports
from flask import request, json
from flask_restful import Resource

# Local object imports
from Starter.app import api
from Schemas.request_schemas import request_input_schema_multiple
from Schemas.response_schemas import response_schema_multiple

# ML Logic
from API.housing_clustering import cluster_houses


def parse_request(request):
    """Parse json from request

    Args:
        request: incoming request from User api call

    Returns:
        dict: json dict from request object
    """
    parsed_result = request.get_json(force=True)
    return parsed_result 


class HousingClustering(Resource):      
    
    def post(self):

        try:
            # Parse request into json and validate schema
            json_data = parse_request(request)
            errors = request_input_schema_multiple.validate(json_data)

            # If errors exist abort and send to api caller
            if errors:
                return str(errors), 400

            # Run Clustering
            results = cluster_houses(json_data)
            
            # Dump results and ok status back to caller
            return response_schema_multiple.dumps(results), 200

        # Unknown error return 404
        except:
            return 'Unknown Error', 404


api.add_resource(HousingClustering, '/HousingClustering')
