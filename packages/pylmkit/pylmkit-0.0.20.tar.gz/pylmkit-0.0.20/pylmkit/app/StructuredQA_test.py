def run_sql(connection, sql):
    results = {'data': "", "columns": []}
    with connection.cursor() as cursor:
        try:
            # 执行SQL语句
            cursor.execute(sql)
            results['columns'] = [i[0] for i in cursor.description]
            # 获取所有记录列表
            results['data'] = cursor.fetchall()
        except:
            pass
    return results


def parse_sql(text):
    sql_statement = ''
    if '```sql' in text and '```' in text:
        sql_statement = text.split('```sql')[1].split('```')[0].replace('\n', ' ')
    return sql_statement


def get_sql(model, connection, prompt, max_get_sql_num=5):
    try:
        if max_get_sql_num != 0:
            respond = model.invoke(prompt)
            respond = respond if isinstance(respond, str) else respond.content
            sql_query = parse_sql(respond)
            if sql_query:
                # print("sql_query：", sql_query)
                sql_result = run_sql(connection, sql_query)
                # print('sql_result: ', sql_result)
                if sql_result['data']:
                    return {
                        "status_code": True,
                        "sql_query": sql_query,
                        "sql_result": sql_result,
                        "run_num": max_get_sql_num
                    }
                else:
                    print('运行SQL错误，重新运行 ........')
                    return get_sql(model, connection, prompt, max_get_sql_num - 1)
            else:
                print('生成SQL错误，重新运行 ........')
                return get_sql(model, connection, prompt, max_get_sql_num - 1)
        else:
            return {
                "status_code": False,
                "sql_query": "",
                "sql_result": {},
                "run_num": max_get_sql_num
            }
    except Exception as e:
        # 这里可以添加更详细的错误处理逻辑
        print(f"An error occurred: {e}")
        return {
            "status_code": False,
            "error": str(e),
            "sql_query": '',
            "sql_result": '',
            "run_num": max_get_sql_num
        }


sql_prompt = """
你是一个MySQL专家。给定一个输入问题，首先创建一个语法正确的MySQL查询来运行，然后查看查询的结果并返回输入问题的答案。
永远不要查询表中的所有列。您必须只查询回答问题所需的列。将每个列名用双引号(")括起来，以表示它们为分隔符。
注意，只使用您可以在下面的表中看到的列名。注意不要查询不存在的列。另外，要注意哪个列在哪个表中。
注意，不局限单表查询，如果用户问题涉及多个表关联查询，则需要多表关联查询，比如：
```sql
SELECT pi.project_name
FROM tabel1 AS pi
INNER JOIN tabel2 AS pm ON pi.project_id = pm.project_id
WHERE pm.member_code = '666666';
```
Use the following format:
```sql
SELECT xx1 FROM database.table WHERE xx2 = '882399'
```
Only use the following tables:
{table_info}
Question: {input}
"""
sql_qa_prompt = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
Question: {query}
SQL Query: {sql_query}
SQL Result: {sql_result}
Answer: """


def get_column_comments(connection, database_name, table_name):
    """
    获取指定数据库中指定表的列名及其注释。
    :param connection: pymysql数据库连接对象
    :param database_name: 数据库名
    :param table_name: 表名
    :return: 一个包含列名和注释的字典
    """
    # 使用 cursor() 方法创建一个游标对象 cursor
    with connection.cursor() as cursor:
        # SQL 查询语句，获取指定数据库中指定表的列信息
        sql = """
        SELECT COLUMN_NAME, COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        """
        # 执行SQL语句
        cursor.execute(sql, (database_name, table_name))
        # 获取所有记录列表
        results = cursor.fetchall()
    # 将查询结果转换为字典形式
    columns_dict = {row[0]: row[1] for row in results}
    return columns_dict


def get_batch_column_comments(connection, database_name, table_names, table_use_names):
    column_comtents = ""
    # 调用函数获取列名和注释
    for i in range(len(table_names)):
        columns_dict = get_column_comments(connection,
                                           database_name,
                                           table_names[i]
                                           )
        column_comtents += f"'数据库名称为{database_name} {table_use_names[i]}:{table_names[i]}': 字段名" + str \
            (columns_dict).replace(' ', '') + '\n'
    # connection.close()
    # print(len(column_comtents))
    return column_comtents
