from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils.types import TSVectorType
from flask_sqlalchemy import BaseQuery
from sqlalchemy.sql import exists
from sqlalchemy.ext.hybrid import hybrid_property
from mods.extensions import db


make_searchable()


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String)
    contract_date = db.Column(db.Date)
    filename = db.Column(db.String)
    path = db.Column(db.String)


class SymbolQuery(BaseQuery, SearchQueryMixin):
    pass


class Symbol(db.Model):
    query_class = SymbolQuery

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.Unicode(16))
    description = db.Column(db.Unicode(64))
    exchange = db.Column(db.Unicode(16))
    category = db.Column(db.Unicode(32))
    search_vector = db.Column(TSVectorType('symbol', 'description',
                                           'exchange', 'category'))

    @hybrid_property
    def downloadable(self):
        return db.session.query(exists().where(File.symbol == self.symbol)).scalar()


class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    subject = db.Column(db.String)
    content = db.Column(db.String)
    recieved_on = db.Column(db.DateTime)
