from os import error
from application.models import EquationEntry
from application.SolveEquation.ExpressionClass import Expression
from application.SolveEquation.Evaluator import Evaluator
import datetime as datetime
import pytest
from flask import json


# #---------------------------------------------------------------------------------------------------------------

# #Unit Test

@pytest.mark.parametrize("equationentrylist",[
    [1,'1+3', '4'],
    [2,'1+3-4', '0'],
    [3,'5-6', '-1']
])

def test_Valid_EquationEntryClass(equationentrylist,capsys):
    with capsys.disabled():
        print(equationentrylist)
        now = datetime.datetime.utcnow()  
        print( equationentrylist[2])     
        new_entry = EquationEntry (
            userid= equationentrylist[0],
            equation= equationentrylist[1],
            Solved_value= equationentrylist[2],
            time_stamp= now
        )
        print(new_entry.Solved_value)
        EquationExpression=Expression(new_entry.equation)
        evaluator = Evaluator( "", "~", '1')
        ValidBracket,ValidOperators,fullySeperatedTokens=EquationExpression.Validate_UserInput()
        Expression_value = evaluator.evaluateSingleExpression(fullySeperatedTokens)
        assert ((new_entry.userid   == equationentrylist[0]))
        assert ((new_entry.equation   == equationentrylist[1]) & (new_entry.equation == EquationExpression.getExpression()) & (ValidBracket == True) & (ValidOperators==True))
        assert ((new_entry.Solved_value == equationentrylist[2]) & (new_entry.Solved_value == str(Expression_value)))
        assert (new_entry.time_stamp   == now)

#Expected Failure, Validation and Range Testing

@pytest.mark.xfail(reason="arguments are not valid")
@pytest.mark.parametrize("equationentrylist",[
    [1,'1+3', '5'],     # Evaluation Failed
    [2,'1-2-', '0'],   # Invalid equation
])

def test_EntryValidationTesting(equationentrylist,capsys):
       with capsys.disabled():
        print(equationentrylist)
        now = datetime.datetime.utcnow()       

        new_entry = EquationEntry (
            userid= equationentrylist[0],
            equation= equationentrylist[1],
            Solved_value= equationentrylist[2],
            time_stamp= now
        )
        
        print(new_entry.Solved_value)
        EquationExpression=Expression(new_entry.equation)
        evaluator = Evaluator( "", "~", '1')
        ValidBracket,ValidOperators,fullySeperatedTokens=EquationExpression.Validate_UserInput()
        Expression_value = evaluator.evaluateSingleExpression(fullySeperatedTokens)
        assert ((new_entry.userid   == equationentrylist[0]))
        assert ((new_entry.equation   == equationentrylist[1]) & (new_entry.equation == EquationExpression.getExpression()) & (ValidBracket == True) & (ValidOperators==True))
        assert ((new_entry.Solved_value == equationentrylist[2]) & (new_entry.Solved_value == str(Expression_value)))
        assert (new_entry.time_stamp   == now)
