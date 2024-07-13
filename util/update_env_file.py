from dotenv import load_dotenv, set_key
import os


def update_env(key, value):
    """
    Function to update or add a variable in the .env file
    """

    # Specify the .env file path
    file_path = ".env"

    # Load the existing environment variables
    load_dotenv(file_path)

    # Read the current .env file content
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
    else:
        lines = []

    # Prepare the new line to be added or updated
    new_line = f"{key}={value}\n"
    key_exists = False

    # Update the existing line if the key is found
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = new_line
            key_exists = True
            break

    # If the key does not exist, add the new line
    if not key_exists:
        lines.append(new_line)

    # Write the updated content back to the .env file
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":

    # Example
    env_variable = "DATABASE_URL"
    env_value = "postgres://user:password@localhost:5432/mydatabase"

    # Update or add the variable in the .env file
    update_env(env_variable, env_value)

    # Optionally, reload the environment variables
    load_dotenv()

    # Verify the update
    print("The database URL is:", os.getenv(env_variable))
