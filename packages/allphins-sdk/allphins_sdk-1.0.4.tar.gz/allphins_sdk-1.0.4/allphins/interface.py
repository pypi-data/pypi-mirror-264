"""This module provides methods to interact with the allphins API."""
import logging
import uuid
from typing import Optional

from pandas import DataFrame

from allphins.models import Policy
from allphins.models import Portfolio
from allphins.models import Risk
from allphins.models.policy import PolicyStatuses
from allphins.utils import validate_uuid4

logger = logging.getLogger(__name__)


def get_portfolios() -> DataFrame:
    """Get all the portfolios.

    Returns:
        dataframe of the portfolios' representation.
    """
    return Portfolio.all().to_pandas()


def get_policies(
    portfolio_id: Optional[uuid.UUID] = None,
    status: Optional[str] = 'written',
    filter_rule: Optional[str] = 'today',
) -> DataFrame:
    """Get the policies, using filtering parameters.

    Values for status:
        * quote
        * written
        * expired
        * declined
        * not_taken_up
        * work_in_progress
        * deleted

    Values for filter_rule:
        * today (policies live today)
        * previous_1_1 (policies live on the previous 1st of January)

    Args:
        portfolio_id (Optional[uuid.UUID]): UUID of the portfolio.
        status (Optional[str]): Status of the policy
        filter_rule (Optional[str]): Filter rule to apply

    Returns:
        dataframe of the policies' representation.
    """
    filters: dict = {}

    if portfolio_id:
        if not validate_uuid4(portfolio_id):
            raise ValueError(f'{portfolio_id} is not a valid UUID.')
        filters['portfolio_id'] = portfolio_id

    if filter_rule:
        if filter_rule not in ['today', 'previous_1_1']:
            raise ValueError(f'{filter_rule} is not a valid filter rule.')
        filters['filter_rule'] = filter_rule

    if status:
        try:
            PolicyStatuses(status)
        except ValueError:
            raise ValueError(f'{status} is not a valid status.')
        filters['status'] = status

    return Policy.filtered_policies(filters).to_pandas()


def get_risks(
    portfolio_id: Optional[uuid.UUID] = None,
    datasource_id: Optional[uuid.UUID] = None,
    scenario_id: Optional[int] = None,
) -> DataFrame:
    """Get the risks, using filtering parameters.

    At least one of the parameters must be provided.

    Fetching the risks from the API could take a while, depending on the amount of data to retrieve.

    Args:
        portfolio_id (Optional[uuid.UUID]): UUID of the portfolio.
        datasource_id (Optional[uuid.UUID]): UUID of the datasource_id.
        scenario_id (Optional[int]): id of the scenario_id.

    Returns:
        dataframe of the risks' representation.
    """
    if not any([portfolio_id, datasource_id, scenario_id]):
        raise ValueError('At least one of the parameters must be provided.')

    filters: dict = {}

    if portfolio_id:
        if not validate_uuid4(portfolio_id):
            raise ValueError(f'{portfolio_id} is not a valid UUID.')
        filters['portfolios'] = portfolio_id

    if datasource_id:
        if not validate_uuid4(datasource_id):
            raise ValueError(f'{datasource_id} is not a valid UUID.')
        filters['datasource_id'] = datasource_id

    if scenario_id:
        filters['scenario_id'] = scenario_id

    logger.info('Fetching risks from the API, this could take a while...')

    return Risk.filtered_risk(filters).to_pandas()
