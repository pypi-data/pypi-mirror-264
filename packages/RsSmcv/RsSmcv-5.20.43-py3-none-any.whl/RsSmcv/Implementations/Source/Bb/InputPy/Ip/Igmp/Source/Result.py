from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ResultCls:
	"""Result commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("result", core, parent)

	def get(self, ipVersion=repcap.IpVersion.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:INPut:IP<CH>:IGMP:[SOURce]:RESult \n
		Snippet: value: str = driver.source.bb.inputPy.ip.igmp.source.result.get(ipVersion = repcap.IpVersion.Default) \n
		Queries the result of pinging the source address. See [:SOURce<hw>]:BB:INPut:IP<ch>:IGMP[:SOURce]:PING. \n
			:param ipVersion: optional repeated capability selector. Default value: Nr4 (settable in the interface 'Ip')
			:return: ping_result: string Returns ping messages."""
		ipVersion_cmd_val = self._cmd_group.get_repcap_cmd_value(ipVersion, repcap.IpVersion)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:INPut:IP{ipVersion_cmd_val}:IGMP:SOURce:RESult?')
		return trim_str_response(response)
