import akshare as ak
class AkShare:
    """_summary_
    文档: https://akshare.akfamily.xyz/introduction.html
    更新: pip install akshare --upgrade -i https://pypi.org/simple

    """
    def __init__(self) -> None:
        pass
    
    def get_stock_zh_a_spot(self):
        """_summary_
        获取A股实时行情数据
        """
        return ak.stock_zh_a_spot()
    

    def get_futures_hog_supply(self):
        """_summary_
        获取生猪行情数据
        """

        futures_hog_supply_df = ak.futures_hog_supply(symbol="猪肉批发价")
        print(futures_hog_supply_df)
        return futures_hog_supply_df
