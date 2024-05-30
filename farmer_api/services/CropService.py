from farmer.models import Product

class CropService:
        
    def get_all_crops_of_farmer(self,farmer):
        allProducts = Product.objects.filter(farmer=farmer)
        return allProducts