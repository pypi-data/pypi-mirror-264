from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PixelCls:
	"""Pixel commands group definition. 6 total commands, 0 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pixel", core, parent)

	def set_color(self, pix_test_color: enums.PixelTestPredefined) -> None:
		"""SCPI: TEST:PIXel:COLor \n
		Snippet: driver.test.pixel.set_color(pix_test_color = enums.PixelTestPredefined.AUTO) \n
		No command help available \n
			:param pix_test_color: No help available
		"""
		param = Conversions.enum_scalar_to_str(pix_test_color, enums.PixelTestPredefined)
		self._core.io.write(f'TEST:PIXel:COLor {param}')

	def get_gradient(self) -> bool:
		"""SCPI: TEST:PIXel:GRADient \n
		Snippet: value: bool = driver.test.pixel.get_gradient() \n
		No command help available \n
			:return: pix_test_grad_stat: No help available
		"""
		response = self._core.io.query_str('TEST:PIXel:GRADient?')
		return Conversions.str_to_bool(response)

	def set_gradient(self, pix_test_grad_stat: bool) -> None:
		"""SCPI: TEST:PIXel:GRADient \n
		Snippet: driver.test.pixel.set_gradient(pix_test_grad_stat = False) \n
		No command help available \n
			:param pix_test_grad_stat: No help available
		"""
		param = Conversions.bool_to_str(pix_test_grad_stat)
		self._core.io.write(f'TEST:PIXel:GRADient {param}')

	def get_point_size(self) -> int:
		"""SCPI: TEST:PIXel:POINtsize \n
		Snippet: value: int = driver.test.pixel.get_point_size() \n
		No command help available \n
			:return: pix_test_grad_stat: No help available
		"""
		response = self._core.io.query_str('TEST:PIXel:POINtsize?')
		return Conversions.str_to_int(response)

	def set_point_size(self, pix_test_grad_stat: int) -> None:
		"""SCPI: TEST:PIXel:POINtsize \n
		Snippet: driver.test.pixel.set_point_size(pix_test_grad_stat = 1) \n
		No command help available \n
			:param pix_test_grad_stat: No help available
		"""
		param = Conversions.decimal_value_to_str(pix_test_grad_stat)
		self._core.io.write(f'TEST:PIXel:POINtsize {param}')

	def get_rgba(self) -> List[int]:
		"""SCPI: TEST:PIXel:RGBA \n
		Snippet: value: List[int] = driver.test.pixel.get_rgba() \n
		No command help available \n
			:return: pixel_test_rgba: No help available
		"""
		response = self._core.io.query_bin_or_ascii_int_list('TEST:PIXel:RGBA?')
		return response

	def set_rgba(self, pixel_test_rgba: List[int]) -> None:
		"""SCPI: TEST:PIXel:RGBA \n
		Snippet: driver.test.pixel.set_rgba(pixel_test_rgba = [1, 2, 3]) \n
		No command help available \n
			:param pixel_test_rgba: No help available
		"""
		param = Conversions.list_to_csv_str(pixel_test_rgba)
		self._core.io.write(f'TEST:PIXel:RGBA {param}')

	def get_text(self) -> bool:
		"""SCPI: TEST:PIXel:TEXT \n
		Snippet: value: bool = driver.test.pixel.get_text() \n
		No command help available \n
			:return: pix_test_grad_stat: No help available
		"""
		response = self._core.io.query_str('TEST:PIXel:TEXT?')
		return Conversions.str_to_bool(response)

	def set_text(self, pix_test_grad_stat: bool) -> None:
		"""SCPI: TEST:PIXel:TEXT \n
		Snippet: driver.test.pixel.set_text(pix_test_grad_stat = False) \n
		No command help available \n
			:param pix_test_grad_stat: No help available
		"""
		param = Conversions.bool_to_str(pix_test_grad_stat)
		self._core.io.write(f'TEST:PIXel:TEXT {param}')

	def set_window(self, pix_test_window: bool) -> None:
		"""SCPI: TEST:PIXel:WINDow \n
		Snippet: driver.test.pixel.set_window(pix_test_window = False) \n
		No command help available \n
			:param pix_test_window: No help available
		"""
		param = Conversions.bool_to_str(pix_test_window)
		self._core.io.write(f'TEST:PIXel:WINDow {param}')
