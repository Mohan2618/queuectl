from core.database import Database


def config_set(key, value):
    db = Database()

    db.set_config(key, value)

    print(f"{key} = {value}")

    db.close()


def config_get(key):
    db = Database()

    value = db.get_config(key)

    if value is None:
        print("Not set.")
    else:
        print(value)

    db.close()