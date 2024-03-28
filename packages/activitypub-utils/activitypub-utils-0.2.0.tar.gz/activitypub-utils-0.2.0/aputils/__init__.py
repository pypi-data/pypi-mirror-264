__version__ = "0.2.0"

from .algorithms import Algorithm, HS2019, RsaSha256
from .algorithms import get as get_algorithm, register as register_algorithm
from .errors import InvalidKeyError, SignatureFailureError
from .message import Attachment, Message, Property
from .misc import Digest, HttpDate, JsonBase, MessageDate, Signature
from .objects import HostMeta, HostMetaJson, Nodeinfo, Webfinger, WellKnownNodeinfo
from .enums import (
	Enum,
	IntEnum,
	StrEnum,
	AlgorithmType,
	KeyType,
	NodeinfoProtocol,
	NodeinfoServiceInbound,
	NodeinfoServiceOutbound,
	NodeinfoVersion,
	ObjectType
)

try:
	from .signer import Signer

except ImportError:
	Signer = None # type: ignore
