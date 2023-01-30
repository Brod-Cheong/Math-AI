from ast import Assert
from multiprocessing.context import assert_spawning
from attr import validate
from flask.app import Flask
from application import db
import datetime as dt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from application.SolveEquation.ExpressionClass import Expression

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'login-users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    Username = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)

    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )


    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.Username)


class Entry(db.Model):


    __tablename__ = 'User_Predictions'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    userid= db.Column(
        db.Integer, nullable=False
        )

    Equationid= db.Column(
        db.Integer, nullable=True
        )
    
    FileName= db.Column(
        db.String(1000),
        nullable=False
    )

    predicted_value=db.Column(    
        db.String(1),
        nullable=False
    
    )

    time_stamp = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    @validates("FileName")
    def validate_filename(self, key, FileName):
        if FileName[-5:] == '.jpeg':    # only accept jpeg image files
            return FileName
        else:
            raise AssertionError('File type is unvalid')

    @validates("predicted_value")
    def validate_value(self, key, predicted_value):
        classes = ['-','+','0','1','2','3','4','5','6','7','8','9']
        if len(predicted_value) > 1:
            raise AssertionError("Predicted value is more than length of 1!")
        elif len(predicted_value) == 0:
            raise AssertionError("Did not receive predicted value!")
        elif predicted_value not in classes:
            raise AssertionError("Predicted value received is not a valid classified class")
        else:
            return predicted_value


    def set_predicted_value(self, value):
        self.predicted_value = value

    def set_Equationid(self, id):
        self.Equationid = id



class EquationEntry(db.Model):
    __tablename__ = 'User_Equations'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    userid= db.Column(
        db.Integer, nullable=False
        )

    equation= db.Column(
        db.String(255), nullable=False
        )


    Solved_value=db.Column(    
        db.Float,
        nullable=False
    )

    time_stamp = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    @validates("equation")
    def validate_filename(self, key, equation):
        EquationExpression=Expression(equation)
        error = EquationExpression.BuildParseTree()
        if error == False:
            return equation
        else:
            raise AssertionError('Equation is not valid!')

    @validates("Solved_value")
    def validate_Solved_value(self, key, Solved_value):
        try:
            check_int = float(Solved_value)
            return Solved_value
        except:
            raise AssertionError("Solved value is not a number")



