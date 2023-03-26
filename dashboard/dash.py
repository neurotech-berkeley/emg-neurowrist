import sys
import csv
import serial
import threading
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import serial.tools.list_ports

class WaveformReader(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize GUI elements
        self.serial_port = QComboBox(self)
        self.serial_port_label = QLabel('Serial Port', self)
        self.channel_count = QComboBox(self)
        self.channel_count_label = QLabel('Channel Count', self)
        self.start_button = QPushButton('Start Recording', self)
        self.stop_button = QPushButton('Stop Recording', self)
        self.plot_widget = pg.PlotWidget(self)
        self.plot_curve = None
        self.csv_data = []
        self.csv_file = None

        # Set GUI layout
        layout = QGridLayout()
        layout.addWidget(self.serial_port_label, 0, 0)
        layout.addWidget(self.serial_port, 0, 1)
        layout.addWidget(self.channel_count_label, 1, 0)
        layout.addWidget(self.channel_count, 1, 1)
        layout.addWidget(self.start_button, 2, 0)
        layout.addWidget(self.stop_button, 2, 1)
        layout.addWidget(self.plot_widget, 3, 0, 1, 2)
        self.setLayout(layout)

        # Populate serial port dropdown
        for port in serial.tools.list_ports.comports():
            self.serial_port.addItem(port.device)

        # Populate channel count dropdown
        self.channel_count.addItems(['1', '2', '3', '4', '5'])

        # Connect signals to slots
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.serial_port.currentIndexChanged.connect(self.update_serial_port)
        self.channel_count.currentIndexChanged.connect(self.update_channel_count)

        # Set window properties
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Waveform Reader')

        # Initialize serial connection
        self.ser = None
        self.serial_thread = None
        self.serial_running = False
        self.serial_lock = threading.Lock()

    def update_serial_port(self):
        # Update serial port when dropdown selection changes
        port_name = self.serial_port.currentText()
        if self.ser:
            self.ser.close()
        self.ser = serial.Serial(port_name, baudrate=115200)

    def update_channel_count(self):
        # Update channel count when dropdown selection changes
        channel_count = int(self.channel_count.currentText())
        self.plot_widget.clear()
        self.plot_curve = self.plot_widget.plot(pen='b')
        self.plot_curve.setData(np.zeros(channel_count))

    def start_recording(self):
        # Start recording when button is pressed
        self.csv_data = []
        self.csv_file = open('data.csv', 'w', newline='')
        self.serial_running = True
        self.serial_thread = threading.Thread(target=self.serial_reader)
        self.serial_thread.start()

    def stop_recording(self):
        # Stop recording when button is pressed
        self.serial_running = False
        self.serial_thread.join()
        self.csv_file.close()

    def serial_reader(self):
        # Read data from serial port and update plot in real-time
        channel_count = int(self.channel_count.currentText())
        while self.serial_running:
            # Read data from serial port
            with self.serial_lock:
                data = self.ser.readline().decode().rstrip().split(',')
            if len(data) == channel_count:
                data = [float(x) for x in data]
                self.csv_data.append(data)
                self.csv_file.write(','.join([str(x) for x in data]) + '\n')
                self.plot_curve.setData(data)

def read_csv_file(self):
    # Read CSV file and display data in plot
    file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV file', '', 'CSV files (*.csv)')
    if file_name:
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            data = []
            for row in reader:
                row = [float(x) for x in row]
                data.append(row)
            data = np.array(data).T
            self.channel_count.setCurrentIndex(data.shape[0] - 1)
            self.plot_curve.setData(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = WaveformReader()
    reader.show()
    sys.exit(app.exec_())