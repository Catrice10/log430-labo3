import graphene
from graphene import ObjectType, String, Int, Float
from stocks.queries.read_stock import get_stock_by_id

class Product(ObjectType):
    id = String()
    quantity = Int()
    name = String()
    sku = String()
    price = Float()

class Query(ObjectType):       
    product = graphene.Field(Product, id=String(required=True))
    stock_level = Int(product_id=String(required=True))
    
    def resolve_product(self, info, id):
        """ Create an instance of Product based on SQLAlchemy joined data """
        stock_record = get_stock_by_id(id)
        if stock_record:
            return Product(
                id=str(stock_record.get('product_id')),
                quantity=stock_record.get('quantity'),
                name=stock_record.get('name'),
                sku=stock_record.get('sku'),
                price=stock_record.get('price')
            )
        return None
    
    def resolve_stock_level(self, product_id):
        """ Retrieve stock quantity from MySQL """
        stock_record = get_stock_by_id(product_id)
        return stock_record.get('quantity') if stock_record else 0