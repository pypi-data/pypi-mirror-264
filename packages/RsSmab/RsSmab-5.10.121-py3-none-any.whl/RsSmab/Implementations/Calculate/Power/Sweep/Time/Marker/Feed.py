from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FeedCls:
	"""Feed commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("feed", core, parent)

	def set(self, marker_binding: enums.MeasRespTimeGate, marker=repcap.Marker.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:MARKer<CH>:FEED \n
		Snippet: driver.calculate.power.sweep.time.marker.feed.set(marker_binding = enums.MeasRespTimeGate.TRAC1, marker = repcap.Marker.Default) \n
		No command help available \n
			:param marker_binding: No help available
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
		"""
		param = Conversions.enum_scalar_to_str(marker_binding, enums.MeasRespTimeGate)
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		self._core.io.write(f'CALCulate:POWer:SWEep:TIME:MARKer{marker_cmd_val}:FEED {param}')

	# noinspection PyTypeChecker
	def get(self, marker=repcap.Marker.Default) -> enums.MeasRespTimeGate:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:MARKer<CH>:FEED \n
		Snippet: value: enums.MeasRespTimeGate = driver.calculate.power.sweep.time.marker.feed.get(marker = repcap.Marker.Default) \n
		No command help available \n
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
			:return: marker_binding: No help available"""
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:MARKer{marker_cmd_val}:FEED?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTimeGate)
