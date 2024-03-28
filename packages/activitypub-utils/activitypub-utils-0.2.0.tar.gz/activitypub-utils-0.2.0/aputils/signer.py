from __future__ import annotations

import typing

from functools import wraps
from pathlib import Path
from urllib.request import Request
from Crypto.PublicKey import RSA, ECC

from . import algorithms
from .enums import AlgorithmType, KeyType
from .errors import SignatureFailureError
from .misc import Signature

try:
	from aiohttp.web import BaseRequest as AiohttpRequest

except ImportError:
	AiohttpRequest = None

if typing.TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any


def _check_private(func: Callable) -> Callable:
	"Checks if the key is a private key before running a method"

	@wraps(func)  # noqa: ANN201
	def wrapper(key: Signer, *args: Any, **kwargs: Any) -> Any:
		if not key.is_private:
			raise TypeError(f"Cannot use method '{func.__name__}' on Signer with public key")

		return func(key, *args, **kwargs)
	return wrapper


def _check_key_type(*types: KeyType | str) -> Callable:
	"Checks if the key is the correct type before running the method"

	types = tuple(KeyType.parse(type) for type in types)

	def outer(func: Callable):
		@wraps(func)  # noqa: ANN201
		def wrapper(signer: Signer, *args: Any, **kwargs: Any) -> Callable:
			if signer.type not in types:
				method = func.__name__
				alg = signer.type.value

				raise TypeError(f"Cannot use method '{method}' on Signer with {alg} key")

			return func(signer, *args, **kwargs)
		return wrapper
	return outer


class Signer:
	"Used to sign or verify HTTP headers"

	__test_mode: bool = False
	__slots__: tuple[str, ...] = ("key", "keyid")


	def __init__(self, key: str | Path | ECC.EccKey | RSA.RsaKey, keyid: str) -> None:
		"""
			Create a new signer object. The key can be an ``RsaKey`` object, ``str``, or ``Path`` to
			an exported key

			:param key: RSA or ECC key to use for signing or verifying
			:param keyid: Url to a web resource which hosts the public key
		"""

		self.key: ECC.EccKey | RSA.RsaKey = key # type: ignore
		"Key to use for signing or verifying"

		self.keyid: str = keyid
		"Url to a web resource which hosts the public key"


	def __repr__(self) -> str:
		if self.type == KeyType.RSA:
			return f"{self.__class__.__name__}(type='RSA', bits={self.bits}, keyid='{self.keyid}')"

		return f"{self.__class__.__name__}(type='ECC', keyid='{self.keyid}')"


	def __setattr__(self, key: str, value: Any) -> None:
		if key == "key":
			if isinstance(value, Path):
				with value.open("r") as fd:
					value = fd.read()

			if isinstance(value, str):
				if not value.startswith("-"):
					with Path(value).expanduser().resolve().open("r", encoding = "utf-8") as fd:
						value = fd.read()

				try:
					value = RSA.import_key(value)

				except ValueError:
					value = ECC.import_key(value)

					if value.curve != "Ed25519":
						msg = "Invalid ECC key. Only the Ed25519 curve is supported."
						raise TypeError(msg) from None

			elif not isinstance(value, (ECC.EccKey, RSA.RsaKey)):
				msg = "Key must be an RsaKey, EccKey, Path, or a string representation of a key"
				raise TypeError(msg)

		object.__setattr__(self, key, value)


	@classmethod
	def new(cls: type[Signer],
			keyid: str,
			keytype: KeyType = KeyType.RSA,
			size: int = 4096) -> Signer:
		"""
			Create a new signer with a generated ``RsaKey`` of the specified size

			:param keyid: Url to a web resource which hosts the public key
			:param keytype: Type of private key to generate
			:param size: Size of RSA key in bits to generate. This is ignore for ECC keys.
		"""

		keytype = KeyType.parse(keytype)

		if keytype == KeyType.RSA:
			return cls(RSA.generate(size), keyid)

		if keytype == KeyType.ECC:
			return cls(ECC.generate(curve="Ed25519"), keyid)

		raise TypeError(f"Invalid key type: {keytype}")


	@classmethod
	def new_from_actor(cls: type[Signer], actor: dict[str, Any]) -> Signer:
		"""
			Create a signer object from an ActivityPub actor dict

			:param dict actor: ActivityPub Actor object
		"""

		return cls(actor["publicKey"]["publicKeyPem"], actor["publicKey"]["id"])


	@property
	@_check_key_type(KeyType.RSA)
	def bits(self) -> int:
		"Size of the RSA key in bits"
		return self.key.size_in_bits() # type: ignore


	@property
	def is_private(self) -> bool:
		"Return ``True`` if the key is private"
		return self.key.has_private()


	@property
	def type(self) -> KeyType:
		"Algorithm used to generate the key"
		if isinstance(self.key, ECC.EccKey):
			return KeyType.ECC

		if isinstance(self.key, RSA.RsaKey):
			return KeyType.RSA

		raise TypeError(f"Invalid key type: {self.key.__class__.__name__}")


	@property
	@_check_private
	def pubkey(self) -> str:
		"Export the public key to a str"
		key_data = self.key.public_key().export_key(format="PEM")
		return key_data.decode("utf-8") if isinstance(key_data, bytes) else key_data


	def export(self, path: Path | str | None = None) -> str:
		"""
			Export the key to a str

			:param path: Path to dump the key in text form to if specified
		"""
		key_data = self.key.export_key(format = "PEM")
		key = key_data.decode("utf-8") if isinstance(key_data, bytes) else key_data

		if path:
			path = Path(path)

			with path.open("w", encoding = "utf-8") as fd:
				fd.write(key)

		return key


	@_check_private
	def sign_headers(self,
					method: str,
					url: str,
					data: dict[str, Any] | bytes | str | None = None,
					headers: dict[str, str] | None = None,
					algorithm: AlgorithmType = AlgorithmType.HS2019,
					sign_all: bool = False) -> dict[str, Any]:
		"""
			Generate a signature and return the headers with a "Signature" key

			Note: HS2019 is the only supported algorithm, so only use others when you absolutely
			have to

			:param method: HTTP method of the request
			:param url: URL of the request
			:param data: ActivityPub message for a POST request
			:param headers: Request headers
			:param algorithm: Type of algorithm to use for hashing the headers. HS2019 is the only
				non-deprecated algorithm.
			:param sign_all: If ``True``, sign all headers instead of just the required ones
		"""

		algo = algorithms.get(algorithm)(self)
		headers = headers or {}
		used_headers = tuple([]) if not sign_all else tuple(headers)
		return algo.sign_headers(method, url, headers, used_headers, data)


	@_check_private
	def sign_request(self, request: Request, algorithm: AlgorithmType = AlgorithmType.HS2019) -> Any:
		"""
			Convenience function to sign a request. Support for more Request classes planned.

			:param request: Request object to sign
			:param algorithm: Type of algorithm to use for signing and hashing the headers. HS2019
				is the only non-deprecated algorithm.

			:raises TypeError: If the Request class is not supported
		"""

		# sign built-in request class
		if isinstance(request, Request):
			request_headers = dict(request.header_items())
			headers = self.sign_headers(
				request.get_method().upper(),
				request.full_url, request.data,
				request_headers,
				algorithm = algorithm
			)

			request.headers = {key.title(): value for key, value in headers.items()}

		else:
			raise TypeError(f"Request from module not supported: {type(request).__module__}")

		return request


	def validate_signature(self,
						method: str,
						path: str,
						headers: dict[str, Any],
						body: bytes | str | None = None) -> bool:
		"""
			Check to make sure the Signature and Digest headers match

			:param method: Request method
			:param path: Request path
			:param headers: Request headers
			:param body: Request body if it exists

			:raises aputils.SignatureFailureError: When any step of the validation process fails
		"""

		if not (signature := Signature.new_from_headers(headers)):
			raise SignatureFailureError("Missing 'signature' header")

		keys = tuple(key.lower() for key in headers)

		for key in signature.headers:
			if not key.startswith("(") and key not in keys:
				raise SignatureFailureError(f"Header key does not exist: {key}")

		algo = algorithms.get(signature.algorithm)(self)

		if not algo.verify_headers(method, path, headers, signature, body):
			raise SignatureFailureError("Failed to verify signature")

		return True


	if AiohttpRequest is not None:
		async def validate_aiohttp_request(self, request: AiohttpRequest) -> bool:
			"""
				Validate the signature header of an AIOHTTP server request object

				:param request: AioHttp server request to validate
			"""

			return self.validate_signature(
				request.method,
				request.path,
				request.headers,
				await request.read()
			)
