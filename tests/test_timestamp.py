
def test_spot_timestamp(client):
    ping_response = client.get_timestamp()
    assert ping_response is not None

def test_futures_timestamp(client):
    ping_response = client.futures_get_timestamp()
    assert ping_response is not None