from marshmallow import Schema, fields

class ClusterResultSchema(Schema):
    row = fields.Integer(required=True, strict=True)
    group = fields.Integer(required=True, strict=True)

# Output Schema
response_schema_multiple = ClusterResultSchema(many=True)