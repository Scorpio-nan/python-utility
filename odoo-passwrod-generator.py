from passlib.context import CryptContext as _CryptContext

class CryptContext:
	def __init__(self, *args, **kwargs):
		self.__obj__ = _CryptContext(*args, **kwargs)

	@property
	def encrypt(self):
		return self.hash

	def copy(self):
		other_wrapper = CryptContext(_autoload=False)
		other_wrapper.__obj__.load(self.__obj__)
		return other_wrapper

	@property
	def hash(self):
		return self.__obj__.hash

	@property
	def identify(self):
		return self.__obj__.identify

	@property
	def verify(self):
		return self.__obj__.verify

	@property
	def verify_and_update(self):
		return self.__obj__.verify_and_update

	def schemes(self):
		return self.__obj__.schemes()

	def update(self, **kwargs):
		if kwargs.get("schemes"):
			assert isinstance(kwargs["schemes"], str) or all(isinstance(s, str) for s in kwargs["schemes"])
		return self.__obj__.update(**kwargs)

API_KEY_SIZE = 20
INDEX_SIZE = 8
KEY_CRYPT_CONTEXT = CryptContext(
	['pbkdf2_sha512'], pbkdf2_sha512__rounds=6000,
)

def generate_password(password):
	print(KEY_CRYPT_CONTEXT.encrypt(password))


generate_password('admin')
