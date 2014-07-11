#!/usr/bin/env python

from partsdb import app, db
import unittest
import os
import tempfile
from flask import json, url_for


TEST_DB = 'test.db'

class TestPartsDBHomePage(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test"""
        app.config['TESTING'] = True
        # Use memory only database for tests
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.session.remove()
        db.drop_all()

    def test_homepage(self):
        """Ensure homepage text is correct"""
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Welcome to PartsDB!', r.data)


class TestURLPaths(unittest.TestCase):
    def setUp(self):
        """Set up a blank temp database before each test"""
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_part_urls(self):
        """Check part URLs are valid"""
        with app.test_request_context():
            self.assertEqual(url_for('parts'), '/part/')
            self.assertEqual(url_for('part', id=1), '/part/1')
            self.assertEqual(url_for('new_part'), '/part/new')
            self.assertEqual(url_for('part_symbols', id=1), '/part/1/symbols/')
            self.assertEqual(url_for('part_footprints', id=1), '/part/1/footprints/')
            self.assertEqual(url_for('part_documents', id=1), '/part/1/documents/')

    def test_symbol_urls(self):
        """Check symbol URLs are valid"""
        with app.test_request_context():
            self.assertEqual(url_for('symbols'), '/symbol/')
            self.assertEqual(url_for('symbol', id=1), '/symbol/1')
            self.assertEqual(url_for('edit_symbol', id=1), '/symbol/1/edit')
            self.assertEqual(url_for('new_symbol'), '/symbol/new')

    def test_footprint_urls(self):
        """Check footprint URLs are valid"""
        with app.test_request_context():
            self.assertEqual(url_for('footprints'), '/footprint/')
            self.assertEqual(url_for('footprint', id=1), '/footprint/1')
            self.assertEqual(url_for('edit_footprint', id=1), '/footprint/1/edit')
            self.assertEqual(url_for('new_footprint'), '/footprint/new')

    def test_document_urls(self):
        """Check document URLs are valid"""
        with app.test_request_context():
            self.assertEqual(url_for('documents'), '/document/')
            self.assertEqual(url_for('document', id=1), '/document/1')
            self.assertEqual(url_for('edit_document', id=1), '/document/1/edit')
            self.assertEqual(url_for('new_document'), '/document/new')

    def test_user_urls(self):
        """Check user URLs are valid"""
        with app.test_request_context():
            self.assertEqual(url_for('user', username='foo'), '/u/foo')
            self.assertEqual(url_for('users'), '/users/')
            self.assertEqual(url_for('edit_user', username='foo'), '/u/foo/edit')


class TestPartsDBPartsListPage(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test"""
        app.config['TESTING'] = True
        # Use memory only database for tests
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.drop_all()

    def test_empty_db(self):
        """Check empty db help text"""
        r = self.app.get('/part/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('There are no parts in this database!', r.data)
        self.assertIn('You can add a new part', r.data)
        # self.assertIn('<a href=' + url_for('new_part') + '>here.</a>', r.data)
        self.assertNotIn('<table>', r.data)


if __name__ == '__main__':
    unittest.main()
