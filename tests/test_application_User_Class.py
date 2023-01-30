#Imports
from os import error
from application.models import User
import datetime as datetime
import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from flask import json

#---------------------------------------------------------------------------------------------------------------

#Unit Test

# check if valid username and password can be logged in
@pytest.mark.parametrize("userlist",[
    ['brod123','brod123']
    ,['joshua123','joshua123']
    ])

def test_UserLogin(userlist,capsys):
    with capsys.disabled():

        new_User = User()
        new_User.set_password(userlist[0])
        assert new_User.check_password(userlist[1])
        # assert new_User.password==userlist[1]

# Expected Failure for Consistency Testing
@pytest.mark.xfail(reason="Hash Password does not match")
@pytest.mark.parametrize("userlist",[
    ['brod123','joshua123']     # wrong password
    ,['joshua123','brod123']    # wrong password
    ])

def test_UserConsistencyTesting(userlist,capsys):
    with capsys.disabled():

        new_User = User()
        new_User.set_password(userlist[0])
        assert new_User.check_password(userlist[1])
        
#---------------------------------------------------------------------------------------------------------------
# Unit Testing


