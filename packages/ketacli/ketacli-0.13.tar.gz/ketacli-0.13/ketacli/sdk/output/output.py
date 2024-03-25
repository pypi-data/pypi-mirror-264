import json

from datetime import datetime
from .format import make_records_to_table, make_table, make_table, prettify_value
from ..util import is_fuzzy_key

RESP_OUTPUT_KEY = {
    "bizsystems": "items",
    "target": "items",
    "targettype": "items",
}


def find_list_field(resp={}):
    """找寻返回结果中的list类型字段，用来查找分页返回结果中应该处理字段的函数

    Args:
        resp (dict, optional): 分页返回结果. Defaults to {}.

    Returns:
        str | None: 第一个list类型字段的key，如果没有则返回None
    """
    for k in resp:
        if isinstance(resp[k], list):
            return k
    return None


def find_result_field(asset_type, resp={}):
    ""
    # 检查白名单有无这个字段的定义，如果有，则直接使用
    real_asset_key = is_fuzzy_key(asset_type, value_map=RESP_OUTPUT_KEY)
    if real_asset_key is not None:
        return RESP_OUTPUT_KEY.get(real_asset_key)

    key = None
    # 优先查看返回结果里是否有类似命名的字段
    key = is_fuzzy_key(asset_type, value_map=resp)

    # 如果最终没有找到类似的字段，则找一个list字段
    if key is None:
        key = find_list_field(resp)

    # 如果返回结果为空
    if key is None or not isinstance(resp[key], list) or len(resp[key]) <= 0:
        return None

    return key


def list_output(asset_type, output_fields=[], resp={}):
    total = resp.get("total")
    if total is None:
        total = 0
    print(f"we have {total} {asset_type} in total")

    result_field = find_result_field(asset_type, resp)
    if result_field is None:
        return None

    table = make_records_to_table(output_fields, resp[result_field])
    return table


def search_result_output(result={}):
    header = []
    for f in result["fields"]:
        header.append(f["name"])
    rows = result["rows"]
    return make_table(header, rows)


def get_asset_output(resp={}, output_fields=[]):
    header = ["field", "value"]
    fields = []
    filter_field = len(output_fields) > 0
    output_fields = set(output_fields)
    for k in resp:
        if (not filter_field) or (k in output_fields):
            fields.append([k, prettify_value(k, resp[k])])
    table = make_table(header, fields)
    return table


def describe_output(asset_type, resp={}):
    """通过result字段推断这个资源返回字段的类型

    Args:
        asset_type (str): 资源的类型，如repo、dashboard等
        resp (dict, optional): 请求的返回体. Defaults to {}.

    Returns:
        PrettyTable | None: 返回格式化好的表格，或者如果没有result字段则返回None
    """
    total = resp.get("total")
    if total is None or total <= 0:
        return None

    result_field = find_result_field(asset_type, resp)
    if result_field is None:
        return None

    header = ["fields", "type"]
    fields = []
    for k in resp[result_field][0]:
        fields.append((k, str(type(resp[result_field][0][k]))))
    table = make_table(header, fields)
    return table


def rs_output_all(asset_types={}):
    header = ["资源类型", "资源描述", "API路径", "支持方法"]
    rows = []
    for rs in asset_types:
        conf = asset_types.get(rs)
        rows.append([rs, conf.get("desc"), conf.get("path"),
                    conf.get("methods")])
    return make_table(header, rows)


def rs_output_one(rs, conf: dict = {}):
    header = ["字段", "值"]
    if conf is None or len(conf) <= 0:
        return make_table(header, [])
    rows = [
        ["资源类型", rs],
        ["资源描述", conf.get("desc")],
        ["API路径", "/" + conf.get("path")],
    ]

    methods = ""
    if "methods" in conf:
        for m in conf.get("methods"):
            cmd = help_methods(rs, m)
            methods += f"{cmd}\n"
        cmd = help_methods(rs, "describe")
        methods += f"{cmd}\n"
    if len(methods) > 0:
        rows.append(["支持方法", methods.strip()])
        
    # example = conf.get("example")
    # if example is not None and len(example) > 0:
    #     rows.append(["请求示例", example])
    return make_table(header, rows)


def help_methods(rs: str, m: str = "list"):
    if m == "list":
        return f"列举资源：ketacli {m} {rs} [--fields FIELDS] [-f FORMAT] [--lang LANG] "
    if m == "get":
        return f"根据id或名字查询：ketacli {m} {rs} \"resource_id_or_name\" [--fields FIELDS] [-f FORMAT]"
    if m == "create":
        return f"创建资源：ketacli {m} {rs} [--file \"/path/to/file\"] [--data ...(json config)]"
    if m == "describe":
        return f"获取资源结构：ketacli {m} {rs} [--fields FIELDS] [-f FORMAT]"
