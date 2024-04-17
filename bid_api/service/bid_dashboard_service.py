from farmer.models import Bid, Product
from account.models import UserProfile
from .bid_dashboard_builder import BidDashBoardBuilder
class BidDashBoardService:

    def __init__(self,product_id,user) -> None:
        self.crop = Product.objects.get(pk=product_id)
        self.user = UserProfile.objects.get(user=user)
        self.builder = BidDashBoardBuilder()

    def getDashBoardData(self):
        total_bids = self.crop.get_totalBids()
        average_bid_price = self.crop.get_averageBidPrice()
        base_price = self.crop.price
        highest_bid_price = self.crop.get_heighest_bid_price()
        self.builder\
            .set_total_bids(total_bids)\
            .set_average_bid_price(average_bid_price)\
            .set_base_bid_price(base_price)\
            .set_highest_bid_price(highest_bid_price)
        
        if(self.user.user_type == 'Customer'):
            customer_bid = Bid.get_customer_lastest_bid(self.user,self.crop)
            print('customer bid ------> ',customer_bid)
            if(customer_bid != None):
                self.builder\
                    .set_is_current_customer_added_bid(Bid.is_current_customer_added(self.user,self.crop))\
                    .set_current_customer_bid_amount(customer_bid.bid_price)\
                    .set_current_customer_profit_amount(customer_bid.profit)
            else:
                self.builder\
                    .set_is_current_customer_added_bid(False)
            
        return self.builder.build()
    