

def is_key(key, value_map={}):
    """精确匹配是否存在key

    Args:
        key (str): 字符串key
        value_map (dict, optional): 是否存在该key的字典. Defaults to {}.

    Returns:
        _type_: 最终的key，如果不存在则为None
    """
    newkey = key.lower()
    if newkey in value_map:
        return newkey
    return None

def is_fuzzy_key(key, value_map={}):
    """
    检查key或者key的复数形式在map中，并返回最终map中的key
    """
    newkey = key.lower() 
    if newkey in value_map:
        return newkey
    if newkey.endswith('s'):
        newkey = newkey[:-1]
    else:
        newkey = newkey + 's'
    if newkey in value_map:
        return newkey
    return None