import pytest
import requests
from HotelSite.models import Payment
import datetime
def test_test():
    assert 1 == 1



@pytest.fixture(params=["test data", ''])
def payment():
    return Payment.objects.create( data="test data",)

@pytest.mark.django_db
def test_payment_creation(payment):
    assert payment.data in ['test data', '']

@pytest.mark.django_db
def test_payment_date_creation(payment):
    assert payment.created_at.day == datetime.datetime.today().day

@pytest.mark.parametrize("url", ['','booking/1','account','place','login','signup'])
def test_pages(url):
    response = requests.get('http://127.0.0.1:8000/'+url)
    assert response.status_code == 200

@pytest.mark.parametrize("url", ['signup','login'])
def test_illegal_post(url):
    response = requests.post('http://127.0.0.1:8000/'+url)
    assert response.status_code == 403