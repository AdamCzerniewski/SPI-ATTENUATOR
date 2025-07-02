#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combined GUI for Signal Generator, Spectrum Analyzer, and PE4302 Attenuator Control
"""

import math
import socket
import sys
import os
import time
import serial
import threading
import spidev
from ui import Ui_MainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QMessageBox


class FrequencySweepThread(QThread):
    update_message = pyqtSignal(str)

    def __init__(self, s_SG, s_SA, min_att, max_att, step_sizeAtt, min_freq, max_freq, span_freq, step_sizeFreq, power, dwell_time):
        super(FrequencySweepThread, self).__init__()
        self.s_SG = s_SG
        self.s_SA = s_SA
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.min_att = min_att
        self.max_att = max_att
        self.step_sizeAtt = step_sizeAtt
        self.span = span_freq
        self.step_sizeFreq = step_sizeFreq
        self.power = power
        self.dwell_time = dwell_time
        
        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Open SPI bus 0
        self.spi.mode = 0  # SPI mode
        self.spi.max_speed_hz = 7629

        # Initialize Serial for Attenuator
        os.system("sudo chmod 666 /dev/ttyS0")  # Port permissions
        self.ser = serial.Serial('/dev/ttyS0', baudrate=115200)
    
    # Send SPI data to the attenuator
    def spiWrite(self, value):
        print("!!!!1111")
        self.spi.xfer([value])  # Send SPI value
        print(f"Bits sent: {bin(value)}")
    
    def run(self):
        freq = self.min_freq
        # while freq <= self.max_freq:
        #     self.update_message.emit(f"Setting frequency to {freq} MHz")
            
        #     setFreq = ":FREQ " + str(freq) + "MHz\r\n"
        #     self.s_SG.send(setFreq.encode())            
            
        #     sweepCenterFreq = ':SENSe:FREQuency:CENTer ' + str(freq) + 'MHz\r\n'
        #     self.s_SA.send(sweepCenterFreq.encode())
            
        #     sweepSpanFreq = ':SENSe:FREQuency:SPAN ' + str(self.span) + 'MHz\r\n'
        #     self.s_SA.send(sweepSpanFreq.encode())            
            
        #     setPower = ":LEV " + str(self.power) + "dBm\r\n"
        #     self.s_SG.send(setPower.encode())               
            
        #     time.sleep(self.dwell_time)

        #     freq += self.step_size

        # self.update_message.emit("Frequency sweep completed")
        for f in range (int(self.min_freq), int(self.max_freq), int(self.step_sizeFreq)):
            
            #SET PLL1 FREQ
            setFreq = ":FREQ " + str(f) + "MHz\r\n"
            print("PLL1 =", f)
            self.s_SG.send(setFreq.encode())              
            
            sweepCenterFreq = ':SENSe:FREQuency:CENTer ' + str(f) + 'MHz\r\n'
            self.s_SA.send(sweepCenterFreq.encode())
            
            sweepSpanFreq = ':SENSe:FREQuency:SPAN ' + str(self.span) + 'MHz\r\n'
            self.s_SA.send(sweepSpanFreq.encode())            
            
            setPower = ":LEV " + str(self.power) + "dBm\r\n"
            self.s_SG.send(setPower.encode())             
            
            #SET PLL2
            f += 10
            setFreq = ":FREQ " + str(f) + "MHz\r\n"
            print("PLL2 =", f)
            self.s_SG.send(setFreq.encode())              
            
            sweepCenterFreq = ':SENSe:FREQuency:CENTer ' + str(f) + 'MHz\r\n'
            self.s_SA.send(sweepCenterFreq.encode())
            
            sweepSpanFreq = ':SENSe:FREQuency:SPAN ' + str(self.span) + 'MHz\r\n'
            self.s_SA.send(sweepSpanFreq.encode())            
            
            setPower = ":LEV " + str(self.power) + "dBm\r\n"
            self.s_SG.send(setPower.encode())        
    
    


            
            for att in range(int(self.min_att), int(self.max_att), int(self.step_sizeAtt)):
                self.update_message.emit(f"Setting attenuation to {att} dB")
                spi_value = int(round(att * 2))
                
                self.spiWrite(spi_value)
                # sweepCenterFreq = ':SENSe:FREQuency:CENTer ' + str(f) + 'MHz\r\n'
                # self.s_SA.send(sweepCenterFreq.encode())
            
                # sweepSpanFreq = ':SENSe:FREQuency:SPAN ' + str(self.span) + 'MHz\r\n'
                # self.s_SA.send(sweepSpanFreq.encode())            
            
                # setPower = ":LEV " + str(self.power) + "dBm\r\n"
                # self.s_SG.send(setPower.encode())   
                
                time.sleep(self.dwell_time)                
    
    # def run(self):
    #     att = self.min_att
    #     while att <= self.max_att:
    #         self.update_message.emit(f"Setting attenuation to {att} dB")
    #         spi_value = int(round(att * 2))
    #         self.spiWrite(spi_value)
            
    #         setFreq = ":FREQ " + str(self.freq) + "MHz\r\n"
    #         self.s_SG.send(setFreq.encode())            
            
    #         sweepCenterFreq = ':SENSe:FREQuency:CENTer ' + str(self.freq) + 'MHz\r\n'
    #         self.s_SA.send(sweepCenterFreq.encode())
            
    #         sweepSpanFreq = ':SENSe:FREQuency:SPAN ' + str(self.span) + 'MHz\r\n'
    #         self.s_SA.send(sweepSpanFreq.encode())            
            
    #         setPower = ":LEV " + str(self.power) + "dBm\r\n"
    #         self.s_SG.send(setPower.encode())               
            
    #         time.sleep(self.dwell_time)

    #         att += self.step_size

    #     self.update_message.emit("Attenuation sweep completed")

    # Send command to Signal Generator

class sendSG_Cmd(QThread):
    update_message = pyqtSignal(str)
    
    def __init__(self, s_SG, command):
        super(sendSG_Cmd, self).__init__()
        self.cmd = command
        self.output = str(self.s_SG.recv(4096))

    def run(self):
    
        self.cmd = self.ui.tf_SG_cmd.text() + '\r\n'
        self.s_SG.send(self.cmd.encode())
        self.ui.te_messages.append(self.output)

class AttenuationSweepThread(QThread):
    update_message = pyqtSignal(str)

    def __init__(self, spiWrite, s_SG, s_SA, min_att, max_att, step_size, power, frequency, span_freq, dwell_time):
        super(AttenuationSweepThread, self).__init__()
        self.spiWrite = spiWrite
        self.s_SG = s_SG
        self.s_SA = s_SA
        self.min_att = min_att
        self.max_att = max_att
        self.step_size = step_size
        self.power = power
        self.freq = frequency
        self.span = span_freq
        self.dwell_time = dwell_time
        
    def run(self):
        att = self.min_att
        while att <= self.max_att:
            self.update_message.emit(f"Setting attenuation to {att} dB")
            spi_value = int(round(att * 2))
            self.spiWrite(spi_value)
            
            setFreq = ":FREQ " + str(self.freq) + "MHz\r\n"
            self.s_SG.send(setFreq.encode())            
            
            sweepCenterFreq = ':SENSe:FREQuency:CENTer ' + str(self.freq) + 'MHz\r\n'
            self.s_SA.send(sweepCenterFreq.encode())
            
            sweepSpanFreq = ':SENSe:FREQuency:SPAN ' + str(self.span) + 'MHz\r\n'
            self.s_SA.send(sweepSpanFreq.encode())            
            
            setPower = ":LEV " + str(self.power) + "dBm\r\n"
            self.s_SG.send(setPower.encode())               
            
            time.sleep(self.dwell_time)

            att += self.step_size

        self.update_message.emit("Attenuation sweep completed")


class Main(qtw.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print("show GUI")

        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Open SPI bus 0
        self.spi.mode = 0  # SPI mode
        self.spi.max_speed_hz = 7629

        # Initialize Serial for Attenuator
        os.system("sudo chmod 666 /dev/ttyS0")  # Port permissions
        self.ser = serial.Serial('/dev/ttyS0', baudrate=115200)

        # Initialize state variables
        self.attVal = 0

        # Connect buttons to functions
        self.ui.btn_SG_Connect.clicked.connect(self.threaded_connectToSigGen)
        self.ui.btn_SA_Connect.clicked.connect(self.threaded_connectToSpecAn)
        self.ui.btn_enterAtt.clicked.connect(self.threaded_setAttenuation)

        self.ui.btn_SG_SendCmd.clicked.connect(self.threaded_sendSGCmd)
        self.ui.btn_SA_SendCmd.clicked.connect(self.threaded_sendSACmd)

        self.ui.btn_RFmode.clicked.connect(self.threaded_RFmode_SignalGenerator)
        self.ui.btn_sendFreq.clicked.connect(self.threaded_signalFrequency)
        self.ui.btn_sendCenterFreq.clicked.connect(self.threaded_centerFreqSA)
        self.ui.btn_sendSpan.clicked.connect(self.threaded_spanFreqSA)
        self.ui.btn_sendPower.clicked.connect(self.threaded_signalPower)

        self.ui.btn_startSweep.clicked.connect(self.threaded_freqSweep)
        #self.ui.btn_startSweepAtt.clicked.connect(self.threaded_attSweep)

        # Print out the PE4302 Truth Table
        self.print_pe4302_table()
   
    def print_pe4302_table(self):
        print("\nPE4302 USES 6 BITS\n")
        print("         PE4302 TRUTH TABLE      ")
        print("----------------------------------")
        print("|  16    8    4    2    1    0.5 |  dB")
        for i in range(6):
            print("|  ", " ".join(['1' if j == i else '0' for j in range(6)]), "|  bit config.")
        print("----------------------------------")

    # Signal Generator connection
    def connectToSigGen(self):
        try:
            self.s_SG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s_SG.settimeout(10)
            hostSG = self.ui.tf_SG_IP.text()
            portSG = int(self.ui.tf_SG_Port.text())
            self.s_SG.connect((hostSG, portSG))
            print(f"Socket to Signal Generator established at {hostSG}:{portSG}")
        except socket.error as err:
            print("socket creation failed with error %s" % (err))

    # Send command to Signal Generator
    def sendSGCmd(self):
        cmd = self.ui.tf_SG_cmd.text() + '\r\n'
        self.s_SG.send(cmd.encode())
        output = str(self.s_SG.recv(4096))
        self.ui.te_messages.append(output)

    # Connect to Spectrum Analyzer
    def connectToSpecAn(self):
        try:
            self.s_SA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s_SA.settimeout(10)
            hostSA = self.ui.tf_SA_IP.text()
            portSA = int(self.ui.tf_SA_Port.text())
            self.s_SA.connect((hostSA, portSA))
            print(f"Socket to Spectrum Analyzer established at {hostSA}:{portSA}")
        except socket.error as err:
            print("socket creation failed with error %s" % (err))

    # Send command to Spectrum Analyzer
    def sendSACmd(self):
        cmd = self.ui.tf_SA_cmd.text() + '\r\n'
        self.s_SA.send(cmd.encode())
        output = str(self.s_SA.recv(4096))
        self.ui.te_messages.append(output)

    # Set attenuation value through SPI
    def setAttenuation(self):
        print("!!!!!")
        try:
            self.attVal = self.ui.dsbox_attenuation.value()
            print(f"Setting attenuation to {self.attVal} dB")
            spi_value = self.convertData_to_SPI(self.attVal)
            self.spiWrite(spi_value)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e), QMessageBox.Ok)

    # Convert attenuation value to SPI command format (dummy implementation)
    def convertData_to_SPI(self, attenuation_value):
        return int(round(attenuation_value * 2))

    # Send SPI data to the attenuator
    def spiWrite(self, value):
        print("!!!!1111")
        self.spi.xfer([value])  # Send SPI value
        print(f"Bits sent: {bin(value)}")

    # Thread for each operation
    def threaded_connectToSigGen(self):
        t = threading.Thread(target=self.connectToSigGen)
        t.start()

    def threaded_sendSGCmd(self):
        command = self.ui.tf_SG_cmd.text()
        output = self.ui.s_SG.recv(4096)
        
        self.send_SG_Cmd_thread = sendSG_Cmd(self.s_SG, command, output)
        self.send_SG_Cmd_thread.update_message.connect(self.update_console)
        self.send_SG_Cmd_thread.start()

    def threaded_connectToSpecAn(self):
        t = threading.Thread(target=self.connectToSpecAn)
        t.start()

    def threaded_sendSACmd(self):
        t = threading.Thread(target=self.sendSACmd)
        t.start()

    def threaded_setAttenuation(self):
        t = threading.Thread(target=self.setAttenuation)
        t.start()

    def threaded_RFmode_SignalGenerator(self):
        t = threading.Thread(target=self.RFmode_SignalGenerator)
        t.start()

    def threaded_signalFrequency(self):
        t = threading.Thread(target=self.signalFrequency)
        t.start()

    def threaded_centerFreqSA(self):
        t = threading.Thread(target=self.centerFreqSA)
        t.start()

    def threaded_spanFreqSA(self):
        t = threading.Thread(target=self.spanFreqSA)
        t.start()

    def threaded_signalPower(self):
        t = threading.Thread(target=self.signalPower)
        t.start()

    def threaded_freqSweep(self):
        min_freq = float(self.ui.tf_minFreq.text())
        max_freq = float(self.ui.tf_maxFreq.text())
        span_freq = float(self.ui.tf_spanFreqSweep.text())
        step_sizeFreq = float(self.ui.tf_stepSizeFreq.text())
        power = float(self.ui.tf_powerFreqSweep.text())
        dwell_time = float(self.ui.tf_dwellTimeAtt.text())
        
        min_att = float(self.ui.tf_minAtt.text())
        max_att = float(self.ui.tf_maxAtt.text())
        step_sizeAtt = float(self.ui.tf_stepSizeAtt.text())

        # self.att_sweep_thread = AttenuationSweepThread(self.spiWrite, self.s_SG, self.s_SA, min_att, max_att, step_size, power, frequency, span_freq, dwell_time)
        # self.att_sweep_thread.update_message.connect(self.update_console)
        # self.att_sweep_thread.start()

        self.freq_sweep_thread = FrequencySweepThread(self.s_SG, self.s_SA, min_att, max_att, step_sizeAtt, min_freq, max_freq, span_freq, step_sizeFreq, power, dwell_time)
        self.freq_sweep_thread.update_message.connect(self.update_console)
        self.freq_sweep_thread.start()

    def threaded_attSweep(self):
        min_att = float(self.ui.tf_minAtt.text())
        max_att = float(self.ui.tf_maxAtt.text())
        step_size = float(self.ui.tf_stepSizeAtt.text())
        power = float(self.ui.tf_powerSweepAtt.text())
        frequency = float(self.ui.tf_freqAttSweep.text())
        span_freq = float(self.ui.tf_spanAttSweep.text())
        dwell_time = float(self.ui.tf_dwellTimeAtt.text())

        self.att_sweep_thread = AttenuationSweepThread(self.spiWrite, self.s_SG, self.s_SA, min_att, max_att, step_size, power, frequency, span_freq, dwell_time)
        self.att_sweep_thread.update_message.connect(self.update_console)
        self.att_sweep_thread.start()

    def update_console(self, message):
        self.ui.te_messages.append(message)

    # RF mode control for Signal Generator
    def RFmode_SignalGenerator(self):
        if self.ui.btn_RFmode.isChecked():
            self.s_SG.sendall(':OUTP ON\n'.encode())
        else:
            self.s_SG.sendall(':OUTP OFF\n'.encode())

    # Frequency setting for Signal Generator
    def signalFrequency(self):
        self.freq = self.ui.tf_FreqFixed.text()
        self.freq = float(self.freq)
        if 0.009 <= self.freq <= 2100:
            setFreq = ":FREQ " + str(self.freq) + "MHz\r\n"
            self.s_SG.send(setFreq.encode())
            time.sleep(1)
        else:
            print('Please enter a frequency less than 2100 MHz and greater than 0.009 MHz')

    # Spectrum Analyzer functions
    def centerFreqSA(self):
        centerFreq = self.ui.tf_centerFreq.text()
        command = f':SENSe:FREQuency:CENTer {centerFreq}MHz\r\n'
        self.s_SA.send(command.encode())

    def spanFreqSA(self):
        spanFreq = self.ui.tf_spanFreq.text()
        command = f':SENSe:FREQuency:SPAN {spanFreq}MHz\r\n'
        self.s_SA.send(command.encode())

    def signalPower(self):
        power = float(self.ui.tf_power.text())
        if -100 <= power <= 5:
            setPower = ":LEV " + str(power) + "dBm" + "\r\n"
            self.s_SG.send(setPower.encode())
            time.sleep(1)
        else:
            print('Please enter power less than 10dBm and greater than -100 dBm')


if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = Main()
    widget.show()
    app.exec_()