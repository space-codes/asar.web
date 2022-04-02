from marshmallow import Schema, fields

class LoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()

class RegisterSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    confirm_password = fields.Str()

class BasicSchema(Schema):
    message = fields.Str()
