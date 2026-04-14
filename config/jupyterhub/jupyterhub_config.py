# JupyterHub Configuration for Shipsmart

# Server settings
c.JupyterHub.bind_url = "http://0.0.0.0:8000"
c.JupyterHub.port = 8000

# Authenticator settings
c.JupyterHub.authenticator_class = "dummy"
c.DummyAuthenticator.passwords = {
    "admin": "shipsmartadmin",
    "teamlead": "shipsmart123",
    "mlengineer": "mlpassword",
    "dataengineer": "datapassword",
}

# Admin users
c.Authenticator.admin_user = "admin"

# Spawner settings
c.Spawner.default_url = "/lab"
c.Spawner.start_timeout = 300
c.Spawner.http_timeout = 60
c.Spawner.mem_limit = "4G"
c.Spawner.cpu_limit = 2

# Notebook settings
c.NotebookApp.ip = "0.0.0.0"
c.NotebookApp.open_browser = False
c.NotebookApp.disable_check_xsrf = False

# Proxy settings
c.JupyterHub.base_url = "/"

# Service settings
c.JupyterHub.cleanup_servers = True
c.JupyterHub.cookie_max_age_days = 7

# Logging
c.JupyterHub.log_level = "INFO"
 
