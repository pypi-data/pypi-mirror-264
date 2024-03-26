import json
import os

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils import normpath


class InputData:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        script.append("\n# INPUT")

        encoding: str = settings["encoding"] if "encoding" in settings else "ISO-8859-1"
        dtype = str if "as_string" in settings and settings["as_string"] == True else None
        delimiter: str = settings["delimiter"] if "delimiter" in settings and settings["delimiter"] else None
        header: str = None if "has_header" in settings and settings["has_header"] == False else "infer"
        file_path = normpath(settings["file_path"]) if "file_path" in settings else ""

        # !! Deploy mode habilitado
        deploy_enabled: bool = settings["deploy_enabled"] if "deploy_enabled" in settings else False

        if deploy_enabled:
            if "deploy_file_path" not in settings or not settings["deploy_file_path"]:
                msg = app_message.dataprep["nodes"]["deploy_enabled"](node_key)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            file_path = normpath(settings["deploy_file_path"]) if "deploy_file_path" in settings else ""

        _, file_ext = os.path.splitext(file_path)
        file_ext = file_ext[1:]
        
        # * check file exists
        file_exists = os.path.exists(file_path)
        
        if not file_exists:
            msg = app_message.dataprep["nodes"]["input_data"]["file_not_exist"](node_key, file_path)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        
        try:
            bug_handler.console('Leyendo fuente "{}"...'.format(file_path), "trace", flow_id)
            if file_ext in ["csv", "txt"]:
                df = pd.read_csv(
                    file_path,
                    dtype=dtype,
                    encoding=encoding,
                    delimiter=delimiter,
                    header=header,
                )
                dtype_str = 'str' if dtype != None else None
                header_str = f"'{header}'" if header else None
                
                script.append(f"df = pd.read_csv('{file_path}', dtype={dtype_str}, encoding='{encoding}', delimiter='{delimiter}', header={header_str})")
                
                # add prefix to df columns
                if header is None:
                    df.columns = [f"col_{name}" for name in df.columns]
                    script.append('df.columns = [f"col_{name}" for name in df.columns]')
                    
                
            elif file_ext == "json":
                orient = settings["orient"] if "orient" in settings else "columns"
                df = pd.read_json(file_path, orient=orient, encoding=encoding)
                script.append(f"df = pd.read_json('{file_path}', orient='{orient}', encoding='{encoding}')")
                
            elif file_ext in ["xls", "xlsx", "xlsm", "xlsb"]:
                sheet_name = settings["sheet_name"] if "sheet_name" in settings else 0
                df = pd.read_excel(file_path, dtype=dtype, sheet_name=sheet_name)
                dtype_str = 'str' if dtype != None else None
                script.append(f"df = pd.read_excel('{file_path}', dtype={dtype_str}, sheet_name='{sheet_name}')")
                
            else:
                msg = app_message.dataprep["nodes"]["input_data"]["unknow_format"](node_key, file_ext)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            df.columns = [str(c) for c in df.columns]

            # revisar si algun nombre de columna tiene espacio al inicio o al final
            if True in [c.startswith((" ", "\t")) or c.endswith((" ", "\t")) for c in df.columns]:
                df.columns = [c.strip() for c in df.columns]
                msg = app_message.dataprep["nodes"]["input_data"]["end_start_spaces"](node_key)
                bug_handler.default_node_log(flow_id, node_key, msg, console_level="warn", bug_level="warning")

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
