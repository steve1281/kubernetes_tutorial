# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.employee import Employee  # noqa: E501
from swagger_server.models.employees import Employees  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_employees_get(self):
        """Test case for employees_get

        
        """
        query_string = [('body_limit', 20),
                        ('page_limit', 5)]
        response = self.client.open(
            '/v1/employees',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_employees_id_get(self):
        """Test case for employees_id_get

        
        """
        response = self.client.open(
            '/v1/employees/{id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_employees_post(self):
        """Test case for employees_post

        
        """
        body = Employee()
        response = self.client.open(
            '/v1/employees',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
