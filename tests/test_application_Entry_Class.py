from os import error
from application.models import Entry
import datetime as datetime
import pytest
from flask import json


# #---------------------------------------------------------------------------------------------------------------

# #Unit Test

@pytest.mark.parametrize("entrylist",[
    [1,3,'test.jpeg', '+',],
    [1,2,'test2.jpeg', '-',],
    [1,1,'test3.jpeg', '1',]
])

def test_EntryClass(entrylist,capsys):
    with capsys.disabled():
        print(entrylist)
        classes = ['-','+','0','1','2','3','4','5','6','7','8','9']
        now = datetime.datetime.utcnow()       

        new_entry = Entry (
            userid= entrylist[0],
            Equationid= entrylist[1],
            FileName= entrylist[2],
            predicted_value= entrylist[3],
            time_stamp= now
        )
        
        assert ((new_entry.userid   == entrylist[0]))
        assert ((new_entry.Equationid  == entrylist[1]))
        assert ((new_entry.FileName   == entrylist[2])  & (new_entry.FileName[-5:] == '.jpeg'))
        assert ((new_entry.predicted_value  == entrylist[3]) & (len(new_entry.predicted_value) == 1) & (new_entry.predicted_value in classes))
        assert (new_entry.time_stamp   == now)

#Expected Failure, Validation and Range Testing

@pytest.mark.xfail(reason="arguments are not valid")
@pytest.mark.parametrize("entrylist",[
    [1,3,'test.jpeg', '',], # empty predicted value
    [1,3,'test.jpeg', '**',], # predicted value invalid
    [1,2,'test2.png', '-',]    # wrong file type
])

def test_EntryValidationTesting(entrylist,capsys):
       with capsys.disabled():
        print(entrylist)
        now = datetime.datetime.utcnow()       
        classes = ['-','+','0','1','2','3','4','5','6','7','8','9']
        new_entry = Entry (
            userid= entrylist[0],
            Equationid= entrylist[1],
            FileName= entrylist[2],
            predicted_value= entrylist[3],
            time_stamp= now
        )
        
        assert ((new_entry.userid   == entrylist[0]))
        assert ((new_entry.Equationid   == entrylist[1]))
        assert ((new_entry.FileName    == entrylist[2])  & (new_entry.FileName[-5:] == '.jpeg'))
        assert ((new_entry.predicted_value  == entrylist[3]) & (len(new_entry.predicted_value) == 1) & (new_entry.predicted_value in classes))
        assert (new_entry.time_stamp   == now)