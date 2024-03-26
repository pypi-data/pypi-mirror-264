# coding=utf-8
"""
File containing test configurations for the SwgohComlink class methods
"""
from swgoh_comlink import SwgohComlink


def test_get_enums(mock_response):
    """
    Test that game enums can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    en = comlink.get_enums()
    assert "CombatType" in en.keys()


def test_get_game_data(mock_response):
    """
    Test that game data can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    game_data = comlink.get_game_data(
        version="0.33.91:vNj39OjkQmazUnkwobp6qg",
        include_pve_units=False,
        request_segment=4
    )
    assert "units" in game_data.keys()


def test_get_guild_by_criteria(mock_response):
    """
    Test that guild data can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    p = comlink.get_guilds_by_criteria({"minGuildGalacticPower": 490000000})
    assert "guild" in p.keys()


def test_get_guild_by_name(mock_response):
    """
    Test that guild data can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    p = comlink.get_guilds_by_name("dead")
    assert "guild" in p.keys()


def test_get_localization_bundle(mock_response):
    """
    Test that localization data can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    game_data = comlink.get_localization(id='sFyXGlFHRCuHEfs0ba3afQ')
    assert "localizationBundle" in game_data.keys()


def test_get_metadata(mock_response):
    """
    Test that game metadata can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    md = comlink.get_game_metadata()
    assert "serverVersion" in md.keys()


def test_get_player(mock_response, allycode):
    """
    Test that player data can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    p = comlink.get_player(allycode=allycode)
    assert "name" in p.keys()


def test_get_player_arena(mock_response, allycode):
    """
    Test that player data can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    p = comlink.get_player_arena(allycode=allycode)
    assert "name" in p.keys()


def test_get_player_arena_details_only(mock_response, allycode):
    """
    Test that player data can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    p = comlink.get_player_arena(allycode=allycode, player_details_only=True)
    assert "name" in p.keys()


def test_get_player_arena_details_only_alias(mock_response, allycode):
    """
    Test that player data can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    p = comlink.get_player_arena(allycode=allycode, playerDetailsOnly=True)
    assert "name" in p.keys()


def test_get_unit_stats(mock_response, allycode):
    """
    Test that player data can be retrieved from game server correctly
    """
    comlink = SwgohComlink(url='http://192.168.1.167:3200', stats_url='http://192.168.1.167:3223')
    p = comlink.get_player(allycode=allycode)
    unit_stats = comlink.get_unit_stats(
        p["rosterUnit"][0], flags=["calcGP", "gameStyle"]
    )
    assert "gp" in unit_stats[0]["stats"].keys()
