from comlink_python import SwgohComlink
import base64
import zipfile
import io

# create an instance of a SwgohComlink object
comlink = SwgohComlink()

game_data_versions = comlink.get_latest_game_data_version()
location_bundle = comlink.get_localization_bundle(id=game_data_versions['language'])
loc_bundle_decoded = base64.b64decode(location_bundle['localizationBundle'])
zip_obj = zipfile.ZipFile(io.BytesIO(loc_bundle_decoded))
