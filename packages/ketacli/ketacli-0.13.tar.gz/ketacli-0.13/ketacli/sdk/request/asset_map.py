from ..util import is_fuzzy_key


ASSET_MAP = {
    # key 都小写
    "repos": {
        "path": "repos",
        "desc": "仓库",
        "query_fields": [
            {"field": "withDocSize", "required": False, "default": True},
        ],
        "methods": {
            "list": "repos",
            "get": "repos",
            "create": "repos",
        },
        "example": {
            "name": "app_mongodb_log",
            "type": "EVENTS",
            "groupPathNames": "数据存储/Mongodb",
            "description": "mongodb日志存储仓库, 默认存储 15 天",
            "retention": 1296000000,
            "writeRefreshIntervalInSeconds": 10,
            "shardMaxDocs": 50000000,
            "shardMaxSizeInMB": 51200,
            "indexMaxAgeInSecond": 86400
        },
    },
    "sourcetype": {
        "path": "sourcetype",
        "desc": "来源类型",
        "methods": {
            "list": "sourcetype",
            "get": "sourcetype",
            "create": "sourcetype",
        },
        "example": {
            "name": "sourcetype_name",
            "line": {"type": "single", "regex": ""},
            "datetime": {
                "type": "auto",
                "zoneOffset": 8,
                "dateTimeFormat": "",
                "dateTimePrefix": "",
                "maxDateTimeLength": 100,
            },
            "description": "",
            "category": "custom",
            "advance": {"charset": "utf-8", "fieldDiscovery": True},
            "preset": 0,
            "extractions": [],
        }
    },
    "extractions": {
        "path": "extractions/list",
        "desc": "字段提取规则",
        "methods": {
            "list": "extractions/list",
            "get": "extractions",
            "create": "extractions",  # 不带名字
        },
        "example": {
            "name": "extraction_name",
            "description": "",
            "type": "regex",
            "config": {
                "pattern": "^(?<a>[\\s\\S]+)",
                "delimiter": ",",
                "delimiterKv": ":"
            },
            "sourcetype": "json",
            "indexed": False,
            "app": "search",
            "schema": [
                {
                    "field": "a"
                }
            ],
            "groupIds": []
        }
    },
    "targets": {
        "path": "metric/targets",
        "desc": "运维资产对象",
        "methods": {
            "list": "metric/targets",
            "get": "metric/targets",
            "create": "metric/targets",
        },
        "example": {
            "targetTypeId": "_storage_switch",
            "identities": {"name": "target_id"},
            "names": {"name": "target_name"},
            "properties": {},
            "customProperties": {}
        }
    },
    "bizsystems": {
        "path": "target/bizSystems",
        "desc": "运维资产业务系统",
        "methods": {
            "list": "target/bizSystems",
            "get": "target/bizSystems",
            "create": "target/bizSystems",
        }
    },
    "metrics": {
        "path": "metric/metrics",
        "desc": "指标",
        "methods": {
            "list": "metric/metrics",
            "get": "metric/metrics",
            "create": "metric/metrics",
        }
    },
    "users": {
        "path": "auth/users",
        "desc": "用户",
        "methods": {
            "list": "auth/users",
        }
    },
    "roles": {
        "path": "auth/roles",
        "desc": "角色",
        "methods": {
            "list": "auth/roles",
        }
    },
    "alerts": {
        "path": "alerts",
        "desc": "告警规则",
        "methods": {
            "list": "alerts",
            "get": "alerts",
        }
    },



    # KetaAgent DC 模块
    "dc/collector/config": {
        "path": "dc/collector/config",
        "desc": "KetaAgent 采集任务配置",
        "methods": {
            "list": "dc/collector/config"
        }
    },
    "dc/collector/server/config": {
        "path": "dc/collector/server/config",
        "desc": "KetaAgent 服务端采集任务配置",
        "methods": {
            "list": "dc/collector/server/config"
        }
    },
    "dc/kubernetes/collector/rule": {
        "path": "dc/kubernetes/collector/rule",
        "desc": "KetaAgent 容器采集任务",
        "methods": {
            "list": "dc/kubernetes/collector/rule"
        }
    },
    "dc/agent": {
        "path": "dc/agent/list",
        "desc": "KetaAgent Agent实例",
        "methods": {
            "list": "dc/agent/list"
        }
    },
    "dc/tags": {
        "path": "dc/tags",
        "desc": "KetaAgent Agent标签",
        "methods": {
            "list": "dc/tags"
        }
    },
    "dc/collect/types": {
        "path": "dc/collect/types",
        "desc": "KetaAgent 采集模板",
        "methods": {
            "list": "dc/collect/types"
        }
    },
    "dc/transformer/types": {
        "path": "dc/transformer/types",
        "desc": "KetaAgent 解析模板",
        "methods": {
            "list": "dc/transformer/types"
        }
    },
    "dc/package": {
        "path": "dc/package/list",
        "desc": "KetaAgent 安装包",
        "methods": {
            "list": "dc/package/list"
        }
    },
}


def get_request_path(asset_type, method):
    path = asset_type
    
    key = is_fuzzy_key(asset_type, value_map=ASSET_MAP)
    print(key)
    if key is None:
        return asset_type
    if "methods" in ASSET_MAP[key] and method in ASSET_MAP[key]["methods"]:
        path = ASSET_MAP.get(key)["methods"][method]
    else:
        path = ASSET_MAP.get(key)["path"]
    return path
        
    
def get_resources():
    return ASSET_MAP

def get_resource(asset_type):
    return ASSET_MAP.get(asset_type)