from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, marker_state: bool, marker=repcap.Marker.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:POWer:MARKer<CH>:STATe \n
		Snippet: driver.calculate.power.sweep.power.marker.state.set(marker_state = False, marker = repcap.Marker.Default) \n
		No command help available \n
			:param marker_state: No help available
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
		"""
		param = Conversions.bool_to_str(marker_state)
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		self._core.io.write(f'CALCulate:POWer:SWEep:POWer:MARKer{marker_cmd_val}:STATe {param}')

	def get(self, marker=repcap.Marker.Default) -> bool:
		"""SCPI: CALCulate:[POWer]:SWEep:POWer:MARKer<CH>:STATe \n
		Snippet: value: bool = driver.calculate.power.sweep.power.marker.state.get(marker = repcap.Marker.Default) \n
		No command help available \n
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
			:return: marker_state: No help available"""
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:POWer:MARKer{marker_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
