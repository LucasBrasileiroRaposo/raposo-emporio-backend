from singleton.Singleton import Singleton
from business.batch.BatchService import BatchService
from business.user.UserService import UserService
from entity.product.ProductRepository import ProductRepository
from entity.product.Product import Product
from dtos.product.ProductRegisterDTO import ProductRegisterDTO
from dtos.product.ProductRegisteredDTO import ProductRegisteredDTO
from dtos.product.ProductUpdateDTO import ProductUpdateDTO

class ProductService(Singleton):

    ADMIN_USER_ROLE = 'ADMIN'

    def __init__(self):
        self.batch_service = BatchService()
        self.user_service = UserService()
        self.product_repository = ProductRepository()

    def register_product(self, product: ProductRegisterDTO, requester_id: int):
        self.user_service.check_user_permission(requester_id, [self.ADMIN_USER_ROLE])
        if len(self.product_repository.find_by_name_or_code([product.name], [product.code])) != 0:
            raise Exception('Product already registered')

        new_product = Product(
            name=product.name,
            description=product.description,
            code=product.code,
            category=product.category,
            base_price=product.base_price,
            image_url=product.image_url,
            is_active=product.is_active
        )

        saved_product = ProductRegisteredDTO(self.product_repository.save(new_product))

        try:
            if product.batches:
                saved_product.batches = self.batch_service.register_batch(product.batches, saved_product.id, requester_id)
        except Exception as e:
            self.delete_product(product_id=saved_product.id, requester_id=requester_id)
            raise Exception(f'Error registering batches: {str(e)}')

        return saved_product

    def get_products(self):
        products = self.product_repository.find_all()
        return [ProductRegisteredDTO(product).deserialize() for product in products]

    def get_product_by_id(self, product_id: int):
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise Exception('Product not found')
        return product

    def update_product(self, product_id: int, product: ProductUpdateDTO, requester_id: int):
        self.user_service.check_user_permission(requester_id, [self.ADMIN_USER_ROLE])
        product_found = self.product_repository.find_by_id(product_id)
        if not product_found:
            raise Exception('Product not found')

        product_found.name = (product.name if product.name else product_found.name)
        product_found.description = (product.description if product.description else product_found.description)
        product_found.code = (product.code if product.code else product_found.code)
        product_found.category = (product.category if product.category else product_found.category)
        product_found.base_price = (product.base_price if product.base_price else product_found.base_price)
        product_found.image_url = (product.image_url if product.image_url else product_found.image_url)
        product_found.is_active = (product.is_active if product.is_active!=None else product_found.is_active)

        return self.product_repository.save(product_found)

    def delete_product(self, product_id: int, requester_id: int):
        self.user_service.check_user_permission(requester_id, [self.ADMIN_USER_ROLE])
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise Exception('Product not found')
        return self.product_repository.delete(product_id)