import unittest
import requests
import json
import uuid
import os
from datetime import datetime, timedelta
from dateutil import parser
import pytz
import lusid
import lusid.models as models
from unittest import TestCase
from msrest.authentication import BasicTokenAuthentication
from TestDataUtilities import TestDataUtilities
from InstrumentLoader import InstrumentLoader
import pandas as pd
import shrine
import shrine.models as shrine_models
import time


try:
    # Python 3.x
    from urllib.request import pathname2url
except ImportError:
    # Python 2.7
    from urllib import pathname2url


class TestAccessFinbourneApi(TestCase):
    client = None
    shrine_client = None
    effective_date = datetime(2017, 1, 1, tzinfo=pytz.utc)

    @classmethod
    def setUpClass(cls):

        cls.ISIN_PROPERTY_KEY = "Instrument/default/Isin"
        cls.SEDOL_PROPERTY_KEY = "Instrument/default/Sedol"
        cls.TICKER_PROPERTY_KEY = "Instrument/default/Ticker"
        cls.FIGI_SCHEME = "Figi"
        cls.CUSTOM_INTERNAL_SCHEME = "ClientInternal"
        cls.GROUPBY_KEY = "Instrument/default/Name"
        cls.AGGREGATION_KEY = "Holding/default/PV"
        cls.sorted_instrument_ids = []
        cls.instrument_universe = {}
        # Load our configuration details from the environment variables
        token_url = os.getenv("FBN_TOKEN_URL", None)
        cls.api_url = os.getenv("FBN_LUSID_API_URL", None)
        username = os.getenv("FBN_USERNAME", None)
        password_raw = os.getenv("FBN_PASSWORD", None)
        client_id_raw = os.getenv("FBN_CLIENT_ID", None)
        client_secret_raw = os.getenv("FBN_CLIENT_SECRET", None)

        # If any of the environmental variables are missing use a local secrets file
        if token_url is None or username is None or password_raw is None or client_id_raw is None \
                or client_secret_raw is None or cls.api_url is None:

            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(dir_path, "secrets.json"), "r") as secrets:
                config = json.load(secrets)

            token_url = os.getenv("FBN_TOKEN_URL", config["api"]["tokenUrl"])
            username = os.getenv("FBN_USERNAME", config["api"]["username"])
            password = pathname2url(os.getenv("FBN_PASSWORD", config["api"]["password"]))
            client_id = pathname2url(os.getenv("FBN_CLIENT_ID", config["api"]["clientId"]))
            client_secret = pathname2url(os.getenv("FBN_CLIENT_SECRET", config["api"]["clientSecret"]))
            cls.api_url = os.getenv("FBN_LUSID_API_URL", config["api"]["apiUrl"])

        else:
            password = pathname2url(password_raw)
            client_id = pathname2url(client_id_raw)
            client_secret = pathname2url(client_secret_raw)

        # Prepare our authentication request
        token_request_body = ("grant_type=password&username={0}".format(username) +
                              "&password={0}&scope=openid client groups".format(password) +
                              "&client_id={0}&client_secret={1}".format(client_id, client_secret))
        headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

        # Make our authentication request
        okta_response = requests.post(token_url, data=token_request_body, headers=headers)

        # Ensure that we have a 200 response code
        assert okta_response.status_code == 200

        # Retrieve our api token from the authentication response
        cls.api_token = {"access_token": okta_response.json()["access_token"]}

        # Initialise our API client using our token so that we can include it in all future requests
        credentials = BasicTokenAuthentication(cls.api_token)
        cls.client = lusid.LUSIDAPI(credentials, cls.api_url)

        ##################################
        # create scopes here
        # prettyprint.heading('Analyst Scope Code', analyst_scope_code)

        # Create scope
        uuid_gen = uuid.uuid4()
        scope = "finbourne"
        analyst_scope_code = 'notepad-access-' + scope          # + "-" + str(uuid_gen)


        ##################################
        # Create policies with access, timing etc (really show off shrine capabilities)
        # Create roles with groups of these policies
        # In Okta, create accounts. Attached roles to these accounts


        #get json file
        file1 = "roleCreationRequestPM.json"
        file2 = "roleCreationRequestPV.json"
        file3 = "policyCreationRequestView.json"
        file4 = "policyCreationRequestMod.json"
        json1 = cls.import_json_file(file1)
        json2 = cls.import_json_file(file2)
        json3 = cls.import_json_file(file3)
        json4 = cls.import_json_file(file4)

        # Pass as HTTP requests to lusid

        cls.shrine_client = shrine.FINBOURNEShrineAPI(credentials)

        #create a policy



        model_for_spec = shrine_models.ForSpec()
        eff_date_rel = shrine_models.EffectiveDateRelative()
        eff_date_rel.date_property = cls.effective_date
        model_for_spec.effective_date_relative = cls.effective_date

        policy_activate_date = datetime(2016, 1, 1, tzinfo=pytz.utc)
        policy_deactivate_date = datetime(2019, 1, 1, tzinfo=pytz.utc)
        model_when_spec = shrine_models.WhenSpec()
        model_when_spec.activate = policy_activate_date
        model_when_spec.deactivate = policy_deactivate_date

        scope_code_id_path_def = shrine_models.ScopeAndCodeIdPathDefinition(scope=analyst_scope_code, code="Performance")
        id_path_def = shrine_models.IdPathDefinition(scope_code_id_path_def)

        path1 = shrine_models.PathDefinition(id_path_definition=id_path_def)

        policy1 = shrine_models.PolicyCreationRequest(grant='ALLOW',
                                                      paths=[path1],
                                                      when=model_when_spec,
                                                      description='Blah',   # runtime resource restrictions
                                                      for_property=[model_for_spec],          # temporal restriction
                                                      )

        response = cls.shrine_client.api_policies_post(policy1)

        # Start the clock on timing
        start = time.time()

        ##################################
        # Create and load in instruments
        inst_list = cls.load_instruments_from_file()
        cls.upsert_intruments(inst_list)

        end = time.time()
        print('Inst load: ' + str(end-start))

        ##################################
        # Create transactions portfolio
        # Define unique code for our portfolio

        transaction_portfolio_code = 'DJII_30'

        # The date our portfolios were first created
        portfolio_creation_date = cls.effective_date

        # Create the request to add our portfolio
        transaction_portfolio_request = models.CreateTransactionPortfolioRequest(
            display_name=transaction_portfolio_code,
            code=transaction_portfolio_code,
            base_currency='USD',
            description='Paper transaction portfolio',
            created=portfolio_creation_date)

        # Call LUSID to create our portfolio
        portfolio_response = cls.client.create_portfolio(
            scope=analyst_scope_code,
            create_request=transaction_portfolio_request)

        # Pretty print the response from LUSID
        # prettyprint.portfolio_response(portfolio_response)

        ##################################
        # Populating our analyst's portfolio with a starting cash balance

        # Set the date from which the cash balance will apply to be just after portfolio creation
        holdings_effective_date = cls.effective_date

        # Define our initial cash balance
        initial_cash_balance = 30000000     # $30mil, so 1mil per line?

        # Create a holding adjustment to set our initial cash balance
        holding_adjustment = [
            models.AdjustHoldingRequest(
                instrument_identifiers={'Instrument/default/Currency': 'USD'},
                tax_lots=[
                    models.TargetTaxLotRequest(
                        units=initial_cash_balance,
                        cost=models.CurrencyAndAmount(
                            amount=initial_cash_balance,
                            currency='USD'),
                        portfolio_cost=initial_cash_balance,
                        price=1)
                ]
            )
        ]

        # Call LUSID to set our initial cash balance
        set_holdings_response = cls.client.set_holdings(
            scope=analyst_scope_code,
            code=transaction_portfolio_code,
            effective_at=holdings_effective_date,
            holding_adjustments=holding_adjustment)

        # Pretty print our response from LUSID
        #prettyprint.set_holdings_response(
        #    set_holdings_response,
        #    analyst_scope_code,
        #    transaction_portfolio_code)
        end = time.time()

        print('Tran portfolio: ' + str(end - start))
        ##################################
        # Allow our analysts to trade across their tradeable instrument universe
        # and add transactions to their transaction portfolio
        # Import transactions from DJII transactions. We have 30 instruments with hidden strategies to investigate

        djii_transactions = cls.load_transactions_from_file('DJIItransactions.csv')

        end = time.time()

        print('Tran load from file: ' + str(end - start))

        # create the strategy property. Although strategies are currently set to none for all transactions,
        # this property is created to allow trades to be identified and categorised at a later date
        # Create a request to define our strategy property
        property_request = models.CreatePropertyDefinitionRequest(
            domain='Trade',
            scope=analyst_scope_code,
            code='strategy',
            value_required=False,
            display_name='strategy',
            data_type_id=models.ResourceId(
                scope='default',
                code='string')
            )

        # Call LUSID to create our new property
        property_response = cls.client.create_property_definition(definition=property_request)

        # Grab the key off the response to use when referencing this property in other LUSID calls
        strategy_property_key = property_response.key

        # Pretty print our strategy property key
        # prettyprint.heading('Strategy Property Key: ', strategy_property_key)

        # Now we wish to upsert our trades into LUSID so we can start our analysis

        # Initialise a list to hold our transactions
        batch_transaction_requests = []

        # Iterate over the transactions for each portfolio
        for transaction_id, transaction in djii_transactions.items():

            if 'Cash' in transaction['instrument_name']:
                identifier_key = 'Instrument/default/Currency'
            else:
                identifier_key = 'Instrument/default/Figi'

            batch_transaction_requests.append(
                models.TransactionRequest(
                    transaction_id=transaction_id,
                    type=transaction['type'],
                    instrument_identifiers={
                        identifier_key: transaction['instrument_uid']},
                    transaction_date=transaction['transaction_date'],
                    settlement_date=transaction['settlement_date'],
                    units=transaction['units'],
                    transaction_price=models.TransactionPrice(
                        price=transaction['transaction_price'],
                        type='Price'),
                    total_consideration=models.CurrencyAndAmount(
                        amount=transaction['total_cost'],
                        currency=transaction['transaction_currency']),
                    source='Client',
                    transaction_currency=transaction['transaction_currency'],
                    properties={
                        strategy_property_key: models.PropertyValue(
                            label_value=transaction['strategy']),
                        'Trade/default/TradeToPortfolioRate': models.PropertyValue(
                            metric_value=models.MetricValue(1.0))
                    }
                ))
        end = time.time()
        print('batch tran create: ' + str(end - start))

        # Call LUSID to upsert our transactions
        transaction_response = cls.client.upsert_transactions(
            scope=analyst_scope_code,
            code=transaction_portfolio_code,
            transactions=batch_transaction_requests)

        # Pretty print the response from LUSID
        # prettyprint.transactions_response(
        #    transaction_response,
        #    analyst_scope_code,
        #    transaction_portfolio_code)
        end = time.time()
        print('and then upsert: ' + str(end - start))

        # We now need to add in closing prices for our instruments over the last two years
        # Import our instrument prices from a CSV file

        instrument_close_prices = pd.read_csv('data/company_closing_prices_no_divis.csv')

        end = time.time()
        print('close prices load: ' + str(end - start))

        # Pretty print our pricing
        # print(instrument_prices.head(n=10))

        # We can now store this information in LUSID in an analytics store.
        # Note we need a separate store for each closing date
        # Set our analytics effective dates

        # analytics_effective_date = datetime.now(pytz.UTC) - timedelta(days=3)
        # today = datetime.now(pytz.UTC)
        analytics_store_dates = []      # we will need to populate this from the closing prices

        # Create prices via instrument, analytic
        instrument_analytics = {}

        for row in instrument_close_prices.iterrows():
            # group closing prices by date for analytics store

            instrument = row[1]

            if 'Cash' in instrument['Name']:
                continue

            # Get our Lusid Instrument Id

            luid = cls.instrument_universe[instrument['Name']]['LUID']
            # check the date to see if anything stands against it yet. If it's new, add a list item (for a new store)
            if instrument['Date'] not in analytics_store_dates:
                analytics_store_dates.append(instrument['Date'])
                instrument_analytics[instrument['Date']] = {}

            # add price/instrument to existing store
            instrument_analytics[instrument['Date']][instrument['Name']] = models.InstrumentAnalytic(
                instrument_uid=luid,
                value=instrument['AdjClose'])
        end = time.time()
        print('close prices by date: ' + str(end - start))

        time2 = time3 = time4 = time5 = 0
        for date, date_item in instrument_analytics.items():
            # Create analytics store request - one required for each date there are prices
            point1 = time.time()
            format_date =parser.parse(date).replace(tzinfo=pytz.utc)
            analytics_store_request = models.CreateAnalyticStoreRequest(scope=analyst_scope_code,
                                                                        date_property=format_date)
            point2 = time.time()
            time2 += (point2 - point1)
            # Call LUSID to create our analytics store
            cls.client.create_analytic_store(request=analytics_store_request)
            point3 = time.time()
            time3 += (point3 - point2)
            days_closes = []
            for inst_name, instrument_analytic_item in date_item.items():
                days_closes.append(instrument_analytic_item)
            point4 = time.time()
            time4 += (point4 - point3)
            # Call LUSID to set up our newly created analytics store with our prices
            cls.client.set_analytics(scope=analyst_scope_code,
                                     year=format_date.year,
                                     month=format_date.month,
                                     day=format_date.day,
                                     data=days_closes)
            point5 = time.time()
            time5 += (point5 - point4)
        end = time.time()
        print('create analytic stores: ' + str(end - start))
        print('create store request: ' + str(time2))
        print('create store: ' + str(time3))
        print('append day closes : ' + str(time4))
        print('set analytics: ' + str(time5))
        print('Analytics Set')

        # we can now value the portfolio assuming different access levels and look at how the
        # stock have been traded.
        # set today to be the last entered close
        today = datetime(2018, 12, 31, tzinfo=pytz.utc)
        # Create our aggregation request
        aggregation_request = models.AggregationRequest(
            recipe_id=models.ResourceId(
            scope=analyst_scope_code,
            code='default'),
            effective_at=today,
            metrics=[
                models.AggregateSpec(
                    key='Holding/default/SubHoldingKey',
                    op='value'),
                models.AggregateSpec(
                    key='Holding/default/Units',
                    op='sum'),
                models.AggregateSpec(
                    key='Holding/default/Cost',
                    op='sum'),
                models.AggregateSpec(
                    key='Holding/default/PV',
                    op='sum'),
                models.AggregateSpec(
                    key='Holding/default/Price',
                    op='sum')
            ],
            group_by=[
                'Holding/default/SubHoldingKey'
            ])

        # Call LUSID to aggregate across all of our portfolios
        aggregated_portfolio = cls.client.get_aggregation_by_portfolio(scope=analyst_scope_code,
                                                                   code=transaction_portfolio_code,
                                                                   request=aggregation_request)
        end = time.time()
        print('get aggregation: ' + str(end - start))
        # prettyprint.aggregation_response_paper(aggregated_portfolio)
        total_cost = 0
        total_pv = 0

        # for result in aggregated_portfolio.data:
        #     if 'Currency' in result['Holding/default/SubHoldingKey']:
        #         continue
        #     sign = result['Sum(Holding/default/Units)'] / abs(result['Sum(Holding/default/Units)'])
        #     print('Instrument :' + result['Holding/default/SubHoldingKey'])
        #     print('Units :' + str(round(result['Sum(Holding/default/Units)'], 0)))
        #     print('Current Price :' + '£'  + str(
        #         round(result['Sum(Holding/default/Price)'], 2)))
        #     print(
        #           'Present Value :' + '£' + str(round(result['Sum(Holding/default/PV)'], 2)))
        #     print('Cost :' + '£' + str(round(result['Sum(Holding/default/Cost)'], 2)))
        #     print('Return :' + str(round(((result['Sum(Holding/default/PV)'] - result[
        #         'Sum(Holding/default/Cost)']) / result['Sum(Holding/default/Cost)']) * 100 * sign, 4)) + '%' + '\n')
        #
        #     total_cost += result['Sum(Holding/default/Cost)']
        #     total_pv += result['Sum(Holding/default/PV)']

        # print('TOTAL RETURN: ')
        # print((round(((total_pv - total_cost) / total_cost) * 100, 4)))
        # # create some test dates
        # dec4th17 = datetime(2017, 12, 4, tzinfo=pytz.utc)
        # dec5th17 = datetime(2017, 12, 5, tzinfo=pytz.utc)
        # dec6th17 = datetime(2017, 12, 6, tzinfo=pytz.utc)

        # # test whats in LUSID by holdings:
        # dec4th17holdings = cls.client.get_holdings(analyst_scope_code, transaction_portfolio_code, False, dec4th17)
        # dec5th17holdings = cls.client.get_holdings(analyst_scope_code, transaction_portfolio_code, False, dec5th17)
        # dec6th17holdings = cls.client.get_holdings(analyst_scope_code, transaction_portfolio_code, False, dec6th17)

        # get realised p&l during the life of the portfolio

        query_params = models.TransactionQueryParameters(
            start_date=cls.effective_date,
            end_date=today,
            query_mode='TradeDate',
            show_cancelled_transactions=None)

        transactions_response = cls.client.build_transactions(
            scope=analyst_scope_code,
            code=transaction_portfolio_code,
            as_at=None,
            sort_by=None,
            start=None,
            limit=None,
            instrument_property_keys=['Instrument/default/Name'],
            filter=None,
            parameters=query_params
        )
        end = time.time()
        print('build output trans: ' + str(end - start))

        # Transactions response is a list of the trades we created
        # In each output transaction, there is a realised gain loss attribute.
        # These can be combined with position p&l to create an overall p&l.
        output_store = {}

        for output_transaction in transactions_response.values:
            if len(output_transaction.realised_gain_loss) > 0:      # not a ccy
                if output_transaction.instrument_uid not in output_store:
                    output_store[output_transaction.instrument_uid] = {}
                realised_gain_loss = 0
                for item in output_transaction.realised_gain_loss:
                    realised_gain_loss += item.realised_total.amount
                output_store[output_transaction.instrument_uid][output_transaction.transaction_date] = realised_gain_loss

        # output_store now holds all the transactions by LUID.
        # we can sum to the pv as shown earlier.

        for instrument_name, instrument_identifiers in cls.instrument_universe.items():
            # get the trades from output_store, the end pv from aggregated_portfolio.data
            position_pl = 0
            trade_pl = 0
            if instrument_identifiers['LUID'] in output_store:
                trade_pl = sum(output_store[instrument_identifiers['LUID']].values())
                print('trade p&l: ' + str(trade_pl))
            for item in aggregated_portfolio.data:
                if item['Holding/default/SubHoldingKey'] == 'LusidInstrumentId=' + instrument_identifiers['LUID'] + '/USD':
                    position_pl = item['Sum(Holding/default/PV)'] - item['Sum(Holding/default/Cost)']
            if position_pl != 0:
                print('pos p&l: ' + str(position_pl))

            print('Total trade and position p&l for ' + instrument_name + ': ' + str(trade_pl + position_pl))

    @classmethod
    def tearDownClass(cls):
        for name, item in cls.instrument_universe.items():
            response = cls.client.delete_instrument(InstrumentLoader.FIGI_SCHEME, item['Figi'])
    @classmethod
    def load_instruments_from_file(cls):
        inst_list = pd.read_csv('data/DOW Figis.csv')
        # Look at the first 10 instruments
        # inst_list.head(n=10)
        return inst_list
    @classmethod
    def load_transactions_from_file(cls, csv_file):
        csv_transactions = cls.import_csv_file(csv_file)
        transactions = {}

        for index, transaction in csv_transactions.iterrows():
            transactions[transaction['transaction_id']] = {
                'type': transaction['transaction_type'],
                'portfolio': transaction['portfolio_name'],
                'instrument_name': transaction['instrument_name'],
                'instrument_uid': cls.instrument_universe[transaction['instrument_name']]['Figi'],
                'transaction_date': parser.parse(transaction['transaction_date']).replace(tzinfo=pytz.utc),
                'settlement_date': (parser.parse(transaction['transaction_date']) + timedelta(days=2)).replace(tzinfo=pytz.utc),
                'units': transaction['transaction_units'],
                'transaction_price': transaction['transaction_price'],
                'transaction_currency': transaction['transaction_currency'],
                'total_cost': transaction['transaction_cost'],
                'strategy': transaction['transaction_strategy']}
            # print(index)
        return transactions

    @classmethod
    def import_csv_file(cls, csv_file):
        """
        This function is used to import data form our csv files
        """
        data = pd.read_csv('./data/{}'.format(csv_file))
        return data

    @classmethod
    def import_json_file(cls, json_file):
        """
        This function is used to import data form our json files
        """
        with open(os.path.join('./data/', json_file), "r") as openfile:
            data = json.load(openfile)
        return data

    @classmethod
    def upsert_intruments(cls, inst_list):
        # Initialise our batch upsert request
        batch_upsert_request = {}
        # Iterate over our instrument universe
        for row in inst_list.iterrows():
            # Collect our instrument note that row[0] gives you the index
            instrument = row[1]
            instrument_ticker = models.InstrumentProperty(cls.TICKER_PROPERTY_KEY,  models.PropertyValue(instrument['instrument_name']))

            # Add the instrument to our batch request using the FIGI as the main unique identifier
            batch_upsert_request[instrument['instrument_name']] = models.InstrumentDefinition(
                name=instrument['instrument_name'],
                identifiers={cls.FIGI_SCHEME: instrument['figi']},
                properties=[instrument_ticker])


        # Call LUSID to upsert our batch
        instrument_response = cls.client.upsert_instruments(requests=batch_upsert_request)

        # Pretty print the response from LUSID
        # prettyprint.instrument_response(instrument_response, identifier='Figi')
        identifier = 'Figi'
        for instrument_name, instrument in instrument_response.values.items():

            # Build a global dictionary of name-figi pairs for use throughout the use-case
            cls.instrument_universe[instrument_name]={}
            cls.instrument_universe[instrument_name]['Figi'] = instrument.identifiers['Figi']
            cls.instrument_universe[instrument_name]['LUID'] = instrument.lusid_instrument_id
            # print results
            print('Instrument Successfully Upserted: ' + instrument_name)
            print(instrument.identifiers[identifier])
            print('LUSID Instrument ID: ' + instrument.lusid_instrument_id)
            print('\n')

        print(len(instrument_response.values), ' instruments upserted successfully')
        print(len(instrument_response.failed), ' instrument upsert failures')

    def test_run_aggregation_with_buy(self):

        print("here")

    def run_aggregation(self, tran_requests):

        print("here")


if __name__ == '__main__':
    unittest.main()
