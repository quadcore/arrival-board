from datasources.opensky import OpenSkyApi
from config import APP_CONFIG
from config import init as init_config

def run():
    init_config()
    
    print(APP_CONFIG)
    print("\n")

    opensky_api = OpenSkyApi()
    state_vectors = opensky_api.get_state_vectors()
    print(state_vectors)

if __name__ == "__main__":
    run()
