# coding=utf-8
"""
Test swgoh_comlink.utils functions
"""
from pathlib import Path
import pytest
import json
from swgoh_comlink import SwgohComlink
from swgoh_comlink.utils import (
    construct_unit_stats_query_string,
    convert_divisions_to_int,
    convert_league_to_int,
    create_localized_unit_name_dictionary,
    get_current_datacron_sets,
    get_current_gac_event,
    # get_gac_brackets,
    get_guild_members,
    get_tw_omicrons,
    human_time,
    load_master_map,
    sanitize_allycode,
    # search_gac_brackets,
    validate_file_path
)

with open("skills.json") as fn:
    _skills: list = json.load(fn)

with open("result_skills.json") as fn:
    _result_skills: list = json.load(fn)

with open("name_key_result.json") as fn:
    _name_key_results: dict = json.load(fn)

with open("eng_us.txt") as fn:
    _eng_us_txt: list = fn.readlines()

_dc_sets: list[dict] = [{'id': 14, 'expirationTimeMs': '1720594800000'},
                        {'id': 13, 'expirationTimeMs': '1715756400000'},
                        {'id': 12, 'expirationTimeMs': '1710918000000'},
                        {'id': 11, 'expirationTimeMs': '1706083200000'},
                        {'id': 10, 'expirationTimeMs': '1701244800000'},
                        {'id': 9, 'expirationTimeMs': '1696402800000'},
                        {'id': 8, 'expirationTimeMs': '1691650800000'},
                        {'id': 7, 'expirationTimeMs': '1686726000000'},
                        {'id': 6, 'expirationTimeMs': '1682146800000'},
                        {'id': 5, 'expirationTimeMs': '1677052800000'},
                        {'id': 4, 'expirationTimeMs': '1672214400000'},
                        {'id': 3, 'expirationTimeMs': '1667372400000'},
                        {'id': 2, 'expirationTimeMs': '1664953200000'},
                        {'id': 1, 'expirationTimeMs': '1662534000000'}]

_dc_results: list['dict'] = [
    {'id': 14, 'expirationTimeMs': '1720594800000'},
    {'id': 13, 'expirationTimeMs': '1715756400000'},
    {'id': 12, 'expirationTimeMs': '1710918000000'},
]


@pytest.fixture
def create_temp_file() -> str:
    """Create a temporary file for use in validating utility functions"""
    d = Path.cwd() / "tests" / "temp_files"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "tmp_file.txt"
    p.write_text("test file", encoding="utf-8")
    yield p
    p.unlink()
    d.rmdir()


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (0, "1970-01-01 00:00:00"),
        (1708898400000, "2024-02-25 22:00:00"),
        (1711317600.99999, "2024-03-24 22:00:00"),
    ],
)
def test_human_time(test_input, expected):
    assert human_time(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (123456789, "123456789"),
        ("123456789", "123456789"),
        ("123-456-789", "123456789"),
        (1234567890, "exception:ValueError"),
    ],
)
def test_sanitize_allycode(test_input, expected):
    if 'exception' in expected:
        with pytest.raises(ValueError):
            sanitize_allycode(test_input)
    else:
        assert sanitize_allycode(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({"flags": ['gameStyle', 'calcGP', 'onlyGP']}, '?flags=calcGP,gameStyle,onlyGP&language=eng_us'),
        ({"flags": ['gameStyle', 'calcGP', 'onlygp']}, '?flags=calcGP,gameStyle&language=eng_us'),
        ({"flags": ['gameStyle']}, '?flags=gameStyle&language=eng_us'),
        ({"flags": ['gameStyle'], "lang": "fre_fr"}, '?flags=gameStyle&language=fre_fr'),
        ({"flags": 1234567890}, "exception:ValueError"),
    ],
)
def test_construct_unit_stats_query_string(test_input, expected):
    if 'exception' in expected:
        with pytest.raises(ValueError):
            construct_unit_stats_query_string(test_input['flags'])
    else:
        if 'lang' in test_input:
            assert construct_unit_stats_query_string(flags=test_input['flags'], language=test_input['lang']) == expected
        else:
            assert construct_unit_stats_query_string(flags=test_input['flags']) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (1, 25),
        ("4", 10),
        ("6", None),
    ],
)
def test_convert_division_to_int(test_input, expected):
    if expected is None:
        assert convert_divisions_to_int(test_input) is expected
    else:
        assert convert_divisions_to_int(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("Kyber", 100),
        ("carbonite", 20),
        ("unknown", None),
    ],
)
def test_convert_league_to_int(test_input, expected):
    if expected is None:
        assert convert_league_to_int(test_input) is expected
    else:
        assert convert_league_to_int(test_input) == expected


def test_get_current_gac_event(mock_response):
    """Test returning current GAC event"""
    comlink = SwgohComlink()
    current_gac_event = get_current_gac_event(comlink)
    assert "id" in current_gac_event


def test_get_guild_members_by_allycode(mock_response, allycode):
    """
    Test that game enums can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    guild_members = get_guild_members(comlink, allycode=314927874)
    assert isinstance(guild_members, list)
    assert "playerId" in guild_members[0].keys()


def test_get_guild_members_by_player_id(mock_response, player_id):
    """
    Test that game enums can be retrieved from game server correctly
    """
    comlink = SwgohComlink()
    guild_members = get_guild_members(comlink, player_id=player_id)
    assert isinstance(guild_members, list)
    assert "playerId" in guild_members[0].keys()


def test_validate_path(create_temp_file):
    assert validate_file_path(create_temp_file) is True


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (_skills, _result_skills),
        ([], []),
        ("unknown", "exception:ValueError"),
    ],
)
def test_get_tw_omicrons(test_input, expected):
    if 'exception' in expected:
        with pytest.raises(ValueError):
            get_tw_omicrons(test_input)

    elif expected is None:
        assert get_tw_omicrons(test_input) is None
    else:
        assert get_tw_omicrons(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (_dc_sets, _dc_results),
        ([], []),
        ("unknown", "exception:ValueError"),
    ],
)
def test_get_current_datacron_sets(test_input, expected):
    if 'exception' in expected:
        with pytest.raises(ValueError):
            get_current_datacron_sets(test_input)

    elif expected is None:
        assert get_current_datacron_sets(test_input) is None
    else:
        assert get_current_datacron_sets(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (_eng_us_txt, _name_key_results),
        ([], {}),
        ({}, "exception:ValueError"),
    ],
)
def test_create_localized_unit_name_dictionary(test_input, expected):
    if 'exception' in expected:
        with pytest.raises(ValueError):
            create_localized_unit_name_dictionary(test_input)

    elif expected is None:
        assert create_localized_unit_name_dictionary(test_input) is None
    else:
        assert create_localized_unit_name_dictionary(test_input) == expected
