from functools import partial

from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from UILoader import UILoader


class ResrcSelector(QtWidgets.QDialog):
    def __init__(self, resource_list) -> None:
        super(ResrcSelector, self).__init__()

        __ui_file_dir = 'UI/ThreadCreator.ui'
        __uiloader = UILoader(__ui_file_dir)
        self.__ui = __uiloader.get_ui()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.__ui)
        self.setLayout(self.layout)
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)

        self.resource_list = resource_list

        self.__bind_widgets()

        self.exec_()

    # Write selected resources into resource_list.
    def write_data(self) -> None:
        # Determine whether the element is hidden.
        index = 0
        for element in self.__resource_element:
            # If it is hidden or its time is 0, skip.
            if element.ishide or self.__sliders[index].value() == 0:
                index += 1
                continue
            # If it is not hidden, append its resource into resource_list
            else:
                self.resource_list.append(
                    [self.__combo_boxs[index].currentText(), self.__sliders[index].value()])
                index += 1

    # Used to bind individual widgets with functions it controls.
    def __bind_widgets(self) -> None:
        self.__ui.add_resource.clicked.connect(self.__add_resource)
        self.__ui.create_thread.clicked.connect(self.__create_thread)

        # Add all element into a tuple.
        self.__resource_element = [self.__ui.resource_0, self.__ui.resource_1,
                                   self.__ui.resource_2, self.__ui.resource_3, self.__ui.resource_4, self.__ui.resource_5]

        # Add comboboxs into a tuple.
        self.__combo_boxs = [self.__ui.combo_box_0, self.__ui.combo_box_1, self.__ui.combo_box_2,
                             self.__ui.combo_box_3, self.__ui.combo_box_4, self.__ui.combo_box_5]

        # Add sliders into a tuple.
        self.__sliders = [self.__ui.slider_0, self.__ui.slider_1, self.__ui.slider_2,
                          self.__ui.slider_3, self.__ui.slider_4, self.__ui.slider_5]

        # Add time_labels into a tuple.
        self.__time_labels = [self.__ui.time_label_0, self.__ui.time_label_1, self.__ui.time_label_2,
                              self.__ui.time_label_3, self.__ui.time_label_4, self.__ui.time_label_5]

        # Add remove_resource buttons into a tuple.
        self.__remove_resource_buttons = [self.__ui.remove_resource_0, self.__ui.remove_resource_1,
                                          self.__ui.remove_resource_2, self.__ui.remove_resource_3, self.__ui.remove_resource_4, self.__ui.remove_resource_5]

        # Hide all resource options at first, and show them after add 'add resources 'button been clicked.
        for element in self.__resource_element:
            element.hide()
            element.ishide = True

        # Connect elements to slider_change function.
        for slider in self.__sliders:
            slider.valueChanged.connect(self.__slider_change)

        # Connect elements to remove_resource function
        index = 0
        for button in self.__remove_resource_buttons:
            button.clicked.connect(partial(self.__hide_resource, index))
            index += 1

    # Used to unhide resource elements on the interface when click on 'add resources 'button.
    def __add_resource(self) -> None:
        # Find a resource is not hide, if no resource is hide, pop a messagebox.
        full_flag = True
        for element in self.__resource_element:
            if element.ishide == True:
                element.show()
                element.ishide = False
                full_flag = False
                break
            else:
                continue

        if full_flag:
            MessageBox = QtWidgets.QMessageBox()
            MessageBox.critical(self, "资源数量限制", "最多只能添加6个资源！")

    # When slider change, get slider value then show it with label.
    def __slider_change(self) -> None:
        index = 0
        for slider in self.__sliders:
            self.__time_labels[index].setText(str(slider.value()) + '秒')
            index += 1

    # When remove_resource button was clicked, hide this element from interface.
    def __hide_resource(self, index) -> None:
        self.__resource_element[index].hide()
        self.__resource_element[index].ishide = True

    # When create_thread botton was clicked, write data and kill this window.
    def __create_thread(self) -> None:
        self.write_data()
        self.close()
