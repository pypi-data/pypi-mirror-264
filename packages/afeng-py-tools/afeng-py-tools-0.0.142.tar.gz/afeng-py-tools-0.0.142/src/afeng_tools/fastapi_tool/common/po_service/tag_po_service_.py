from afeng_tools.fastapi_tool.common.po_service.base_po_service import PoService


class TagPoService(PoService):
    """
    使用示例：tag_po_service = TagPoService(app_info.db_code, TagInfoPo)
    """
    _table_name_ = "tb_tag_info"
    pass
