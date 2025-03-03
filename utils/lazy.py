from typing import Callable


# this is probably a mistake
class Lazy[T]:
	_inner: T = None
	_get_inner: Callable[[], T]

	def __init__(self, get_inner: Callable[[], T]):
		self._get_inner = get_inner

	def __getattr__(self, attr):
		if attr.startswith('_'):
			return super().__getattribute__(attr)
		if self._inner is None:
			self._inner = self._get_inner()
		return getattr(self._inner, attr)

	def __setattr__(self, attr, value):
		if attr.startswith('_'):
			super().__setattr__(attr, value)
			return
		if self._inner is None:
			self._inner = self._get_inner()
		setattr(self._inner, attr, value)
