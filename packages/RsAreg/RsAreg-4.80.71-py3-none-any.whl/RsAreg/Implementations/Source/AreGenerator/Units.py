from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UnitsCls:
	"""Units commands group definition. 6 total commands, 0 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("units", core, parent)

	# noinspection PyTypeChecker
	def get_angle(self) -> enums.UnitAngleAreg:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:ANGLe \n
		Snippet: value: enums.UnitAngleAreg = driver.source.areGenerator.units.get_angle() \n
		No command help available \n
			:return: areg_unit_agle: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:UNITs:ANGLe?')
		return Conversions.str_to_scalar_enum(response, enums.UnitAngleAreg)

	def set_angle(self, areg_unit_agle: enums.UnitAngleAreg) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:ANGLe \n
		Snippet: driver.source.areGenerator.units.set_angle(areg_unit_agle = enums.UnitAngleAreg.DEGree) \n
		No command help available \n
			:param areg_unit_agle: No help available
		"""
		param = Conversions.enum_scalar_to_str(areg_unit_agle, enums.UnitAngleAreg)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:UNITs:ANGLe {param}')

	# noinspection PyTypeChecker
	def get_doppler(self) -> enums.AregDopplerUnit:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:DOPPler \n
		Snippet: value: enums.AregDopplerUnit = driver.source.areGenerator.units.get_doppler() \n
		Defines if the radial velocity is defined as Doppler speed or frequency. \n
			:return: areg_obj_dopp_unit: SPEed| FREQuency
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:UNITs:DOPPler?')
		return Conversions.str_to_scalar_enum(response, enums.AregDopplerUnit)

	def set_doppler(self, areg_obj_dopp_unit: enums.AregDopplerUnit) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:DOPPler \n
		Snippet: driver.source.areGenerator.units.set_doppler(areg_obj_dopp_unit = enums.AregDopplerUnit.FREQuency) \n
		Defines if the radial velocity is defined as Doppler speed or frequency. \n
			:param areg_obj_dopp_unit: SPEed| FREQuency
		"""
		param = Conversions.enum_scalar_to_str(areg_obj_dopp_unit, enums.AregDopplerUnit)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:UNITs:DOPPler {param}')

	# noinspection PyTypeChecker
	def get_range(self) -> enums.UnitLengthAreg:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:RANGe \n
		Snippet: value: enums.UnitLengthAreg = driver.source.areGenerator.units.get_range() \n
		Defines the range unit. \n
			:return: areg_unit_range: M| CM| FT M Meter CM Centimeter FT Feet
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:UNITs:RANGe?')
		return Conversions.str_to_scalar_enum(response, enums.UnitLengthAreg)

	def set_range(self, areg_unit_range: enums.UnitLengthAreg) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:RANGe \n
		Snippet: driver.source.areGenerator.units.set_range(areg_unit_range = enums.UnitLengthAreg.CM) \n
		Defines the range unit. \n
			:param areg_unit_range: M| CM| FT M Meter CM Centimeter FT Feet
		"""
		param = Conversions.enum_scalar_to_str(areg_unit_range, enums.UnitLengthAreg)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:UNITs:RANGe {param}')

	# noinspection PyTypeChecker
	def get_rcs(self) -> enums.UnitRcsAreg:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:RCS \n
		Snippet: value: enums.UnitRcsAreg = driver.source.areGenerator.units.get_rcs() \n
		Defines the unit of the radar cross section. \n
			:return: areg_unit_rcs: DBSM| SM DBSM dB relative to one square meter. SM m2 (square meters) .
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:UNITs:RCS?')
		return Conversions.str_to_scalar_enum(response, enums.UnitRcsAreg)

	def set_rcs(self, areg_unit_rcs: enums.UnitRcsAreg) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:RCS \n
		Snippet: driver.source.areGenerator.units.set_rcs(areg_unit_rcs = enums.UnitRcsAreg.DBSM) \n
		Defines the unit of the radar cross section. \n
			:param areg_unit_rcs: DBSM| SM DBSM dB relative to one square meter. SM m2 (square meters) .
		"""
		param = Conversions.enum_scalar_to_str(areg_unit_rcs, enums.UnitRcsAreg)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:UNITs:RCS {param}')

	# noinspection PyTypeChecker
	def get_shift(self) -> enums.UnitShiftAreg:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:SHIFt \n
		Snippet: value: enums.UnitShiftAreg = driver.source.areGenerator.units.get_shift() \n
		No command help available \n
			:return: areg_unit_shift: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:UNITs:SHIFt?')
		return Conversions.str_to_scalar_enum(response, enums.UnitShiftAreg)

	def set_shift(self, areg_unit_shift: enums.UnitShiftAreg) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:SHIFt \n
		Snippet: driver.source.areGenerator.units.set_shift(areg_unit_shift = enums.UnitShiftAreg.HZ) \n
		No command help available \n
			:param areg_unit_shift: No help available
		"""
		param = Conversions.enum_scalar_to_str(areg_unit_shift, enums.UnitShiftAreg)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:UNITs:SHIFt {param}')

	# noinspection PyTypeChecker
	def get_speed(self) -> enums.UnitSpeedAreg:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:SPEed \n
		Snippet: value: enums.UnitSpeedAreg = driver.source.areGenerator.units.get_speed() \n
		Defines the speed unit. \n
			:return: areg_unit_speed: KMH| MPH| MPS KMH Kilometer per hour MPH Miles per Hour MPS Meter per Seconds
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:UNITs:SPEed?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSpeedAreg)

	def set_speed(self, areg_unit_speed: enums.UnitSpeedAreg) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:UNITs:SPEed \n
		Snippet: driver.source.areGenerator.units.set_speed(areg_unit_speed = enums.UnitSpeedAreg.KMH) \n
		Defines the speed unit. \n
			:param areg_unit_speed: KMH| MPH| MPS KMH Kilometer per hour MPH Miles per Hour MPS Meter per Seconds
		"""
		param = Conversions.enum_scalar_to_str(areg_unit_speed, enums.UnitSpeedAreg)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:UNITs:SPEed {param}')
