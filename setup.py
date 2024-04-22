import os
import getpass

if not os.path.exists(".env"):
    token = getpass.getpass("Input Discord token (hidden, enter to quit): ")
    if token.strip() != "":
        with open(".env", "w") as env_f:
            env_f.write(f"TOKEN={token}")
        print("Written Discord Token to .env")

if not os.path.exists("./images"):
    try:
        os.makedirs("./images")
    except FileExistsError:
        pass # Happens for symbolic links?

if not os.path.exists("./utilities/reverse_api/.env"):
    while True:
        username = input("Input Microsoft username for reverse API if needed (press enter to quit): ")
        if username.strip() == "":
            break
        password = getpass.getpass("Input your password (hidden): ")
        if password.strip() == "":
            break
        pair = f"{username}={password}"
        with open("./utilities/reverse_api/.env", "a") as env_f:
            env_f.write(pair)
        print(f"Written {pair}")

if not os.path.exists("./utilities/reverse_api/prompt.txt"):
    prompt = input("Input username (press enter to quit): ")
    with open("./utilities/reverse_api/prompt.txt", "w") as f:
        f.write(pair)

if os.path.exists("./utilities/reverse_api/usernames.json"):
    with open("./utilities/reverse_api/usernames.json") as ufile:
        usernames = json.load(ufile)
else:
    with open("./utilities/reverse_api/usernames.json", 'w') as uFile:
        print("intialised usernames.json as it does not exist, please use this file for loading of accounts (in the normal key)")
        usernames = {"normal": [], "cookie": [], "unusable": [], "otp": []}
        json.dump(usernames, uFile, indent=4)

os.system("pip install -r requirements.txt")
print("Setup complete!")