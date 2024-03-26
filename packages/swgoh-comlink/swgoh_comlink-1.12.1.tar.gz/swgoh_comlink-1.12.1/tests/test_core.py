import swgoh_comlink


def test_construct_request_headers(mock_response):
    base = swgoh_comlink.SwgohComlink()
    base.access_key = 'abcxyz'
    base.secret_key = 'zyxdef'
    base.hmac = True
    headers = base.construct_request_headers(
        endpoint="getEvents",
        payload={})
    assert 'X-Date' in headers.keys()
    assert 'Authorization' in headers.keys()


def test_construct_url_base():
    base_url = swgoh_comlink.SwgohComlink.construct_url_base("http", "localhost", 8888)
    assert base_url == "http://localhost:8888"


def test_get_player_payload(allycode):
    player_payload = swgoh_comlink.SwgohComlink.get_player_payload(allycode)
    assert player_payload == {'payload': {'allyCode': str(allycode)}, 'enums': False}
