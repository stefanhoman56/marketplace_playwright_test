import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
import uuid
from helpers.ticket import Ticket
import variables
from helpers.ticket import create_ticket

@pytest.mark.regression
def test_ticket_resolve_from_ticket_info_field(page, login, api_request_context):
    ticket = Ticket()
    ticket.create(api_request_context)

    customer_name = str(uuid.uuid4())
    customer_id, _ = create_customer(customer_name, api_request_context)


    ticket_id, ticket_num = create_ticket(customer_id,api_request_context)

    quick_view_selector = '#quick-view-ticket-{}'.format(ticket_id)
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)
    page.click('//a[@data-original-title="Resolve"]')
    page.goto(f'{variables.base_url}/tickets/{ticket_id}')
    assert page.locator(f'span#best_in_place_ticket_{ticket_id}_status').inner_text() == 'Resolved'
