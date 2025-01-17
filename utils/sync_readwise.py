import os
import glob
import json
import requests
import time

def get_api_token():
    token = os.environ.get('READWISE_API_TOKEN')
    if not token:
        raise ValueError('READWISE_API_TOKEN environment variable not set')
    return token

def send_to_readwise(url, token):
    try:
        response = requests.post(
            url="https://readwise.io/api/v3/save/",
            headers={"Authorization": f"Token {token}"},
            json={
                "url": url,
                "tags": ["auto-import"]
            }
        )
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:  # Too Many Requests
            retry_after = int(e.response.headers.get('Retry-After', '60'))
            print(f"Rate limit reached. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            # Retry the request once after waiting
            return send_to_readwise(url, token)
        print(f"Error sending {url} to Readwise: {str(e)}")
        return False
    except requests.RequestException as e:
        print(f"Error sending {url} to Readwise: {str(e)}")
        return False

def sync_file(json_file, token):
    print(f"Processing {json_file}...")
    try:
        with open(json_file, 'r') as f:
            posts = json.load(f)
        
        if not isinstance(posts, list):
            print(f"Error: {json_file} does not contain a list of posts")
            return
        
        success = 0
        total = 0
        
        for i, post in enumerate(posts, 1):
            if 'url' not in post:
                print(f"Warning: Post {i} is missing URL field, skipping...")
                continue
            total += 1
            if send_to_readwise(post['url'], token):
                success += 1
        
        print(f"Successfully synced {success}/{total} posts from {json_file}")
            
    except Exception as e:
        print(f"Error processing {json_file}: {str(e)}")

def main():
    try:
        token = get_api_token()
        json_files = glob.glob('*.json')
        
        if not json_files:
            print("No JSON files found")
            return
        
        for json_file in json_files:
            sync_file(json_file, token)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main() 