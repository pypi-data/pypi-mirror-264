from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AreGeneratorCls:
	"""AreGenerator commands group definition. 31 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("areGenerator", core, parent)

	@property
	def channel(self):
		"""channel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def object(self):
		"""object commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_object'):
			from .Object import ObjectCls
			self._object = ObjectCls(self._core, self._cmd_group)
		return self._object

	@property
	def osetup(self):
		"""osetup commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_osetup'):
			from .Osetup import OsetupCls
			self._osetup = OsetupCls(self._core, self._cmd_group)
		return self._osetup

	@property
	def radar(self):
		"""radar commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_radar'):
			from .Radar import RadarCls
			self._radar = RadarCls(self._core, self._cmd_group)
		return self._radar

	@property
	def units(self):
		"""units commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_units'):
			from .Units import UnitsCls
			self._units = UnitsCls(self._core, self._cmd_group)
		return self._units

	def clone(self) -> 'AreGeneratorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AreGeneratorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
