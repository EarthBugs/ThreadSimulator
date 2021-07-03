from PySide2 import QtWidgets
from PySide2.QtCore import QTimer
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

from FakeThread import FakeThread
from ResrcSelector import ResrcSelector
from UILoader import UILoader


# Use to storage ui elements.
class UiElement:
	def __init__(self, qwidgetthread, thread_label, progress_bar, resource_label) -> None:
		self.qwidgetthread = qwidgetthread
		self.thread_label = thread_label
		self.progress_bar = progress_bar
		self.resource_label = resource_label
		self.thread = None


class ThreadSimulator:
	def __init__(self) -> None:
		self.__app = QApplication()

		self.__thread_index = 0
		self.__thread_counter = 0
		self.__thread_ui_list = list()

		self.__cpu_queue = list()
		self.__gpu_queue = list()
		self.__io_queue = list()
		self.__queue_list = list()
		self.__queue_list.append(self.__cpu_queue)
		self.__queue_list.append(self.__gpu_queue)
		self.__queue_list.append(self.__io_queue)

		self.__cpu_queue_txt = list()
		self.__gpu_queue_txt = list()
		self.__io_queue_txt = list()

		ui_file_dir = 'UI/MainGUI.ui'
		self.__ui_init(ui_file_dir)
		self.__ui.show()

		self.__timer = QTimer()
		self.__cur_time = 0
		self.__isrunning = False

		self.__bind_widgets()

		self.__app.exec_()

	def __ui_init(self, ui_file_dir) -> None:
		uiloader = UILoader(ui_file_dir)
		self.__ui = uiloader.get_ui()

		self.__app.setWindowIcon(QIcon('icon.jpg'))

		# Add all thread ui element into a list.
		thread_ui0 = UiElement(self.__ui.qwidgetthread_0, self.__ui.thread_label_0,
							   self.__ui.progress_bar_0, self.__ui.resource_label_0)
		thread_ui1 = UiElement(self.__ui.qwidgetthread_1, self.__ui.thread_label_1,
							   self.__ui.progress_bar_1, self.__ui.resource_label_1)
		thread_ui2 = UiElement(self.__ui.qwidgetthread_2, self.__ui.thread_label_2,
							   self.__ui.progress_bar_2, self.__ui.resource_label_2)
		thread_ui3 = UiElement(self.__ui.qwidgetthread_3, self.__ui.thread_label_3,
							   self.__ui.progress_bar_3, self.__ui.resource_label_3)
		thread_ui4 = UiElement(self.__ui.qwidgetthread_4, self.__ui.thread_label_4,
							   self.__ui.progress_bar_4, self.__ui.resource_label_4)
		thread_ui5 = UiElement(self.__ui.qwidgetthread_5, self.__ui.thread_label_5,
							   self.__ui.progress_bar_5, self.__ui.resource_label_5)
		self.__thread_ui_list.append(thread_ui0)
		self.__thread_ui_list.append(thread_ui1)
		self.__thread_ui_list.append(thread_ui2)
		self.__thread_ui_list.append(thread_ui3)
		self.__thread_ui_list.append(thread_ui4)
		self.__thread_ui_list.append(thread_ui5)

		for thread_ui in self.__thread_ui_list:
			thread_ui.qwidgetthread.hide()
			thread_ui.qwidgetthread.ishide = True
			thread_ui.progress_bar.setValue(0)

	# Used to bind individual widgets with functions it controls.
	def __bind_widgets(self) -> None:
		self.__ui.start_buttom.clicked.connect(self.__start_btn_handle)
		self.__ui.create_buttom.clicked.connect(self.__creat_thread)
		self.__timer.timeout.connect(self.__time_handle)

	def __start_btn_handle(self) -> None:
		# If timmer is not running, start timer.
		if self.__isrunning:
			self.__timer.stop()
			self.__isrunning = False
			self.__print_to_log('计时器暂停')
		# Otherwise, stop the timer.
		else:
			self.__timer.start(1000)
			self.__isrunning = True
			self.__print_to_log('计时器开始')

	# Call a resrc_selector to let user selece thread`s resrcs, and start a fake_thread in a real python thread. 
	def __creat_thread(self) -> bool:
		# Stop timer
		self.__timer.stop()
		self.__isrunning = False
		self.__print_to_log('计时器暂停')

		self.__print_to_log('	--------\n	开始创建进程')
		# Check if amout of thread more than 6.
		if self.__thread_counter >= 6:
			MessageBox = QtWidgets.QMessageBox()
			MessageBox.critical(self.__ui, "进程数量限制", "最多只能同时运行6个进程！")
			self.__print_to_log('进程创建中断\n--------')
			return
		else:
			# Send a resrcs_list into thread_selector, when user clicked 'create_thread' button, thread_creator will write resrcs into resrcs_list in format [resrc_type, resrc_time]
			resrcs_list = list()

			# Call a ResrcSelector
			resrc_selector = ResrcSelector(resrcs_list)
			del resrc_selector

			# Create thread
			if resrcs_list:
				# Print to log
				index = 0
				txt_temp = '		已选择资源:'
				for resrc in resrcs_list:
					txt_temp = txt_temp + '\n		资源' +str(index) + ':' + str(resrc[0]) + '，持续时间:' + str(resrc[1])
					index += 1
				self.__print_to_log(txt_temp)

				thread = FakeThread(resrcs_list, self.__thread_index)

				# Init ui
				for thread_ui in self.__thread_ui_list:
					if thread_ui.qwidgetthread.ishide == True:
						thread_ui.thread = thread
						thread_ui.thread_label.setText(
							'进程' + str(thread_ui.thread.index))
						thread_ui.resource_label.setText('正在等待：' + thread.get_cur_resrc())
						thread_ui.qwidgetthread.show()
						thread_ui.qwidgetthread.ishide = False
						break
				
				self.__thread_counter += 1

				# Add thread`s first resrc to corresponding queue.
				first_resrc = thread.get_cur_resrc()
				if first_resrc == 'CPU':
					self.__cpu_queue.append(thread)
					self.__cpu_queue_txt.append('进程' + str(self.__thread_index))
					self.__update_queue_txt()
					self.__print_to_log('		已将进程' + str(thread.index) + '添加到CPU队列，进程进入就绪态')
				if first_resrc == 'GPU':
					self.__gpu_queue.append(thread)
					self.__gpu_queue_txt.append('进程' + str(self.__thread_index))
					self.__update_queue_txt()
					self.__print_to_log('		已将进程' + str(thread.index) + '添加到GPU队列，进程进入就绪态')
				if first_resrc == 'IO':
					self.__io_queue.append(thread)
					self.__io_queue_txt.append('进程' + str(self.__thread_index))
					self.__update_queue_txt()
					self.__print_to_log('		已将进程' + str(thread.index) + '添加到IO队列，进程进入就绪态')

			else:
				MessageBox = QtWidgets.QMessageBox()
				MessageBox.critical(self.__ui, "资源选择非法", "请选择至少一个持续时间大于零的资源！")
				self.__print_to_log('	进程创建中断\n	--------')
				return

		self.__print_to_log('	已创建进程' + str(self.__thread_index) + '\n	--------')
		self.__thread_index += 1

	def __time_handle(self) -> None:
		self.__cur_time += 1

		self.__print_to_log('--------\n以下为第' + str(self.__cur_time) + '秒')

		self.__process_schedul()

		self.__ui.time_lcd.display(self.__cur_time)
		self.__ui_update()

		self.__print_to_log('以上为第' + str(self.__cur_time) + '秒\n--------')

	# Select a thread from each queue and call run thread to run it.
	def __process_schedul(self) -> None:
		# Check each queue if they are None.
		for queue in self.__queue_list:
			if queue:
				thread = queue[0]
				istimeout = self.__run_thread(thread)
				if istimeout:
					self.__resrc_end_handle(thread, queue)
				
	# Recive a thread form process schedul funtion, update thread time. If timeout, return True, otherwise return False.
	def __run_thread(self, thread) -> bool:
		self.__print_to_log('进程' + str(thread.index) + '正在使用' + str(thread.get_cur_resrc()) + '资源')

		thread.isactive = True
		istimeout = thread.check_timeout()
		if istimeout:
			return True
		else:
			thread.update_time()
			return False

	def __resrc_end_handle(self, thread, queue) -> None:
		thread.isactive = False
		queue.pop(0)

		txt_temp = ''

		# Pop first element of corresponding queue txt.
		thread_cur_resrc = thread.get_cur_resrc()
		if thread_cur_resrc == 'CPU':
			self.__cpu_queue_txt.pop(0)
			txt_temp = '进程' + str(thread.index) + '对CPU的使用结束，进入阻塞态\n'
		if thread_cur_resrc == 'GPU':
			self.__gpu_queue_txt.pop(0)
			txt_temp = '进程' + str(thread.index) + '对GPU的使用结束，进入阻塞态\n'
		if thread_cur_resrc == 'IO':
			self.__io_queue_txt.pop(0)
			txt_temp = '进程' + str(thread.index) + '对IO的使用结束，进入阻塞态\n'

		has_next_resrc = thread.next_resrc()
		if has_next_resrc:
			resrc = thread.get_cur_resrc()
			if resrc == 'CPU':
				self.__cpu_queue.append(thread)
				self.__cpu_queue_txt.append('进程' + str(self.__thread_index))
				txt_temp = txt_temp + '已将进程' + str(thread.index) + '添加到CPU队列，进程进入就绪态'
				self.__print_to_log(txt_temp)
			if resrc == 'GPU':
				self.__gpu_queue.append(thread)
				self.__gpu_queue_txt.append('进程' + str(self.__thread_index))
				txt_temp = txt_temp + '已将进程' + str(thread.index) + '添加到GPU队列，进程进入就绪态'
				self.__print_to_log(txt_temp)
			if resrc == 'IO':
				self.__io_queue.append(thread)
				self.__io_queue_txt.append('进程' + str(self.__thread_index))
				txt_temp = txt_temp + '已将进程' + str(thread.index) + '添加到IO队列，进程进入就绪态'
				self.__print_to_log(txt_temp)
		else:
			self.__kill_thread(thread)
			txt_temp = txt_temp + '进程' + str(thread.index) + '运行结束'

	def __kill_thread(self, thread) -> None:
		for thread_ui in self.__thread_ui_list:
			# Hide ui
			if thread_ui.thread == thread:
				thread_ui.thread == None
				thread_ui.qwidgetthread.hide()
				thread_ui.qwidgetthread.ishide = True
		self.__thread_counter -= 1
		self.__print_to_log('进程' + str(thread.index) + '已销毁')
		del thread

	def __ui_update(self) -> None:
		for thread_ui in self.__thread_ui_list:
			# If this qwidget is not hide, update it.
			if not thread_ui.qwidgetthread.ishide:
				resrc_txt = thread_ui.thread.get_cur_resrc()
				if thread_ui.thread.isactive:
					thread_ui.resource_label.setText('正在使用：' + resrc_txt)
				else:
					thread_ui.resource_label.setText('正在等待：' + resrc_txt)

				progress = thread_ui.thread.get_cur_resrc_progress()
				thread_ui.progress_bar.setValue(progress)
			
		self.__update_queue_txt()

	def __update_queue_txt(self) -> None:
			index = 0
			txt_temp = ''
			for line in self.__cpu_queue_txt:
				txt_temp = txt_temp + str(index) + ':' + str(line)
				if index == 0:
					txt_temp = txt_temp + '(正在运行)\n'
				else:
					txt_temp = txt_temp + '\n'
				index += 1
			self.__ui.cpu_queue_text.setText(txt_temp)

			index = 0
			txt_temp = ''
			for line in self.__gpu_queue_txt:
				txt_temp = txt_temp + str(index) + ':' + str(line)
				if index == 0:
					txt_temp = txt_temp + '(正在运行)\n'
				else:
					txt_temp = txt_temp + '\n'
				index += 1
			self.__ui.gpu_queue_text.setText(txt_temp)

			index = 0
			txt_temp = ''
			for line in self.__io_queue_txt:
				txt_temp = txt_temp + str(index) + ':' + str(line)
				if index == 0:
					txt_temp = txt_temp + '(正在运行)\n'
				else:
					txt_temp = txt_temp + '\n'
				index += 1
			self.__ui.io_queue_text.setText(txt_temp)
		
	def __print_to_log(self, log) -> None:
		self.__ui.log_text.append(log)
		self.__ui.log_text.textCursor().End
