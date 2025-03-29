from app.mikrotik.routeros import connect

def create_pppoe_user(username, password, profile="pppoe-profile"):
    conn = connect()
    api = conn.get_api()

    user_data = {
        "name": username,
        "password": password,
        "service": "pppoe",
        "profile": profile
    }

    api.get_resource('/ppp/secret').add(**user_data)
    conn.disconnect()

def list_pppoe_users():
    conn = connect()
    api = conn.get_api()
    users = api.get_resource('/ppp/secret').get()
    conn.disconnect()
    return users

def suspender_pppoe_user(username):
    conn = connect()
    api = conn.get_api()
    secrets = api.get_resource('/ppp/secret')
    secrets.set(**{"name": username, "disabled": "true"})
    conn.disconnect()

def activar_pppoe_user(username):
    conn = connect()
    api = conn.get_api()
    secrets = api.get_resource('/ppp/secret')
    secrets.set(**{"name": username, "disabled": "false"})
    conn.disconnect()
