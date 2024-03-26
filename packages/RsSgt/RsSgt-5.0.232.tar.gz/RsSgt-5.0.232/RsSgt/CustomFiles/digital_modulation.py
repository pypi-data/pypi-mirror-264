from ..Internal import Core

from typing import List
from math import ceil
from datetime import datetime


class DigitalModulation:
	"""Class containing utilities to operate digital modulation files - creation and transfer to the instrument"""

	def __init__(self, core: Core):
		self._core = core

	def send_waveform_file_to_instrument(self, wv_file_path, instr_file_path):
		"""Same as send_file_from_pc_to_instrument()"""
		cmd = f"MMEM:DATA '{instr_file_path}',"
		self._core.io.write_bin_block_from_file(cmd, wv_file_path)

	@staticmethod
	def _get_wv_file_tag(content: str) -> str:
		"""Returns the tag surrounded by exactly one pair of curly brackets"""
		content = content.lstrip('{').rstrip('}')
		content = '{' + content + '}'
		return content

	@staticmethod
	def create_datalist_file(logical_pattern: List[bool], out_datalist_file_path: str, comment: str = '', copyrights: str = '') -> None:
		"""Creates an R&S dalist file for a custom digital modulation
		:param logical_pattern: List of boolean bits
		:param out_datalist_file_path: Path where to save the created file
		:param comment: Comment for the datalist file
		:param copyrights: Copyright for the datalist file"""

		pattern_len = len(logical_pattern)
		# Determine overall number of bytes - 8 bits per byte.
		req_bytes_len = ceil(pattern_len / 8)

		# The number of bytes must be the multiple of 4 - the rest is filled with zeroes.
		coerced_data_len = req_bytes_len
		if req_bytes_len % 4 > 0:
			coerced_data_len += 4 - (req_bytes_len % 4)

		# Open new waveform file for writing as text
		with open(out_datalist_file_path, 'w') as file:
			# Write waveform file header
			# The tags TYPE, CLOCK, LEVEL OFFS and WAVEFORM are mandatory for each
			# waveform. All other tags are optional and can be inserted after the TYPE tag in
			# arbitrary order. The waveform data tag must be the final one.
			file.write(DigitalModulation._get_wv_file_tag('{TYPE:SMU-DL}'))
			file.write(DigitalModulation._get_wv_file_tag(f'COMMENT:{comment}'))
			file.write(DigitalModulation._get_wv_file_tag(f'COPYRIGHT:{copyrights}'))
			file.write(DigitalModulation._get_wv_file_tag(f'DATE:{datetime.now().strftime("%Y-%m-%d;%H:%M:%S")}'))
			file.write(DigitalModulation._get_wv_file_tag(f'DATA BITLENGTH:{pattern_len}'))
			file.write('{DATA LIST-')
			file.write(f'{coerced_data_len + 1}:#')

		# Payload as binary data
		with open(out_datalist_file_path, 'ab') as file:
			ix = 0
			for i in range(coerced_data_len):
				num = 0
				multiplicator = 128
				for b in range(8):
					if ix < pattern_len:
						if logical_pattern[ix]:
							num += multiplicator
					multiplicator = multiplicator >> 1
					ix += 1
				file.write(num.to_bytes(1, 'little'))

			# Tag curly bracket at the end
			file.write(b'}')

	def sync_from(self, source: 'DigitalModulation') -> None:
		"""Synchronises these ArbFiles with the source."""
