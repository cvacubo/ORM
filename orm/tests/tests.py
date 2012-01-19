import unittest
from nose.tools import ok_, eq_
from pyramid.config import Configurator
from pyramid import testing
from orm.views import view_relations
from . import util

def _initTestingDB():
    from sqlalchemy import create_engine
    from orm.models import initialize_sql
    session = initialize_sql(create_engine('sqlite://'))
    return session

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        _initTestingDB()

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        request = testing.DummyRequest()
        inf = view_relations(request)

        self.assertEqual(inf[0]['parent'], 'Alexander')
        self.assertEqual(inf[1]['parent'], 'Olga')


    def test_child(self):
        p0 = util.make_parent_with_child("Inga Maksapetyan", "Artem")
        ok_(p0.children)

        #for child in p0.children:
        #    ok_(child.is_child("Artem"))

        ok_(p0.children[0].is_child("Artem"))
        eq_(p0.children[0].name, "Artem", "Name is not Artem")

        ok_(p0.children[0].is_child("Arthur"))


        p1 = util.make_parent("Anna Maksapetyan")
        eq_(p1.children, [], "Has children")
