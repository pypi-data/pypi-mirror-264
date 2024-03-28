from marshmallow import RAISE, Schema, ValidationError, fields

list_issue_code = ["INBOUND", "OUTBOUND", "RETURN_GOODS", "INVENTORY_CHECKING"]

list_from_system = ["WMS", "OMS"]


def validate_issue_code(val):
    if val not in list_issue_code:
        raise ValidationError(f"issue_code in : {list_issue_code}")


def validate_from_system(val):
    if val not in list_from_system:
        raise ValidationError(f"from_system in : {list_from_system}")


class NewTicketSchema(Schema):
    issue_code = fields.Str(required=True, validate=validate_issue_code)
    from_system = fields.Str(required=True, validate=validate_from_system)
    partner_code = fields.Str(required=True)
    ticket_name = fields.Str(required=True)
    requested_email = fields.Str(required=True)
    description = fields.Str(required=True)
    attachments = fields.Str(required=True)
    lambda_type = fields.Str(required=True)

    class Meta:
        strict = True
        unknown = RAISE


class NewSellerSchema(Schema):
    partner_code = fields.Str(required=True)
    email = fields.Str(required=True)
    cs_email = fields.Str(required=True)
    lambda_type = fields.Str(required=True)

    class Meta:
        strict = True
        unknown = RAISE
