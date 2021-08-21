# Create Account
POST /create_account
HTTP_FORM Params
username: String
password: String

return:
## Success
User object
## Failure
{"username": None} // Already exists

## Modify Password
POST /modify_password
HTTP_FORM Params
username: String
oldpass: String
newpass: String

## Success
{"status": "succuss"}

## Failures
{"status": "incorrect password"}
{"status": "no user found"}

# Modify Username
POST /modify_username
HTTP_FORM Params
oldusername: String
newusername: String
password: String

## Success
{"status": "succuss"}

## Failures
{"status": "incorrect password"}
{"status": "no user found"}

# Delete User
POST /delete_user
HTTP_FORM Params
username: String
password: String

## Success
{"status": "succuss"}

## Failures
{"status": "incorrect password"}
{"status": "no user found"}

