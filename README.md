# Grindery Nexus Gmail Connector Schema Definitions

## Index

- [ConnectorSchema](#connectorschema)
  - [ParamsSchema](#ParamsSchema)
    - [Credentials](#Credentials)
    - [Fields](#Fields)
- [ResponseSchema](#ResponseSchema)
  - [ResultSchema](#ResultSchema)
    - [Fields](#Fields)


## ConnectorSchema
An `object` that represents a connector app.

Key | Type | Required | Description
----|------|----------|------------
`jsonrpc` | `string` | yes | Version number of jsonrpc.
`method` | `string` | yes | A method to uniquely identify this connector (e.g "sendEmail").
`params` | array<[ParamsSchema](#ParamsSchema)> | yes | The params fields the user needs to configure for this trigger.
`id` | integer | yes | identifier.


#### ParamsSchema

An `object` that defines an input.

Key | Type | Required | Description
----|------|----------|------------
`key` | `string` | yes | A unique key for gmail connector (e.g "gMailSender").
`sessionId` | `string` | yes | session Id.
`credentials` | array<[Credentials](#Credentials)> | no | The credential fields the user needs to configure for this trigger.
`fields` | array<[Fields](#Fields)> | no | The data fields the user needs to configure for this trigger.



#### Credentials

An `object` that defines credentials.

Key | Type | Required | Description
----|------|----------|------------
`token` | `string` | yes | access token for google account.
`refresh_token` | `string` | yes | refresh_token for google account.
`token_uri` | `string` | yes | token_uri for google account.
`client_id` | `string` | yes | client_id for google account.
`client_secret` | `string` | yes | client_secret for google account.
`Scopes` | `array` | yes | Array of scope for Gmail.
`expiry` | `string` | yes | expiry for access token.


#### Fields

An `object` that defines an input or output field.

Key | Type | Required | Description
----|------|----------|------------
`to` | `string` | yes | recipient email address.
`cc` | `string` | no | carbon copy email address.
`bcc` | `string` | no | blind carbon copy email address.
`subject` | `string` | yes | subject of email.
`message` | `string` | yes | content of message.


## ResponseSchema
An `object` that response schema.

Key | Type | Required | Description
----|------|----------|------------
`jsonrpc` | `string` | yes | Version number of jsonrpc.
`result` | array<[ResultSchema](#ResultSchema)> | yes | The result fields.
`id` | integer | yes | identifier.


#### ResultSchema
An `object` that result field.

Key | Type | Required | Description
----|------|----------|------------
`key` | `string` | yes | A unique key for gmail connector (e.g "gMailSender").
`sessionId` | `string` | yes | session Id.
`payload` | array<[Fields](#Fields)> | no | The payload fields.
