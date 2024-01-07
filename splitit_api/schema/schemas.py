from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, Parameter, IN_QUERY, TYPE_NUMBER, TYPE_ARRAY


class AuthRequestSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(
            type=TYPE_OBJECT,
            properties={
                'idToken': Schema(
                    type=TYPE_STRING,
                    description='Id token issues by firebase'
                ),
            },
            required=['idToken'],
            **kwargs
        )


email_query_param = Parameter(
    'email',
    in_=IN_QUERY,
    type=TYPE_STRING,
    description='Email address to search for',
    required=True,
)


class AddUserToGroupRequestSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(
            type=TYPE_OBJECT,
            properties={
                'user_id': Schema(
                    type=TYPE_STRING,
                    description='User id to add to the group'
                ),
            },
            required=['user_id'],
            **kwargs
        )


class MessageResponseSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(
            type=TYPE_OBJECT,
            properties={
                'message': Schema(
                    type=TYPE_STRING,
                    description='Success message'
                ),
            },
            **kwargs
        )


class GetBalancesResponseSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(
            type=TYPE_ARRAY,
            items=Schema(
                type=TYPE_OBJECT,
                properties={
                    'spender': Schema(
                        type=TYPE_STRING,
                        description='User id who has spent the amount'
                    ),
                    'borrower': Schema(
                        type=TYPE_STRING,
                        description='User id who has borrowed the amount'
                    ),
                    'amount': Schema(
                        type=TYPE_NUMBER,
                        description='Balance amount. Borrower owes this amount to spender'
                    )
                },
            ),
            **kwargs
        )