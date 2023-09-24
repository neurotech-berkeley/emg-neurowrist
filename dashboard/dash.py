import sys
import serial
import csv
import os
import time
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg

def populate_serial_ports(self):
    # Use the "ls /dev/cu.*" command to get a list of serial ports
    available_ports = []
    # run 'ls /dev/cu.*' in terminal
    # get the output of the command
    # split the output into a list and store it in available_ports
    available_ports = os.popen('ls /dev/cu.*').read().split()
    # add the available ports to the combo box
    for port in available_ports:
        self.serial_port_combo.addItem(port)


class EMG_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize GUI elements
        self.serial_port_combo = QComboBox(self)
        self.record_button = QPushButton("Start Recording", self)
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setYRange(0, 4095) # prevent scaling
        self.plot_curve = None

        # Set GUI layout
        layout = QGridLayout()
        layout.addWidget(self.serial_port_combo, 0, 0)
        layout.addWidget(self.record_button, 0, 1)
        layout.addWidget(self.plot_widget, 1, 0, 1, 2)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Create a combo box for selecting the serial port
        self.serial_port_combo.addItem("Select Serial Port")
        self.populate_serial_ports()
        self.serial_port_combo.currentIndexChanged.connect(self.update_serial_port)
        # port for serial communication with the device
        self.port = None

        # Create a start/stop recording button
        self.record_button.setStyleSheet("background-color: green; color: white")
        self.record_button.clicked.connect(self.toggle_record)

        # Set window properties
        self.setWindowTitle('Neurotech Devices - EMG analysis GUI')
        self.setGeometry(300, 300, 800, 600)

    def populate_serial_ports(self):
        # Use the "ls /dev/cu.*" command to get a list of serial ports
        available_ports = []
        # run 'ls /dev/cu.*' in terminal
        # get the output of the command
        # split the output into a list and store it in available_ports
        available_ports = os.popen('ls /dev/cu.*').read().split()
        # add the available ports to the combo box
        for port in available_ports:
            self.serial_port_combo.addItem(port)

    def update_serial_port(self):
        # Connect to the selected serial port and start streaming data
        self.port = self.serial_port_combo.currentText()
        if self.port != "Select Serial Port":
            self.ser = serial.Serial(self.port, 115200, timeout=1)
            self.record_button.setEnabled(True)

    def toggle_record(self):
        # Start or stop recording data to a CSV file
        if self.record_button.text() == "Start Recording":
            self.record_button.setText("Stop Recording")
            self.record_button.setStyleSheet("background-color: red; color: white")
            # based on the current time, create a unique CSV filename
            csv_filename = "recordings/emg_data_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
            self.csv_file = open(csv_filename, "w", newline="")
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow(["time", "ch0", "ch1", "ch2"])
            self.record_data = True
            self.start_time = time.time()
            self.plot_real_time_data()
        else:
            self.record_button.setText("Start Recording")
            self.record_button.setStyleSheet("background-color: green; color: white")
            self.csv_file.close()
            self.record_data = False
            # stop the timer and display the last 100 data points
            self.timer.stop()
            self.plot_curve.setData(self.xdata[-100:], self.ydata[-100:])

    def plot_real_time_data(self):
        # This function will plot the data from the selected serial port in real-time
        self.xdata, self.ydata = [], []  # Initialize the x and y data arrays
        self.start_time = time.time()  # Get the start time
        # clear the plot
        self.plot_widget.clear()
        # Create the the plot curve that updates in real-time every 10ms
        self.plot_curve = self.plot_widget.plot(self.xdata, self.ydata, pen=pg.mkPen('r', width=3))
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start(1)

    def update_plot_data(self):
        # This function will update the plot data in real-time
        ser = self.ser
        # Read the data from the serial port
        data = ser.readline().decode("utf-8")
        # data is in the format: "0 4096 ch0 ch1 ch2\n"
        # split the data into a list
        data = data.split()

        # Check if the data is valid
        if data != "":
            # Get the current time
            current_time = time.time() - self.start_time
            current_time = round(current_time, 3)
            # Add the data to the x and y data arrays
            self.xdata.append(current_time)
            ch0 = data[2]
            ch1 = data[3]
            ch2 = data[4]
            self.ydata.append(float(ch0))
            print(ch0, ch1, ch2)
            # Update the plot curve with the new data (only keep the last 100 data points)
            self.plot_curve.setData(self.xdata[-100:], self.ydata[-100:])
            # Check if the record data flag is set to True
            if self.record_data:
                # Write the data to the CSV file
                self.csv_writer.writerow([current_time, ch0, ch1, ch2])
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = EMG_GUI()
    gui.show()
    sys.exit(app.exec_())