#  Settings included in the initial app object

class AppMetadata:
    title: str = "Idoven API"
    description: str = "This API contains a Backend Challenge proposed by Idoven"
    summary: str = "To-Do"
    version: str = "0.1.0"
    contact: dict = {
        "name": "Manu Molina",
        "email": "manu.molinam@gmail.com",
    }
    license_info: dict = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }


app_metadata = AppMetadata()
