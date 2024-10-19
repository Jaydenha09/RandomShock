import requests
import random
import time
import threading

# Settings
api_key = "api_key"
shock_ids = ["id1", "id2"]
# In seconds, must not lower than 0.3 and not higher than 30
min_shock_duration = 0.3
max_shock_duration = 30
# Intensity settings, must not lower than 1 and must not higher than 100
min_shock_intensity = 1
max_shock_intensity = 100
min_sleep_time = 10
max_sleep_time = 600
# Endpoint domain
endpoint="api.openshock.app" # Set this to your custom endpoint if you have one or leave it

shock_duration = 0
min_shock_duration_ms = min_shock_duration * 1000
max_shock_duration_ms = max_shock_duration * 1000

if not (0.3 <= min_shock_duration <= 30 and 0.3 <= max_shock_duration <= 30 and 1 <= min_shock_intensity <= 100 and 1 <= max_shock_intensity <= 100):
    raise ValueError("Variables out of range")

def trigger_shock(api_key, shock_id, intensity, duration, shock_type='Shock'):
    global shock_duration
    url = f'https://{endpoint}/2/shockers/control'
    headers = {
        'accept': 'application/json',
        'OpenShockToken': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'shocks': [{
            'id': shock_id,
            'type': shock_type,
            'intensity': intensity,
            'duration': duration,
            'exclusive': True
        }],
        'customName': 'ShockControl'
    }

    try:
        response = requests.post(url=url, headers=headers, json=payload)
        response_data = {
            'status_code': response.status_code,
            'response_body': response.json() if response.headers.get('content-type') == 'application/json' else response.text,
            'success': response.status_code == 200
        }
        print(f"Triggered shock for {shock_id}: {response_data}")
        
        shock_duration = duration
    except requests.exceptions.RequestException as e:
        print(f"Error triggering shock for {shock_id}: {str(e)}")

def randomize_shocks(shock_ids):
    method_choice = random.choice(['all', 'random_amount', 'random_one'])
    duration = random.randint(int(min_shock_duration_ms), int(max_shock_duration_ms))
    duration = round(duration, -3)

    if method_choice == 'all':
        threads = []
        for shock_id in shock_ids:
            intensity = random.randint(min_shock_intensity, max_shock_intensity)
            thread = threading.Thread(target=trigger_shock, args=(api_key, shock_id, intensity, duration))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    elif method_choice == 'random_amount':
        num_shockers = random.randint(1, len(shock_ids))
        selected_shockers = random.sample(shock_ids, num_shockers)
        threads = []
        for shock_id in selected_shockers:
            intensity = random.randint(min_shock_intensity, max_shock_intensity)
            thread = threading.Thread(target=trigger_shock, args=(api_key, shock_id, intensity, duration))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    elif method_choice == 'random_one':
        shock_id = random.choice(shock_ids)
        intensity = random.randint(min_shock_intensity, max_shock_intensity)
        thread = threading.Thread(target=trigger_shock, args=(api_key, shock_id, intensity, duration))
        thread.start()
        thread.join()

while True:
    randomize_shocks(shock_ids)
    shock_duration_n = int(shock_duration / 1000)
    next_shock_time = random.randint(min_sleep_time, max_sleep_time)
    
    for shocking_remaining in range(shock_duration_n, 0, -1):
        print(f"\rShocking for {shocking_remaining} seconds.", end="")
        time.sleep(1)
    
    for remaining in range(next_shock_time, 0, -1):
        print(f"\rNext API request will be sent in {remaining} seconds.", end="")
        time.sleep(1)

    print()