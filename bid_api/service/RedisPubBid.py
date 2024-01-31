import redis
class RedisPubBid:
    
    def __init__(self) -> None:
        self.client = redis.StrictRedis(host="localhost",port=6379, db=0)
    
    def pubBid(self,channel,bid):
        response = self.client.publish(channel,bid)
        print('redis response',response)