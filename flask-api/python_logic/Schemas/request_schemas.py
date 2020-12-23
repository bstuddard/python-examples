from marshmallow import Schema, fields

class RequestInput(Schema):
    square_footage = fields.Integer(required=True, strict=True)
    number_of_rooms = fields.Integer(required=True, strict=True)
    price = fields.Integer(required=True, strict=True)

# Input Schema
request_input_schema_multiple = RequestInput(many=True)