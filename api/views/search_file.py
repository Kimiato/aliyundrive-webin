from sanic.response import json
from typing import List
from aligo.types import BaseFile
from aligo.types.Enum import SearchCategory

from ..app import alidrive


async def search_file(request):
    """
    搜索文件

    :request param:
    filename: [必选] 搜索的文件名
    file_category:[可选] 搜索的文件类型
    """
    filename = request.args.get("filename")
    page_marker = request.args.get("page_marker")
    if not filename:
        return json(body={'error': 'param filename'}, status=403)
    file_category = request.args.get("file_category")
    result = alidrive.search_file(name=filename, category=file_category, pagination=True, page_marker=page_marker)
    # 处理搜索结果
    next_page_marker = ''
    if result and isinstance(result[-1], str):
        next_page_marker = result.pop()
    result = handle_search_result(result)
    return json(body={"result": result, "next_page_marker": next_page_marker})


def handle_search_result(result: List[BaseFile], **kwargs) -> list:
    """处理搜索结果
    filter_types: [可选] 搜索过滤的文件类型
    """
    handle_list = []
    does_filter = True if 'filter_types' in kwargs else False
    for file in result:
        file_info = {
            'name': file.name,
            'file_id': file.file_id,
            'type': file.type
        }
        if does_filter:
            file_name_split = file.name.split('.')
            if file_name_split and file_name_split[-1] not in kwargs['filter_types']:
                continue
        handle_list.append(file_info)
    return handle_list
