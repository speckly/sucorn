import os
import getpass

if not os.path.exists(".env"):
    token = getpass.getpass("Input your Discord token (hidden): ")
    with open(".env", "w") as env_f:
        env_f.write(f"TOKEN={token}")
    print("Written Discord Token to .env")

if not os.path.exists("./images"):
    os.makedirs("./images")

if not os.path.exists(".env"):
    token = getpass.getpass("Input your Discord token (hidden): ")
    with open(".env", "w") as env_f:
        env_f.write(f"TOKEN={token}")
    print("Written Discord Token to .env")