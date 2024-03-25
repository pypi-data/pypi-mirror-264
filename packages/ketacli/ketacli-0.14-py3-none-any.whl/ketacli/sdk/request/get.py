from ..util import is_fuzzy_key
from .asset_map import ASSET_MAP, get_request_path

def get_asset_by_id_request(asset_type, asset_id=None, lang=None, **kwargs):
    path = get_request_path(asset_type, "get")
    if asset_id is not None:
        path = f"{path}/{asset_id}"
    
    custom_headers = {}
    if lang is not None and isinstance(lang, str):
        custom_headers["X-Pandora-Language"] = lang

    return {
        "path": path,
        "query_params": {},
        # list 操作用不到的内容
        "method": "get",
        "data": {},
        "custom_headers": custom_headers,
    }
