
def require_limit(sql: str):
    lower_sql = sql.lower()
    if 'limit' not in lower_sql:
        return True
    idx = lower_sql.rindex('limit')
    if idx > 0 and ')' in lower_sql[idx:]:
        return True
    return False


def limit_one_sql_args(sql: str):
    if require_limit(sql):
        return '{} LIMIT 1'.format(sql)
    return sql
