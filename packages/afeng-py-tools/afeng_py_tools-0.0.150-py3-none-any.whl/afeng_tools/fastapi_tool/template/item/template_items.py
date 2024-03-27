from typing import Optional, Any

from afeng_tools.pydantic_tool.model.common_models import LinkItem, EnumItem
from pydantic import BaseModel, Field

from afeng_tools.fastapi_tool.template.item import CalendarDataItem, AppinfoDataItem, Error501DataItem, \
    Error500DataItem, Error404DataItem


class TemplateHtmlHeadData(BaseModel):
    """模板head信息"""
    # 标题
    title: str
    # 描述
    description: Optional[str] = None
    # 关键字
    keyword_list: Optional[list[str]] = []
    # 作者
    author: Optional[str] = Field(default='chentiefeng')
    # favicon图标
    favicon: Optional[str] = Field(default='/favicon.ico')
    # 域信息
    origin: Optional[str] = None


class TemplateBreadCrumbData(BaseModel):
    """面包屑信息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 标题
    page_title: Optional[str] = None
    # 面包屑列表
    bread_crumb_list: Optional[list[LinkItem]] = None


class TemplateLeftNavData(BaseModel):
    """左侧链接信息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 链接列表
    link_list: Optional[list[LinkItem]] = None


class TemplatePaginationAreaData(BaseModel):
    """分页信息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 上一页按钮
    pre_btn: Optional[LinkItem] = None
    # 下一页按钮
    next_btn: Optional[LinkItem] = None
    # 中间数据按钮
    data_list: Optional[list[LinkItem]] = []
    # 总数量
    total_count: Optional[int] = 0
    # 总页数
    total_page: Optional[int] = 0
    # 跳转到某页的地址
    jump_href: Optional[str] = None
    # 跳转页面时附加的数据数据字典
    jump_data_dict: Optional[dict[str, Any]] = None


class TemplatePageFooterData(BaseModel):
    """页面底部链息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 友情链接标题
    friendly_link_title: Optional[LinkItem] = LinkItem(title='友情链接', href='/article/help/friendly_link')
    # 联系信息，如：QQ: 1640125562， 邮箱：imafengbook@aliyun.com
    contact_info: Optional[str] = None
    # 友情链接列表
    friendly_link_list: Optional[list[LinkItem]] = None
    # 底部链接列表
    footer_link_list: Optional[list[LinkItem]] = None
    # 版权链接
    copyright_link: Optional[LinkItem] = LinkItem(title='阿锋', href='/')
    # ICP备案信息，如：京ICP备2023032898号-1 京公网安备xxxx号
    icp_record_info: Optional[str] = None
    # 公安备案信息，如：京公网安备11000002000001号
    police_record_info: Optional[str] = None
    # 公安备案号：11000002000001
    police_record_code: Optional[str] = None


class TemplateTopBarData(BaseModel):
    """页面顶部top bar链息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 应用链接列表
    app_link_list: Optional[list[LinkItem]] = None
    # 微信公众号图片
    weixin_qr_code_image: Optional[str] = '/static/image/qrcode/wx_of_qrcode.jpg'
    # 快捷链接列表
    quick_link_list: Optional[list[LinkItem]] = None


class TemplateLogoSearchData(BaseModel):
    """页面顶部logo search链息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # logo图片
    logo_image: Optional[str] = '/image/logo/logo.png'
    # 应用标题, 如：阿锋书屋
    app_title: Optional[str] = None
    # 查询表单提交url
    search_form_submit_url: Optional[str] = '/search'
    # 查询选项名称， 如：search_type
    search_select_type_name: Optional[str] = 'search_type'
    # 查询选项列表
    search_select_option_list: Optional[list[EnumItem]] = None


class TemplateFixNavData(BaseModel):
    """页面顶部fix nav链息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 类型链接列表
    type_link_list: Optional[list[LinkItem]] = None
    # 热点链接列表
    hotspot_link_list: Optional[list[LinkItem]] = None


class TemplatePageHeaderData(BaseModel):
    """页面顶部链息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # topbar数据
    topbar_data: TemplateTopBarData = TemplateTopBarData()
    # logo search数据
    logo_search_data: TemplateLogoSearchData = TemplateLogoSearchData()
    # fix nav数据
    fix_nav_data: TemplateFixNavData = TemplateFixNavData()


class TemplateIndexPageHeaderData(BaseModel):
    """页面顶部链息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 应用链接列表
    app_link_list: Optional[list[LinkItem]] = None
    # 微信公众号图片
    weixin_qr_code_image: Optional[str] = '/static/image/qrcode/wx_of_qrcode.jpg'
    # 快捷链接列表
    quick_link_list: Optional[list[LinkItem]] = None
    # 全部类型列表
    all_type_list: Optional[list[LinkItem]] = None


class TemplatePageSearchHeaderData(BaseModel):
    """页面搜索顶部链息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 微信公众号图片
    weixin_qr_code_image: Optional[str] = '/static/image/qrcode/wx_of_qrcode.jpg'
    # 快捷链接列表
    quick_link_list: Optional[list[LinkItem]] = None
    # 查询关键字
    keyword: Optional[str] = None
    # 搜索模式
    search_model_list: Optional[list[EnumItem]] = None
    # 搜索类型
    search_type_list: Optional[list[EnumItem]] = None


class TemplateResultListData(BaseModel):
    """页面结果列表链息"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 结果值列表
    data_list: Optional[list[Any]] = None
    # 没有数据时的html代码
    none_html_code: Optional[str] = '暂无数据！'


class TemplateGroupListData(BaseModel):
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 查询提交url
    search_url: Optional[str] = None
    # 查询输入框placeholder
    search_placeholder: Optional[str] = None
    # 搜索值
    search_value: Optional[str] = None
    # 数据列表
    data_list: Optional[list[LinkItem]] = None


class TemplateTagListData(BaseModel):
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 查询提交url
    search_url: Optional[str] = None
    # 查询输入框placeholder
    search_placeholder: Optional[str] = None
    # 搜索值
    search_value: Optional[str] = None
    # 数据列表
    data_list: Optional[list[LinkItem]] = None


class TemplateFilterTypeAreaData(BaseModel):
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 数据列表
    data_list: Optional[list[LinkItem]] = None


class TemplateDayCalendarData(BaseModel):
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 标题
    title: Optional[str] = None
    # 初始日期
    init_date: Optional[str] = None
    # 数据列表
    data_list: Optional[list[CalendarDataItem]] = None


class TemplateTabPanelItem(BaseModel):
    # 是否激活
    is_active: Optional[bool] = False
    # 编码
    code: Optional[str] = None
    # 标题
    title: Optional[str] = None
    # html内容
    html: Optional[str] = None


class TemplateTabPanelData(BaseModel):
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 查看更多的按钮
    more_btn: Optional[LinkItem] = None
    # 子项列表
    item_list: Optional[list[TemplateTabPanelItem]] = None


class TemplateTopRankingData(BaseModel):
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 标题
    title: Optional[str] = None
    # 数据列表
    data_list: Optional[list[LinkItem]] = None


class TemplateRedirectDownloadAreaData(BaseModel):
    """下载区域数据"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 应用信息
    app_info: Optional[AppinfoDataItem] = None
    # 文件名
    file_name: Optional[str] = None
    # 广告列表
    ad_list: Optional[list[LinkItem]] = None
    # 下载链接
    download_url: Optional[str] = None
    # 返回链接
    back_url: Optional[str] = '/'


class TemplateRedirectAreaData(BaseModel):
    """重定向区域数据"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 应用信息
    app_info: Optional[AppinfoDataItem] = None
    # 广告列表
    ad_list: Optional[list[LinkItem]] = None
    # 跳转链接
    redirect_url: Optional[str] = None
    # 返回链接
    back_url: Optional[str] = '/'


class TemplateError404AreaData(Error404DataItem):
    """错误404数据"""
    # 是否是移动端
    is_mobile: Optional[bool] = False


class TemplateError500AreaData(Error500DataItem):
    """错误500数据"""
    # 是否是移动端
    is_mobile: Optional[bool] = False


class TemplateError501AreaData(Error501DataItem):
    """错误501数据"""
    # 是否是移动端
    is_mobile: Optional[bool] = False

