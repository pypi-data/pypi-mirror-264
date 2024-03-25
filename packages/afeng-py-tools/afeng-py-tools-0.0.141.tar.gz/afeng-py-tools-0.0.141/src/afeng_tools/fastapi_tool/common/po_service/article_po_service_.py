from typing import Any

from afeng_tools.fastapi_tool.common.po_service.base_po_service import PoService


class ArticlePoService(PoService):
    """
    使用示例：article_po_service = ArticlePoService(app_info.db_code, ArticleInfoPo)
    """
    _table_name_ = "tb_article_info"

    def query_by_code(self, type_code: str, article_code: str) -> Any:
        return self.get(self.model_type.type_code == type_code, self.model_type.code == article_code)

