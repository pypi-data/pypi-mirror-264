from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPyCls:
	"""InputPy commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inputPy", core, parent)

	def get_nom_gain(self) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:INPut:NOMGain \n
		Snippet: value: float = driver.source.areGenerator.channel.inputPy.get_nom_gain() \n
		No command help available \n
			:return: areg_chan_nom_gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:INPut:NOMGain?')
		return Conversions.str_to_float(response)

	def set_nom_gain(self, areg_chan_nom_gain: float) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:INPut:NOMGain \n
		Snippet: driver.source.areGenerator.channel.inputPy.set_nom_gain(areg_chan_nom_gain = 1.0) \n
		No command help available \n
			:param areg_chan_nom_gain: No help available
		"""
		param = Conversions.decimal_value_to_str(areg_chan_nom_gain)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:CHANnel:INPut:NOMGain {param}')

	def get_rel_level(self) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:INPut:RELLevel \n
		Snippet: value: float = driver.source.areGenerator.channel.inputPy.get_rel_level() \n
		No command help available \n
			:return: areg_chan_rel_lev: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:INPut:RELLevel?')
		return Conversions.str_to_float(response)
