from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)

	def get_nom_gain(self) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:OUTPut:NOMGain \n
		Snippet: value: float = driver.source.areGenerator.channel.output.get_nom_gain() \n
		No command help available \n
			:return: areg_chan_nom_gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:OUTPut:NOMGain?')
		return Conversions.str_to_float(response)

	def set_nom_gain(self, areg_chan_nom_gain: float) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:OUTPut:NOMGain \n
		Snippet: driver.source.areGenerator.channel.output.set_nom_gain(areg_chan_nom_gain = 1.0) \n
		No command help available \n
			:param areg_chan_nom_gain: No help available
		"""
		param = Conversions.decimal_value_to_str(areg_chan_nom_gain)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:CHANnel:OUTPut:NOMGain {param}')
