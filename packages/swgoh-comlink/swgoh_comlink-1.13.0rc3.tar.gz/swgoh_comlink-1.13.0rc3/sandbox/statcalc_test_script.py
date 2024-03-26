from comlink_python import StatCalc, SwgohComlink, DataBuilder
import json

print("Starting StatCalc test run...")

comlink = SwgohComlink()
comlink_stats = SwgohComlink(url='http://192.168.1.168:3200', stats_url='http://192.168.1.168:3223')
print("Getting player roster information...")
player = comlink.get_player(allycode=314927874)
test_char = player['rosterUnit'][102]
print(f"Character {test_char['definitionId']} selected for testing.")
print("Getting stats calc from via python wrapper call to Docker...")
test_char['rarity'] = test_char['currentRarity']
test_char['level'] = test_char['currentLevel']
test_char['gear'] = test_char['currentTier']
test_char['equipped'] = test_char['equipment']
test_char['skills'] = test_char['skill']
test_char['mods'] = test_char['equippedStatMod']
for mod in test_char['mods']:
    mod['pips'] = mod['tier']
test_char_list = [test_char]
test_char_stats = comlink_stats.get_unit_stats(request_payload=test_char_list)
print("Stats calc complete.")

print("Writing old stats to file...")
with open('test_char_stats_orig.json', 'w') as outfile:
    json.dump(test_char_stats[0]['stats'], outfile, indent=2, sort_keys=True)
print("Stats written to file.")

if not DataBuilder.is_initialized():
    print("Initializing DataBuilder...")
    DataBuilder.initialize()

print("Initialing StatCalc...")
StatCalc.initialize()
print("Getting stats calc from StatCalc...")
test_stats = StatCalc.calc_char_stats(char=test_char)
print("Writing new stats to file...")
with open('test_char_stats_new.json', 'w') as outfile:
    json.dump(test_stats, outfile, indent=2, sort_keys=True)

print("Stats written to file.")
print("Execution complete.")
