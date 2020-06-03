import connexion
import six

from swagger_server.models.employee import Employee  # noqa: E501
from swagger_server.models.employees import Employees  # noqa: E501
from swagger_server import util


def employees_get(body_limit=None, page_limit=None):  # noqa: E501
    """employees_get

    Obtain information about employees from the HR database # noqa: E501

    :param body_limit: The amount of employes returned
    :type body_limit: int
    :param page_limit: The pages to return employees info returned
    :type page_limit: int

    :rtype: Employees
    """
    return 'do some magic!'


def employees_id_get(id_):  # noqa: E501
    """employees_id_get

    Obtain information about specific employee # noqa: E501

    :param id: The ID of the employee
    :type id: int

    :rtype: Employee
    """
    return 'do some magic!'


def employees_post(body):  # noqa: E501
    """employees_post

    Creates a new employee in the database # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Employee.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
