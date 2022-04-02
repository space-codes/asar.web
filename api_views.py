from marshmallow import Schema, fields

class LoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()

class RegisterSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    confirm_password = fields.Str()

class PredictSchema(Schema):
    image = fields.Str()

class PredictionDetailsSchema(Schema):
    id = fields.Int()
    image = fields.Str()
    result = fields.Str()

class PredictionListSchema(Schema):
    results = fields.List(fields.Nested(PredictionDetailsSchema))

class BasicSchema(Schema):
    message = fields.Str()
