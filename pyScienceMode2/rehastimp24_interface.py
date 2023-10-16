from sciencemode import sciencemode
from pyScienceMode2.sciencemode import RehastimGeneric
import serial
from pyScienceMode2.utils import *

import time


class StimulatorP24(RehastimGeneric):
    """
    Class used for the communication with Rehastim P24.
    """

    MAX_PACKET_BYTES = 69
    STUFFED_BYTES = [240, 15, 129, 85, 10]
    BAUD_RATE = 3000000
    Flow_Control = True

    def __init__(self, port: str, show_log: bool = False, device_type: str = "RehastimP24"):
        """
        Creates an object stimulator for the rehastim P24.

        Parameters
        ----------
        port : str
            Port of the computer connected to the Rehastim.
        show_log: bool
            If True, the log of the communication will be printed.

        """

        self.list_channels = None
        self.stimulation_interval = None
        self.inter_pulse_interval = 2
        self.electrode_number = 0
        self.amplitude = []
        self.pulse_width = []
        self.mode = []
        self.muscle = []
        self.given_channels = []
        self.stimulation_started = None
        self.point_number = 0
        self.show_log = show_log

        super().__init__(port, show_log, device_type=device_type)

    def _initialize_device(self):
        """
        Initialize the device.
        """
        com = sciencemode.ffi.new("char[]", self.port.port.encode())
        ret = sciencemode.smpt_check_serial_port(com)
        if not sciencemode.smpt_open_serial_port(self.device, self.com):
            raise ConnectionError(f"Impossible d'ouvrir le port série {self.com.decode()}.")

    def ll_init(self):
        ll_init = sciencemode.ffi.new("Smpt_ll_init*")
        ll_init.high_voltage_level = sciencemode.Smpt_High_Voltage_Default
        ll_init.packet_number = sciencemode.smpt_packet_number_generator_next(self.device)

        if not sciencemode.smpt_send_ll_init(self.device, ll_init):
            raise RuntimeError("Ll initialization failed.")

        print("Le niveau inférieur (lower level) a été initialisé avec succès.")

    def init_stimulation(self):
        """
        Démarre la stimulation sur le dispositif.
        """
        ml_init = sciencemode.ffi.new("Smpt_ml_init*")
        ml_init.packet_number = sciencemode.smpt_packet_number_generator_next(self.device)

        if not sciencemode.smpt_send_ml_init(self.device, ml_init):
            raise RuntimeError("failed to start stimulation")

        print("Stimulation démarrée avec succès.")

    def start_stimulation(self,stimulation_duration: float = None, upd_list_channels: list = None):
        if upd_list_channels is not None:
            new_electrode_number = calc_electrode_number(upd_list_channels)

        ml_update = sciencemode.ffi.new("Smpt_ml_update*")
        ml_update.packet_number = sciencemode.smpt_packet_number_generator_next(self.device)

    def stop_stimulation(self):
        """
        Arrête la stimulation sur le dispositif.
        """
        packet_number = sciencemode.smpt_packet_number_generator_next(self.device)

        if not sciencemode.smpt_send_ml_stop(self.device, packet_number):
            raise RuntimeError("Échec de l'arrêt de la stimulation.")

        print("Stimulation arrêtée avec succès.")