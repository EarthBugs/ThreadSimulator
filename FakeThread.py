class FakeThread:
	def __init__(self, resrcs_list, index) -> None:
		self.__resrcs_list = resrcs_list.copy()
		self.__cur_resrc_passed_time = 0
		self.isactive = False
		self.index = index

	def update_time(self) -> None:
		self.__cur_resrc_passed_time += 1

	# Return a progress in percentage form.
	def get_cur_resrc_progress(self) -> int:
		return 100 * self.__cur_resrc_passed_time / self.__resrcs_list[0][1]

	def check_timeout(self) -> bool:
		# If current resrc passed time >= current resrc time, return True.
		if self.__cur_resrc_passed_time >= self.__resrcs_list[0][1]:
			return True
		# Otherwise return False.
		else:
			return False

	# Return first element
	def get_cur_resrc(self):
		return self.__resrcs_list[0][0]

	# If has next resrc, return True, otherwise return False.
	def next_resrc(self) -> bool:
		self.__resrcs_list.pop(0)
		if self.__resrcs_list:
			self.__cur_resrc_passed_time = 0
			return True
		else:
			return False
