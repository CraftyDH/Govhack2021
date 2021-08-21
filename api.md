# Create Account
POST /create_account
HTTP_FORM Params
username: String no space, at least 5 character (in case space might becomes %20 when url encoding)
password: String 8-255 characters

return:
## Success
{
  "status": "success",
  "user": {
    "username": "jonte2",
    "password": "password",
    "public_key": "9049da8f7b8f8f7317df47ab0ead1180d612888153b95b58efa8ab5e4723c09f",
    "private_key": "df091bfc73489f2c86f876c0edf79b72d3fc6fa0199f396d7c4eb55ea4a20ec6",
    "local_ledger": []
  }
}
## Failure
{"status": "invalid username"}
{"status": "user exists"} // Already exists

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

# Login
POST /login
HTTP_FORM Params
username: String
password: String

## Success
{
  "status": "success",
  "user": {
    "username": "jonte2",
    "password": "password",
    "public_key": "9049da8f7b8f8f7317df47ab0ead1180d612888153b95b58efa8ab5e4723c09f",
    "private_key": "df091bfc73489f2c86f876c0edf79b72d3fc6fa0199f396d7c4eb55ea4a20ec6",
    "local_ledger": []
  }
}
## Failure
{"status": "user deleted"}
{"status": "incorrect password"}
{"status": "no user found"}