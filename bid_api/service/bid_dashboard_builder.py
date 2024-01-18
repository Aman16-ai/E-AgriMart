from farmer.models import Bid, Product
class BidDashBoardBuilder:

    def __init__(self):
        self.dashboard_data = {
            'total_bids': None,
            'average_bid_price': None,
            'base_bid_price': None,
            'highest_bid_price': None,
        }

    def set_total_bids(self, total_bids):
        self.dashboard_data['total_bids'] = total_bids
        return self

    def set_average_bid_price(self, average_bid_price):
        self.dashboard_data['average_bid_price'] = average_bid_price
        return self

    def set_base_bid_price(self, base_bid_price):
        self.dashboard_data['base_bid_price'] = base_bid_price
        return self

    def set_highest_bid_price(self, highest_bid_price):
        self.dashboard_data['highest_bid_price'] = highest_bid_price
        return self

    def set_is_current_customer_added_bid(self,status):
        if('customer' not in self.dashboard_data):
            self.dashboard_data['customer'] = {}
        self.dashboard_data['customer']['is_current_customer_added_bid'] = status
        return self
    
    def set_current_customer_bid_amount(self,bid_amount):
        self.dashboard_data['customer']['bid_amount'] = bid_amount
        return self
    def set_current_customer_profit_amount(self,profit_amount):
        self.dashboard_data['customer']['profit'] = profit_amount
        return self
    def build(self):
        return self.dashboard_data
        