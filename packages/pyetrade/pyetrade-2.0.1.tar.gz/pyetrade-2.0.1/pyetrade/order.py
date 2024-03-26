"""Order - ETrade Order API

   TODO:
       * Preview equity order change
       * Place equity order change
       * Preview option order
       * Place option order
       * Preview option order change
       * Place option order change

"""

import logging
import xmltodict
import dateutil.parser

from typing import Union
from jxmlease import emit_xml
from requests_oauthlib import OAuth1Session

LOGGER = logging.getLogger(__name__)

# some constants
CALL = "Call"
PUT = "Put"


# price: number
# round_down: bool
# return string
def to_decimal_str(price: float, round_down: bool) -> str:
    spstr = "%.2f" % price  # round to 2-place decimal
    spstrf = float(spstr)  # convert back to float again
    diff = price - spstrf

    if diff != 0:  # have to work hard to round to decimal
        HALF_CENT = 0.005  # e.g. BUY  stop: round   up to decimal

        if round_down:
            HALF_CENT *= -1  # e.g. SELL stop: round down to decimal
        price += HALF_CENT

        if price > 0:
            spstr = "%.2f" % price  # now round to 2-place decimal

    return spstr


# resp_format: xml (default)
# empty_json: either [] or {}, depends on the caller's semantics
def get_request_result(req: OAuth1Session.request, empty_json: dict, resp_format: str = "xml") -> dict:
    LOGGER.debug(req.text)

    if resp_format == "json":
        if req.text.strip() == "":
            # otherwise, when ETrade server return empty string, we got this error:
            # simplejson.errors.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
            req_output = empty_json  # empty json object
        else:
            req_output = req.json()
    else:
        req_output = xmltodict.parse(req.text)

    if 'Error' in req_output.keys():
        raise Exception(f'Etrade API Error - Code: {req_output["Error"]["code"]}, Msg: {req_output["Error"]["message"]}')  # noqa: E501
    else:
        return req_output


# return Etrade internal option symbol: e.g. "PLTR--220218P00023000" ref:_test_option_symbol()
def option_symbol(symbol: str, call_put: str, expiry_date: str, strike_price: float) -> str:
    sym = symbol.strip().upper()
    symstr = sym + ("-" * (6 - len(sym)))

    ed = dateutil.parser.parse(expiry_date)  # dateutil can handle most date formats
    edstr = ed.strftime("%y%m%d")
    assert (len(edstr) == 6)

    sp = "%08d" % (float(strike_price) * 1000)
    assert (len(sp) == 8)

    opt_sym = symstr + edstr + call_put.strip().upper()[0] + sp
    assert (len(opt_sym) == 21)

    return opt_sym


class OrderException(Exception):
    """:description: Exception raised when giving bad args to a method not from Etrade calls

    """

    def __init__(self, explanation=None, params=None) -> None:
        super().__init__()
        self.required = params
        self.args = (explanation, params)

    def __str__(self) -> str:
        return "Missing required parameters"


class ETradeOrder(object):
    """:description: Object to perform Orders

       :param client_key: Client key provided by Etrade
       :type client_key: str, required
       :param client_secret: Client secret provided by Etrade
       :type client_secret: str, required
       :param resource_owner_key: Resource key from :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_key: str, required
       :param resource_owner_secret: Resource secret from
            :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_secret: str, required
       :param dev: Defines Sandbox (True) or Live (False) ETrade, defaults to True
       :type dev: bool, optional
       :param timeout: Timeout value for OAuth, defaults to 30
       :type timeout: int, optional
       :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

    """

    def __init__(
        self,
        client_key,
        client_secret,
        resource_owner_key,
        resource_owner_secret,
        dev=True,
        timeout=30,
    ):
        self.base_url = (
            r"https://apisb.etrade.com/v1/accounts"
            if dev
            else r"https://api.etrade.com/v1/accounts"
        )
        self.dev_environment = dev
        self.timeout = timeout
        self.session = OAuth1Session(
            client_key,
            client_secret,
            resource_owner_key,
            resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def list_orders(self, account_id_key: str, resp_format: str = "json", **kwargs) -> dict:
        """:description: Lists orders for a specific account ID Key

            :param account_id_key: AccountIDKey from :class:`pyetrade.accounts.ETradeAccounts.list_accounts`
            :type  account_id_key: str, required
            :param resp_format: Desired Response format, defaults to xml
            :type  resp_format: str, optional
            :param kwargs: Parameters for api. Refer to EtradeRef for options
            :type  kwargs: ``**kwargs``, optional
            :return: List of orders for an account
            :rtype: ``xml`` or ``json`` based on ``resp_format``
            :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

            :return: List of orders in an account

        """

        api_url = f'{self.base_url}/{account_id_key}/orders'

        if resp_format == "json":
            api_url += ".json"

        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=kwargs, timeout=self.timeout)

        return get_request_result(req, {}, resp_format)

    def find_option_orders(self, account_id_key: str, symbol: str, call_put: str, expiry_date: str, strike_price: float) -> list:  # noqa: E501
        """:description: Lists option orders for a specific account ID Key

            :param account_id_key: AccountIDKey from :class:`pyetrade.accounts.ETradeAccounts.list_accounts`
            :type  account_id_key: str, required
            :param symbol: ticker symbol for options chain
            :type  symbol: str, required
            :param call_put: whether the option is a call or put
            :type  call_put: str, required
            :param expiry_date: desired expiry of option (ex: 12-05-2021)
            :type  expiry_date: str, required
            :param strike_price: strike price of desired option
            :type  strike_price: str, required

            :return: List of matching option orders in an account

        """

        opt_sym = option_symbol(symbol, call_put, expiry_date, strike_price)
        orders = self.list_orders(account_id_key, resp_format="json", status="OPEN")  # this call may return empty

        results = []

        if len(orders) > 0:
            for o in orders["OrdersResponse"]["Order"]:
                product = o["OrderDetail"][0]["Instrument"][0]["Product"]

                if product["securityType"] == "OPTN":
                    symbol = product["productId"]["symbol"]  # e.g. "PLTR--220218P00023000"

                    if symbol == opt_sym:
                        results.append(o)
        return results

    @staticmethod
    def check_order(**kwargs):
        """:description: Check that required params for preview or place order are there and correct

                         (Used internally)
        """

        mandatory = [
            "accountIdKey",
            "symbol",
            "orderAction",
            "clientOrderId",
            "priceType",
            "quantity",
            "orderTerm",
            "marketSession",
        ]

        if not all(param in kwargs for param in mandatory):
            raise OrderException

        if kwargs["priceType"] == "STOP" and "stopPrice" not in kwargs:
            raise OrderException
        if kwargs["priceType"] == "LIMIT" and "limitPrice" not in kwargs:
            raise OrderException
        if (
                kwargs["priceType"] == "STOP_LIMIT"
                and "limitPrice" not in kwargs
                and "stopPrice" not in kwargs
        ):
            raise OrderException

    def build_order_payload(self, order_type: str, **kwargs) -> dict:
        """:description: Builds the POST payload of a preview or place order
                         (Used internally)

           :param order_type: PreviewOrderRequest or PlaceOrderRequest
           :type  order_type: str, required
           :securityType: EQ or OPTN
           :orderAction: for OPTN: BUY_OPEN, SELL_CLOSE
           :callPut: CALL or PUT
           :expiryDate: string, e.g. "2022-02-18"
           :return: Builds Order Payload
           :rtype: ``xml`` or ``json`` based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """
        securityType = kwargs.get("securityType", "EQ")  # EQ by default
        product = {"securityType": securityType, "symbol": kwargs["symbol"]}

        if securityType == "OPTN":
            expiryDate = dateutil.parser.parse(kwargs.pop("expiryDate"))  # dateutil can handle most date formats
            product.update({
                "expiryDay": expiryDate.day,
                "expiryMonth": expiryDate.month,
                "expiryYear": expiryDate.year,
                "callPut": kwargs["callPut"],
                "strikePrice": kwargs["strikePrice"]
            })

        instrument = {
            "Product": product,
            "orderAction": kwargs["orderAction"],
            "quantityType": "QUANTITY",
            "quantity": kwargs["quantity"],
        }

        order = kwargs
        order["Instrument"] = instrument

        def remove_invalid_price_from_kwargs(key: str) -> None:
            if float(kwargs.get(key, 0)) <= 0:
                kwargs.pop(key, 0)

        remove_invalid_price_from_kwargs("stopPrice")
        remove_invalid_price_from_kwargs("limitPrice")

        if "stopPrice" in kwargs:
            stopPrice = float(kwargs["stopPrice"])
            round_down = ("SELL" == kwargs["orderAction"][:4])
            spstr = to_decimal_str(stopPrice, round_down)

            order["stopPrice"] = spstr

        payload = {
            order_type: {
                "orderType": securityType,
                "clientOrderId": kwargs["clientOrderId"],
                "Order": order,
            }
        }

        if "previewId" in kwargs:
            payload[order_type]["PreviewIds"] = {"previewId": kwargs["previewId"]}

        return payload

    def perform_request(self, method, api_url: str, payload: Union[dict, str], resp_format: str = "xml") -> dict:
        """:description: POST or PUT request with json or xml used by preview, place and cancel

           :param method: PUT or POST method
           :type method: session, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, required
           :param api_url: API URL
           :type  api_url: str, required
           :param payload: Payload
           :type  payload: json/dict or str xml, required
           :return: Return request
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """

        LOGGER.debug(api_url)
        LOGGER.debug("payload: %s", payload)

        if resp_format == "json":
            req = method(api_url, json=payload, timeout=self.timeout)
        else:
            headers = {"Content-Type": "application/xml"}
            payload = emit_xml(payload)
            LOGGER.debug("xml payload: %s", payload)
            req = method(api_url, data=payload, headers=headers, timeout=self.timeout)

        return get_request_result(req, {}, resp_format)

    def preview_equity_order(self, **kwargs) -> dict:
        """API is used to submit an order request for preview before placing it

           :param accountIdKey: AccountIDkey retrieved from :class:`list_accounts`
           :type  accountIdKey: str, required
           :param symbol: Market symbol for the security being bought or sold
           :type  symbol: str, required
           :param orderAction: Action that the broker is requested to perform
           :type  orderAction: str, required
           :orderAction values:
               * BUY
               * SELL
               * BUY_TO_COVER
               * SELL_SHORT
           :param previewId: Required only if order was previewed.
                             Numeric preview ID from preview.
                             **Note** - Other parameters much match that of preview
           :type  previewId: long, conditional
           :param clientOrderId: Reference number generated by developer.
                                 Used to ensure duplicate order is not submitted.
                                 Value can be of 20 alphanmeric characters or less
                                 Must be uniquewithin this account.
                                 Does not appear in any API responses.
           :type  clientOrderId: str, required
           :param priceType: Type of pricing specified in equity order
           :type  priceType: str, required
           :priceType values:
               * MARKET
               * LIMIT - Requires `limitPrice`
               * STOP - Requires `stopPrice`
               * STOP_LIMIT - Requires `limitPrice`
               * MARKET_ON_CLOSE
           :param limitPrice: Highest to buy or lowest to sell.
                              Required if `priceType` is `STOP` or `STOP_LIMIT`
           :type  limitPrice: double, conditional
           :param stopPrice: Price to buy or sell if specified in a stop order.
                             Required if `priceType` is  `STOP` or `STOP_LIMIT`
           :type  stopPrice: double, conditional
           :param allOrNone: Specifies if order must be executed all at once.
                             TRUE triggers `allOrNone`, defaults to FALSE
           :type  allOrNone: bool, optional
           :param quantity: Number of shares to buy or sell
           :type  quantity: int, required
           :param reserveOrder: If set to TRUE, publicly displays only a limited
                                number of shares (the reserve quantity), instead
                                of the entire order, to avoid influencing other
                                traders. If TRUE, must also specify the
                                `reserveQuantity`, defaults to FALSE
           :type  reserveOrder: bool, optional
           :param reserveQuantity: Number of shares to be publicly displayed if
                                   this is a reserve order. Required if
                                   `reserveOrder` is TRUE.
           :type reserveQuantity: int, conditional
           :param marketSession: Session to place the equity order
           :type  marketSession: str, required
           :marketSession values:
               * REGULAR
               * EXTENDED
           :param orderTerm: Term for which the order is in effect.
           :type  orderTerm: str, required
           :orderTerm values:
               * GOOD_UNTIL_CANCEL
               * GOOD_FOR_DAY
               * IMMEDIATE_OR_CANCEL (only for `LIMIT` orders)
               * FILL_OR_KILL (only for `LIMIT` orders)
           :param routingDestination: Exchange where the order should be executed.
           :type  routingDestination: str, optional
           :routingDestination values:
               * AUTO (default)
               * ARCA
               * NSDQ
               * NYSE
           :param estimatedCommission: Cost billed to the user to preform requested action
           :type  estimatedCommission: double
           :param estimatedTotalAmount: Cost including commission
           :type  estimatedTotalAmount: double
           :param messageList: Container for messages describing the result of the action
           :type  messageList: dict
           :param msgDesc: Text of the result message, indicating order status, success
                           or failure, additional requirements that must be met before
                           placing the order, etc. Applications typically display this
                           message to the user, which may result in further user action
           :type  msgDesc: str
           :param msgCode: Standard numeric code of the result message. Refer to
                           the Error Messages documentation for examples. May optionally
                           be displayed to the user, but is primarily intended for
                           internal use.
           :type  msgCode: int
           :param orderNum: Numeric ID for this order in the E*TRADE system
           :type  orderNum: int
           :param orderTime: The epoch time the order was submitted.
           :type  orderTime: long
           :param symbolDesc: Text description of the security
           :type  symbolDesc: str
           :param symbol: The market symbol for the underlier
           :type  symbol: str
           :return: Confirmation of the Preview Equity Order
           :rtype: ``xml`` or ``json`` based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """
        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        api_url = f'{self.base_url}/{kwargs["accountIdKey"]}/orders/preview'

        # payload creation
        payload = self.build_order_payload("PreviewOrderRequest", **kwargs)

        return self.perform_request(self.session.post, api_url, payload, "xml")

    def change_preview_equity_order(self, account_id_key: str, order_id: str, **kwargs):
        """:description: Same as :class:`preview_equity_order` with orderId
           :param order_id: order_id to modify, refer :class:`list_orders`
           :type  order_id: str, required
           :param account_id_key: account_id_key retrieved from :class:`list_accounts`
           :type  account_id_key: str, required
           :return: Previews Changed order with orderId for account with account_id_key
           :rtype: dict/json
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """

        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        api_url = f'{self.base_url}/{account_id_key}/orders/{order_id}/change/preview'

        # payload creation
        payload = self.build_order_payload("PreviewOrderRequest", **kwargs)

        return self.perform_request(self.session.put, api_url, payload, "xml")

    def place_option_order(self, **kwargs) -> dict:
        """:description: Places Option Order, only single leg CALL or PUT is supported for now
           :return: Returns confirmation of the equity order
        """
        kwargs["securityType"] = "OPTN"

        return self.place_equity_order(**kwargs)

    def place_equity_order(self, **kwargs) -> dict:
        """:description: Places Equity Order

           :param kwargs: Parameters for api, refer :class:`preview_equity_order`
           :type  kwargs: ``**kwargs``, required
           :return: Returns confirmation of the equity order
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html
        """

        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        if "previewId" not in kwargs:
            LOGGER.debug(
                "No previewId given, previewing before placing order "
                "because of an Etrade bug as of 1/1/2019"
            )
            preview = self.preview_equity_order(**kwargs)
            kwargs["previewId"] = preview["PreviewOrderResponse"]["PreviewIds"]["previewId"]

            LOGGER.debug("Got a successful preview with previewId: %s", kwargs["previewId"])

        api_url = f'{self.base_url}/{kwargs["accountIdKey"]}/orders/place'

        # payload creation
        payload = self.build_order_payload("PlaceOrderRequest", **kwargs)

        return self.perform_request(self.session.post, api_url, payload, "xml")

    def place_changed_option_order(self, **kwargs) -> dict:
        """:description: Places Option Order, only single leg CALL or PUT is supported for now
           :return: Returns confirmation of the equity order
        """
        kwargs["securityType"] = "OPTN"

        return self.place_changed_equity_order(**kwargs)

    def place_changed_equity_order(self, **kwargs) -> dict:
        """:description: Places changes to equity orders
            NOTE: the ETrade server will actually cancel the old orderId, and create a new orderId

           :param kwargs: Parameters for api, refer :class:`change_preview_equity_order`
           :type  kwargs: ``**kwargs``, required
           :return: Returns confirmation similar to :class:`preview_equity_order`
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """

        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        if "previewId" not in kwargs:
            LOGGER.debug(
                "No previewId given, previewing before placing order "
                "because of an Etrade bug as of 1/1/2019"
            )
            preview = self.preview_equity_order(**kwargs)

            if "Error" in preview:
                LOGGER.error(preview)
                raise Exception("Please check your order!")

            kwargs["previewId"] = preview["PreviewOrderResponse"]["PreviewIds"]["previewId"]
            LOGGER.debug("Got a successful preview with previewId: %s", kwargs["previewId"])

        api_url = f'{self.base_url}/{kwargs["accountIdKey"]}/orders/{kwargs["orderId"]}/change/place'

        # payload creation
        payload = self.build_order_payload("PlaceOrderRequest", **kwargs)

        return self.perform_request(self.session.put, api_url, payload, "xml")

    def cancel_order(self, account_id_key: str, order_num: int, resp_format: str = "xml") -> dict:
        """:description: Cancels a specific order for a given account

           :param account_id_key: AccountIDkey retrieved from
                              :class:`pyetrade.accounts.ETradeAccounts.list_accounts`
           :type  account_id_key: str, required
           :param order_num: Numeric id for this order listed in :class:`list_orders`
           :type  order_num: int, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, required
           :return: Confirmation of cancellation
           :rtype: ``dict/json``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html
        """

        api_url = f'{self.base_url}/{account_id_key}/orders/cancel'
        payload = {"CancelOrderRequest": {"orderId": order_num}}

        return self.perform_request(self.session.put, api_url, payload, resp_format)
