"""
Script to show collection of groups of player data using threads versus asyncio
"""
from swgoh_comlink import SwgohComlink, Utils
import concurrent.futures
import time
import sys


def split_list(s_list: list, segments: int) -> iter:
    for i in range(0, len(s_list), segments):
        yield s_list[i:i + segments]


def get_players(cl: SwgohComlink, player_list: list) -> list:
    """Take list of player IDs or allyCodes and collect the information for each"""

    return_list = []
    for player in player_list:
        if len(player) == 9 or '-' in player:
            p = cl.get_player(allycode=player)
        else:
            p = cl.get_player(player_id=player)
        if 'rosterUnit' in p:
            return_list.append(p)
    return return_list


def get_player_ids(g_members: list) -> list:
    """Take list of guild members from the get_guild() return data and return list of player Ids"""
    p_ids = []
    for member in g_members:
        p_ids.append(member['playerId'])
    return p_ids


def main():
    log = Utils.get_logger()
    guild_member = 0
    log.info("Prompting for guild member allycode...")
    while len(str(guild_member)) != 9:
        guild_member = input("Please enter the allycode for a guild member: ")
        if '-' in guild_member:
            guild_member = guild_member.replace('-', '')
        if len(str(guild_member)) != 9:
            print("Invalid allycode format. Please input the allycode as 'xxx-xxx-xxx' or 'xxxxxxxxx'.")
    log.debug(f"{guild_member} allycode entered...")
    log.info("Creating SwgohComlink instance...")
    comlink = SwgohComlink()
    log.info("Getting guild Id information...")
    player = comlink.get_player(allycode=guild_member)

    if 'guildId' not in player:
        log.error(f"An error occurred while attempting to get the guild membership for allycode {guild_member}.")
        print(f"An error occurred while attempting to get the guild membership for allycode {guild_member}.")
        sys.exit(1)

    log.info("Getting guild information...")
    guild = comlink.get_guild(guild_id=player['guildId'])
    log.info("Getting guild member information...")
    player_ids = get_player_ids(guild['member'])
    begin_count = len(player_ids)
    log.info(f"Total number of guild members is {begin_count}...")
    if begin_count > 25:
        player_lists = list(split_list(player_ids, 25))
    else:
        player_lists = [player_ids]
    player_id_list = []
    start_ts = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_player_lists = {executor.submit(get_players, comlink, p_list): p_list for p_list in player_lists}
        for future in concurrent.futures.as_completed(future_to_player_lists):
            try:
                player_id_list.extend(future.result())
                log.info(f"'player_id_list' has {len(player_id_list)} items.")
            except Exception as exc:
                print(f'Exception caught: {exc}')
    end_ts = time.time()
    print(f'\nData collection for {len(player_id_list)} players completed in {end_ts - start_ts} seconds.\n')
    # pp(player_id_list, depth=3, compact=True)


if __name__ == '__main__':
    main()
