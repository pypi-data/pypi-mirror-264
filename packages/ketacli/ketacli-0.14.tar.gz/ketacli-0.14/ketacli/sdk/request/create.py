from ..util import is_fuzzy_key
from .asset_map import ASSET_MAP
from .asset_map import get_request_path

def create_asset_request(asset_type, name=None, data=None, **kwargs):
    path = get_request_path(asset_type, "get")
    if name is not None:
        path = f"{path}/{name}"

    return {
        "path": path,
        "query_params": {},
        # list 操作用不到的内容
        "method": "post",
        "data": data,
        "custom_headers": {},
    }
