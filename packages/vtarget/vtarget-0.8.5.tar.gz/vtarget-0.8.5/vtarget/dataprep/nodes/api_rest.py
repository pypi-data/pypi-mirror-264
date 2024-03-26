import json
import pprint

import numpy as np
import pandas as pd
import requests

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class ApiRest:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        script.append("\n# APIREST")
        method: str = settings["method"] if "method" in settings and settings["method"] else None
        url: str = settings["url"] if "url" in settings and settings["url"] else None
        headers: list = settings["headers"] if "headers" in settings and settings["headers"] else []
        params: list = settings["params"] if "params" in settings and settings["params"] else []
        items: str = settings["items"] if "items" in settings and settings["items"] else "data.items"

        if not method:
            msg = app_message["nodes"]["api-rest"]["no_method"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        if not url:
            msg = app_message["nodes"]["api-rest"]["no_url"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            # method = "GET"
            # url = "https://api.clay.cl/v1/cuentas_bancarias/movimientos/"

            headers = {item["prop"]: item["value"] for item in headers}
            params = {item["prop"]: item["value"] for item in params}
            print('0')
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
            )
            print('1')
            script.append(
                f"import requests\n\nresponse = requests.request(\n\t'{method}', \n\t'{url}', \n\theaders={headers}, \n\tparams={params}\n)\n\nresponse = response.json()"
            )

            response_json = response.json()
            new_items = "".join([f'["{i}"]' for i in items.split(".")])
            df = eval(f"pd.DataFrame(response_json{new_items})")

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(e.args)})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}
