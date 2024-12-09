import requests_mock
import pytest
from aioresponses import aioresponses


def test_get_accounts(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/accounts"
        m.get(url, json={}, status_code=200)
        client.get_accounts()

def test_get_subaccounts(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/sub/user"
        m.get(url, json={}, status_code=200)
        client.get_subaccounts()

def test_get_subaccounts_v2(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v2/sub/user"
        m.get(url, json={}, status_code=200)
        client.get_subaccounts_v2()

def test_margin_get_account_detail(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/margin/account"
        m.get(url, json={}, status_code=200)
        client.margin_get_account_detail()

def test_futures_get_account_detail(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/account-overview"
        m.get(url, json={}, status_code=200)
        client.futures_get_account_detail()

def test_get_subaccount_balance(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/sub-accounts/sub_user_id"
        m.get(url, json={}, status_code=200)
        client.get_subaccount_balance("sub_user_id", "include_base_ammount")
        url = m.last_request._request.url
        assert "include_base_ammount" in url

def test_get_all_subaccounts_balance(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/sub-accounts"
        m.get(url, json={}, status_code=200)
        client.get_all_subaccounts_balance()

def test_futures_get_all_subaccounts_balance(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/account-overview-all"
        m.get(url, json={}, status_code=200)
        client.futures_get_all_subaccounts_balance()

def test_get_subaccount_api_list(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/sub/api-key"
        m.get(url, json={}, status_code=200)
        client.get_subaccount_api_list("sub_name")
        url = m.last_request._request.url
        assert "sub_name" in url

def test_create_subaccount_api(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/sub/api-key"
        m.post(url, json={}, status_code=200)
        client.create_subaccount_api("sub_name", "passphrase", "remark")
        body = m.last_request._request.body
        assert "sub_name" in body
        assert "passphrase" in body
        assert "remark" in body

# todo: update test for order creation/modification
# def test_modify_subaccount_api(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/sub/api-key/update"
#         m.post(url, json={}, status_code=200)
#         client.modify_subaccount_api("sub_name", "api_key", "passphrase")
#         body = m.last_request._request.body
#         assert "sub_name" in body
#         assert "api_key" in body
#         assert "passphrase" in body
# 
def test_delete_subaccount_api(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/sub/api-key"
        m.delete(url, json={}, status_code=200)
        client.delete_subaccount_api("api_key", "passphrase", "sub_name")
        url = m.last_request._request.url
        assert "api_key" in url
        url = m.last_request._request.url
        assert "passphrase" in url
        url = m.last_request._request.url
        assert "sub_name" in url

def test_get_account(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/accounts/account_id"
        m.get(url, json={}, status_code=200)
        client.get_account("account_id")

def test_create_account(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/accounts"
        m.post(url, json={}, status_code=200)
        client.create_account("account_type", "currency")
        body = m.last_request._request.body
        assert "account_type" in body
        assert "currency" in body

def test_get_account_activity(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/accounts/ledgers"
        m.get(url, json={}, status_code=200)
        client.get_account_activity()

def test_futures_get_account_activity(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/transaction-history"
        m.get(url, json={}, status_code=200)
        client.futures_get_account_activity()

def test_get_transferable_balance(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/accounts/transferable"
        m.get(url, json={}, status_code=200)
        client.get_transferable_balance("currency", "type")
        url = m.last_request._request.url
        assert "currency" in url
        url = m.last_request._request.url
        assert "type" in url

def test_create_universal_transfer(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/accounts/universal-transfer"
        m.post(url, json={}, status_code=200)
        client.create_universal_transfer("client_oid", "amount", "from_account_type", "type", "to_account_type")
        body = m.last_request._request.body
        assert "client_oid" in body
        assert "amount" in body
        assert "from_account_type" in body
        assert "type" in body
        assert "to_account_type" in body

def test_create_transfer_in(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/accounts/transfer-in"
        m.post(url, json={}, status_code=200)
        client.create_transfer_in("amount", "currency", "pay_account_type")
        body = m.last_request._request.body
        assert "amount" in body
        assert "currency" in body
        assert "pay_account_type" in body

def test_get_transfer_list(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/transfer-list"
        m.get(url, json={}, status_code=200)
        client.get_transfer_list()

def test_get_deposits(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/deposits"
        m.get(url, json={}, status_code=200)
        client.get_deposits()

def test_get_deposit_history(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hist-deposits"
        m.get(url, json={}, status_code=200)
        client.get_deposit_history()

def test_get_user_type(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/accounts/opened"
        m.get(url, json={}, status_code=200)
        client.get_user_type()

def test_get_withdrawals(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/withdrawals"
        m.get(url, json={}, status_code=200)
        client.get_withdrawals()

def test_get_historical_withdrawals(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hist-withdrawals"
        m.get(url, json={}, status_code=200)
        client.get_historical_withdrawals()

def test_get_withdrawal_quotas(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/withdrawals/quotas"
        m.get(url, json={}, status_code=200)
        client.get_withdrawal_quotas("currency")
        url = m.last_request._request.url
        assert "currency" in url

def test_cancel_withdrawal(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/withdrawals/withdrawal_id"
        m.delete(url, json={}, status_code=200)
        client.cancel_withdrawal("withdrawal_id")

def test_get_base_fee(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/base-fee"
        m.get(url, json={}, status_code=200)
        client.get_base_fee()

def test_get_trading_pair_fee(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/trade-fees"
        m.get(url, json={}, status_code=200)
        client.get_trading_pair_fee("symbols")
        url = m.last_request._request.url
        assert "symbols" in url

def test_futures_get_trading_pair_fee(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/trade-fees"
        m.get(url, json={}, status_code=200)
        client.futures_get_trading_pair_fee("symbol")
        url = m.last_request._request.url
        assert "symbol" in url

# todo: update test for order creation/modification
# def test_create_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/orders"
#         m.post(url, json={}, status_code=200)
#         client.create_order("symbol", "type", "side")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "type" in body
#         assert "side" in body
# 
# todo: update test for order creation/modification
# def test_create_test_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/orders/test"
#         m.post(url, json={}, status_code=200)
#         client.create_test_order("symbol", "type", "side")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "type" in body
#         assert "side" in body
# 
# todo: update test for order creation/modification
# def test_create_orders(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/orders/multi"
#         m.post(url, json={}, status_code=200)
#         client.create_orders("symbol", "order_list")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "order_list" in body
# 
def test_cancel_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/orders/order_id"
        m.delete(url, json={}, status_code=200)
        client.cancel_order("order_id")

def test_cancel_order_by_client_oid(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/order/client-order/client_oid"
        m.delete(url, json={}, status_code=200)
        client.cancel_order_by_client_oid("client_oid")

def test_cancel_all_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/orders"
        m.delete(url, json={}, status_code=200)
        client.cancel_all_orders()

def test_get_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/orders"
        m.get(url, json={}, status_code=200)
        client.get_orders()

def test_get_recent_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/limit/orders"
        m.get(url, json={}, status_code=200)
        client.get_recent_orders()

def test_get_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/orders/order_id"
        m.get(url, json={}, status_code=200)
        client.get_order("order_id")

def test_get_order_by_client_oid(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/order/client-order/client_oid"
        m.get(url, json={}, status_code=200)
        client.get_order_by_client_oid("client_oid")

# todo: update test for order creation/modification
# def test_hf_create_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/hf/orders"
#         m.post(url, json={}, status_code=200)
#         client.hf_create_order("symbol", "type", "side")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "type" in body
#         assert "side" in body
# 
# todo: update test for order creation/modification
# def test_hf_create_test_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/hf/orders/test"
#         m.post(url, json={}, status_code=200)
#         client.hf_create_test_order("symbol", "type", "side")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "type" in body
#         assert "side" in body
# 
# todo: update test for order creation/modification
# def test_sync_hf_create_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/hf/orders/sync"
#         m.post(url, json={}, status_code=200)
#         client.sync_hf_create_order("symbol", "type", "side")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "type" in body
#         assert "side" in body
# 
# todo: update test for order creation/modification
# def test_hf_create_orders(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/hf/orders/multi"
#         m.post(url, json={}, status_code=200)
#         client.hf_create_orders("order_list")
#         body = m.last_request._request.body
#         assert "order_list" in body
# 
# todo: update test for order creation/modification
# def test_sync_hf_create_orders(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/hf/orders/multi/sync"
#         m.post(url, json={}, status_code=200)
#         client.sync_hf_create_orders("order_list")
#         body = m.last_request._request.body
#         assert "order_list" in body
# 
# todo: update test for order creation/modification
# def test_hf_modify_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/hf/orders/alter"
#         m.post(url, json={}, status_code=200)
#         client.hf_modify_order("symbol")
#         body = m.last_request._request.body
#         assert "symbol" in body
# 
def test_hf_cancel_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/order_id"
        m.delete(url, json={}, status_code=200)
        client.hf_cancel_order("order_id", "symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_sync_hf_cancel_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/sync/order_id"
        m.delete(url, json={}, status_code=200)
        client.sync_hf_cancel_order("order_id", "symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_hf_cancel_specified_quantity_of_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/cancel/order_id"
        m.delete(url, json={}, status_code=200)
        client.hf_cancel_specified_quantity_of_order("order_id", "symbol", "cancel_size")
        url = m.last_request._request.url
        assert "symbol" in url
        url = m.last_request._request.url
        assert "cancel_size" in url

def test_hf_cancel_orders_by_symbol(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders"
        m.delete(url, json={}, status_code=200)
        client.hf_cancel_orders_by_symbol("symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_hf_cancel_all_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/cancelAll"
        m.delete(url, json={}, status_code=200)
        client.hf_cancel_all_orders()

def test_hf_get_active_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/active"
        m.get(url, json={}, status_code=200)
        client.hf_get_active_orders("symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_hf_get_symbol_with_active_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/active/symbols"
        m.get(url, json={}, status_code=200)
        client.hf_get_symbol_with_active_orders()

def test_hf_get_completed_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/done"
        m.get(url, json={}, status_code=200)
        client.hf_get_completed_orders("symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_hf_get_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/order_id"
        m.get(url, json={}, status_code=200)
        client.hf_get_order("order_id", "symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_hf_auto_cancel_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/dead-cancel-all"
        m.post(url, json={}, status_code=200)
        client.hf_auto_cancel_order("timeout")
        body = m.last_request._request.body
        assert "timeout" in body

def test_hf_get_auto_cancel_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/orders/dead-cancel-all"
        m.get(url, json={}, status_code=200)
        client.hf_get_auto_cancel_order()

# todo: update test for order creation/modification
# def test_create_stop_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/stop-order"
#         m.post(url, json={}, status_code=200)
#         client.create_stop_order("symbol", "type", "side", "stop_price")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "type" in body
#         assert "side" in body
#         assert "stop_price" in body
# 
def test_cancel_stop_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/stop-order/order_id"
        m.delete(url, json={}, status_code=200)
        client.cancel_stop_order("order_id")

def test_cancel_stop_order_by_client_oid(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/stop-order/cancelOrderByClientOid"
        m.delete(url, json={}, status_code=200)
        client.cancel_stop_order_by_client_oid("client_oid")
        url = m.last_request._request.url
        assert "client_oid" in url

def test_cancel_all_stop_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/stop-order/cancel"
        m.delete(url, json={}, status_code=200)
        client.cancel_all_stop_orders()

def test_get_stop_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/stop-order"
        m.get(url, json={}, status_code=200)
        client.get_stop_orders()

def test_get_stop_order(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/stop-order/order_id"
        m.get(url, json={}, status_code=200)
        client.get_stop_order("order_id")

def test_get_stop_order_by_client_oid(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/stop-order/queryOrderByClientOid"
        m.get(url, json={}, status_code=200)
        client.get_stop_order_by_client_oid("client_oid")
        url = m.last_request._request.url
        assert "client_oid" in url

# todo: update test for order creation/modification
# def test_oco_create_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v3/oco/order"
#         m.post(url, json={}, status_code=200)
#         client.oco_create_order("symbol", "side", "size", "price", "stop_price", "limit_price")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "side" in body
#         assert "size" in body
#         assert "price" in body
#         assert "stop_price" in body
#         assert "limit_price" in body
# 
def test_oco_cancel_all_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v3/oco/orders"
        m.delete(url, json={}, status_code=200)
        client.oco_cancel_all_orders()

def test_oco_get_orders(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v3/oco/orders"
        m.get(url, json={}, status_code=200)
        client.oco_get_orders()

# todo: update test for order creation/modification
# def test_margin_create_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/margin/order"
#         m.post(url, json={}, status_code=200)
#         client.margin_create_order("symbol", "type", "side")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "type" in body
#         assert "side" in body
# 
# todo: update test for order creation/modification
# def test_margin_create_test_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api.kucoin.com/api/v1/margin/order/test"
#         m.post(url, json={}, status_code=200)
#         client.margin_create_test_order("symbol", "type", "side")
#         body = m.last_request._request.body
#         assert "symbol" in body
#         assert "type" in body
#         assert "side" in body
# 
# todo: update test for order creation/modification
# def test_futures_create_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api-futures.kucoin.com/api/v1/orders"
#         m.post(url, json={}, status_code=200)
#         client.futures_create_order("symbol")
#         body = m.last_request._request.body
#         assert "symbol" in body
# 
# todo: update test for order creation/modification
# def test_futures_create_test_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api-futures.kucoin.com/api/v1/orders/test"
#         m.post(url, json={}, status_code=200)
#         client.futures_create_test_order("symbol")
#         body = m.last_request._request.body
#         assert "symbol" in body
# 
# todo: update test for order creation/modification
# def test_futures_create_stop_order(client):
#     with requests_mock.mock() as m:
#         url = "https://api-futures.kucoin.com/api/v1/st-orders"
#         m.post(url, json={}, status_code=200)
#         client.futures_create_stop_order("symbol")
#         body = m.last_request._request.body
#         assert "symbol" in body
# 
# todo: update test for order creation/modification
# def test_futures_create_orders(client):
#     with requests_mock.mock() as m:
#         url = "https://api-futures.kucoin.com/api/v1/orders/multi"
#         m.post(url, json={}, status_code=200)
#         client.futures_create_orders("orders_data")
#         body = m.last_request._request.body
#         assert "orders_data" in body
# 
def test_futures_cancel_order(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/orders/order_id"
        m.delete(url, json={}, status_code=200)
        client.futures_cancel_order("order_id")

# todo: update test for order creation/modification
# def test_futures_cancel_orders(client):
#     with requests_mock.mock() as m:
#         url = "https://api-futures.kucoin.com/api/v1/orders/multi-cancel"
#         m.delete(url, json={}, status_code=200)
#         client.futures_cancel_orders()
# 
def test_futures_cancel_all_orders(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/orders"
        m.delete(url, json={}, status_code=200)
        client.futures_cancel_all_orders()

def test_futures_cancel_all_stop_orders(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/stopOrders"
        m.delete(url, json={}, status_code=200)
        client.futures_cancel_all_stop_orders()

def test_futures_get_orders(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/orders"
        m.get(url, json={}, status_code=200)
        client.futures_get_orders()

def test_futures_get_stop_orders(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/stopOrders"
        m.get(url, json={}, status_code=200)
        client.futures_get_stop_orders()

def test_futures_get_recent_orders(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/recentDoneOrders"
        m.get(url, json={}, status_code=200)
        client.futures_get_recent_orders()

def test_futures_get_order(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/orders/order_id"
        m.get(url, json={}, status_code=200)
        client.futures_get_order("order_id")

def test_futures_get_order_by_client_oid(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/orders/byClientOid"
        m.get(url, json={}, status_code=200)
        client.futures_get_order_by_client_oid("client_oid")
        url = m.last_request._request.url
        assert "client_oid" in url

def test_get_fills(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/fills"
        m.get(url, json={}, status_code=200)
        client.get_fills("trade_type")
        url = m.last_request._request.url
        assert "trade_type" in url

def test_get_recent_fills(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/limit/fills"
        m.get(url, json={}, status_code=200)
        client.get_recent_fills()

def test_hf_get_fills(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/hf/fills"
        m.get(url, json={}, status_code=200)
        client.hf_get_fills("symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_futures_get_fills(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/fills"
        m.get(url, json={}, status_code=200)
        client.futures_get_fills()

def test_futures_get_recent_fills(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/recentFills"
        m.get(url, json={}, status_code=200)
        client.futures_get_recent_fills()

def test_futures_get_active_order_value(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/openOrderStatistics"
        m.get(url, json={}, status_code=200)
        client.futures_get_active_order_value("symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_margin_get_leverage_token_info(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v3/etf/info"
        m.get(url, json={}, status_code=200)
        client.margin_get_leverage_token_info()

def test_margin_get_config(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/margin/config"
        m.get(url, json={}, status_code=200)
        client.margin_get_config()

def test_margin_get_isolated_synbols_config(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/isolated/symbols"
        m.get(url, json={}, status_code=200)
        client.margin_get_isolated_synbols_config()

def test_margin_get_isolated_account_info(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/isolated/accounts"
        m.get(url, json={}, status_code=200)
        client.margin_get_isolated_account_info()

def test_margin_get_single_isolated_account_info(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v1/isolated/account/symbol"
        m.get(url, json={}, status_code=200)
        client.margin_get_single_isolated_account_info("symbol")

def test_margin_lending_subscribtion(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v3/purchase"
        m.post(url, json={}, status_code=200)
        client.margin_lending_subscribtion("currency", "size", "interest_rate")
        body = m.last_request._request.body
        assert "currency" in body
        assert "size" in body
        assert "interest_rate" in body

def test_margin_lending_redemption(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v3/redeem"
        m.post(url, json={}, status_code=200)
        client.margin_lending_redemption("currency", "size", "purchase_order_no")
        body = m.last_request._request.body
        assert "currency" in body
        assert "size" in body
        assert "purchase_order_no" in body

def test_futures_get_position(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/position"
        m.get(url, json={}, status_code=200)
        client.futures_get_position("symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_futures_get_positions(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/positions"
        m.get(url, json={}, status_code=200)
        client.futures_get_positions()

def test_futures_get_positions_history(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/history-positions"
        m.get(url, json={}, status_code=200)
        client.futures_get_positions_history()

def test_futures_get_max_withdraw_margin(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/margin/maxWithdrawMargin"
        m.get(url, json={}, status_code=200)
        client.futures_get_max_withdraw_margin("symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_futures_withdraw_margin(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/margin/withdrawMargin"
        m.post(url, json={}, status_code=200)
        client.futures_withdraw_margin("symbol", "amount")
        body = m.last_request._request.body
        assert "symbol" in body
        assert "amount" in body

def test_futures_get_private_funding_history(client):
    with requests_mock.mock() as m:
        url = "https://api-futures.kucoin.com/api/v1/funding-history"
        m.get(url, json={}, status_code=200)
        client.futures_get_private_funding_history("symbol")
        url = m.last_request._request.url
        assert "symbol" in url

def test_get_user_info(client):
    with requests_mock.mock() as m:
        url = "https://api.kucoin.com/api/v2/user-info"
        m.get(url, json={}, status_code=200)
        client.get_user_info()
