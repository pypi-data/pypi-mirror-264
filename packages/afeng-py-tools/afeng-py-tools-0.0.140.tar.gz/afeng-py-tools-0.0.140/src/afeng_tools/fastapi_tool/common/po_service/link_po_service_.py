from typing import Any

from afeng_tools.fastapi_tool.common.po_service.base_po_service import PoService


class LinkPoService(PoService):
    """
    使用示例：link_po_service = LinkPoService(app_info.db_code, LinkInfoPo)
    """
    _table_name_ = "tb_link_info"

    def query_by_type_code(self, type_code: str) -> list[Any]:
        return self.query_more(self.model_type.type_code == type_code)
