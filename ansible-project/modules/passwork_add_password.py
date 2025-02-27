#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests
import random
import string

def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def main():
    module_args = dict(
        api_url=dict(type='str', required=True),
        api_token=dict(type='str', required=True),
        record_title=dict(type='str', required=True),
        category_id=dict(type='int', required=True),
        user_id=dict(type='int', required=False),
        group_id=dict(type='int', required=False),
        password_length=dict(type='int', default=16)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    api_url = module.params['api_url']
    api_token = module.params['api_token']
    record_title = module.params['record_title']
    category_id = module.params['category_id']
    user_id = module.params['user_id']
    group_id = module.params['group_id']
    password_length = module.params['password_length']

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    password = generate_password(password_length)

    payload = {
        'title': record_title,
        'login': '',
        'password': password,
        'category_id': category_id,
        'url': '',
        'user_id': user_id,
        'group_id': group_id
    }

    if module.check_mode:
        module.exit_json(changed=True, msg="Password would be added to Passwork", password=password)

    try:
        response = requests.post(f'{api_url}/api/v2/records', json=payload, headers=headers)
        response.raise_for_status()
        module.exit_json(changed=True, msg="Password added to Passwork", password=password, record=response.json())
    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Failed to add password to Passwork: {e}")

if __name__ == '__main__':
    main()