from abc import abstractmethod
from typing import Protocol, Any, Self, runtime_checkable, Type

import msgspec


@runtime_checkable
class Msg[T](Protocol):
	@abstractmethod
	def enc(self) -> T:
		...

	@classmethod
	@abstractmethod
	def dec(cls, val: T) -> Self:
		...


def enc_hook(obj: Any) -> Any:
	if obj is not None and issubclass(type(obj), Msg):
		return obj.enc()
	else:
		# Raise a NotImplementedError for other types
		raise NotImplementedError(f"Objects of type {type(obj)} are not supported")


def dec_hook(t: Type, obj: Any) -> Any:
	if obj is not None and issubclass(t, Msg):
		return t.dec(obj)
	else:
		# Raise a NotImplementedError for other types
		raise NotImplementedError(f"Objects of type {type(obj)} are not supported")


def enc() -> msgspec.json.Encoder:
	return msgspec.json.Encoder(enc_hook=enc_hook)


def dec(val: Type) -> msgspec.json.Decoder:
	return msgspec.json.Decoder(val, dec_hook=dec_hook)
