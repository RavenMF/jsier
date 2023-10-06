import json
import jsonschema
import jsondiff
import os

def new_file(name, msg=None):
    if not name.endswith(".json"):
        name += ".json"

    try:
        with open(name, "w") as file:
            if msg:
                print(f"File saved as {name}")
    except OSError as e:
        print(f"Error creating file '{name}': {str(e)}")
    return name

def load_data(filename, msg=True):
    if not os.path.isfile(filename):
        if msg:
            print(f"File '{filename}' doesn't exist.")
        return []  # Return an empty list if the file doesn't exist
    
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError:
        if msg:
            print(f"Error decoding JSON data in '{filename}'. File might be empty or corrupted.")
        return []

def save_data(filename, data, msg=None):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        if msg:
            print(f"Data saved to {filename}")
    except OSError as e:
        print(f"Error saving data to '{filename}': {str(e)}")

def add_data(filename, new_data, msg=True):
    data = load_data(filename, msg=False)
    max_id = max(item.get("id", 0) for item in data) if data else 0
    new_data["id"] = max_id + 1
    data.append(new_data)
    save_data(filename, data, msg=msg)
    if msg:
        print(f"Data added to {filename}: {new_data}")

def get_data(filename, id, msg=None):
    data = load_data(filename, msg=None)
    if data:
        for item in data:
            if item.get("id") == id:
                if msg:
                    print(f"Data retrieved from {filename}: {item}")
                return item
        if msg:
            print(f"Data with ID '{id}' not found in {filename}")
    return None

def remove_data(filename, id, msg=None):
    data = load_data(filename, msg=None)
    new_data = [item for item in data if item.get("id") != id]
    if len(new_data) < len(data):
        save_data(filename, new_data, msg=msg)
        if msg:
            print(f"Data with ID '{id}' removed from {filename}")
    elif msg:
        print(f"Data with ID '{id}' not found in {filename}")

def validate_json(filename, schema_filename):
  """Validates the JSON data in a file against a schema.

  Args:
    filename: The path to the JSON file to validate.
    schema_filename: The path to the JSON schema file.

  Returns:
    True if the JSON data is valid, False otherwise.
  """

  with open(schema_filename, "r") as file:
    schema = json.load(file)

  with open(filename, "r") as file:
    data = json.load(file)

  try:
    jsonschema.validate(data, schema)
    return True
  except jsonschema.ValidationError as e:
    print(f"JSON data in '{filename}' is invalid: {e}")
    return False

def diff_json(filename1, filename2):
  """Compares two JSON files and returns a diff object.

  Args:
    filename1: The path to the first JSON file.
    filename2: The path to the second JSON file.

  Returns:
    A jsondiff.Diff object containing the differences between the two JSON files.
  """

  with open(filename1, "r") as file:
    data1 = json.load(file)

  with open(filename2, "r") as file:
    data2 = json.load(file)
    
