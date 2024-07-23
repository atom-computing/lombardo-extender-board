#! /usr/bin/env python3

# Copyright (c) 2024 Atom Computing, Inc.

import argparse
import ctypes
import logging

import smbus


class SfpEepromStruct(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("identifier", ctypes.c_uint8),
        ("ext_identifier", ctypes.c_uint8),
        ("connector", ctypes.c_uint8),
        ("transceiver", ctypes.c_uint8 * 8),
        ("encoding", ctypes.c_uint8),
        ("br_nominal", ctypes.c_uint8),
        ("rate_identifier", ctypes.c_uint8),
        ("length_smf_km", ctypes.c_uint8),
        ("length_smf_100m", ctypes.c_uint8),
        ("length_om2_50um", ctypes.c_uint8),
        ("length_om1_62_5um", ctypes.c_uint8),
        ("length_om4_50um", ctypes.c_uint8),
        ("length_om3_50um", ctypes.c_uint8),
        ("vendor_name", ctypes.c_uint8 * 16),
        ("transceiver_code", ctypes.c_uint8),
        ("vendor_oui", ctypes.c_uint8 * 3),
        ("vendor_pn", ctypes.c_uint8 * 16),
        ("vendor_rev", ctypes.c_uint8 * 4),
        ("wavelength", ctypes.c_uint16),
        ("fibre_channel_speed", ctypes.c_uint8),
        ("cc_base", ctypes.c_uint8),
        ("options", ctypes.c_uint16),
        ("br_max", ctypes.c_uint8),
        ("br_min", ctypes.c_uint8),
        ("vendor_sn", ctypes.c_uint8 * 16),
        ("date_code", ctypes.c_uint8 * 8),
        ("diagnostics", ctypes.c_uint8),
        ("enhanced_options", ctypes.c_uint8 * 2),
        ("sff_8472_compliance", ctypes.c_uint8),
        ("cc_ext", ctypes.c_uint8),
        ("vendor_specific", ctypes.c_uint8 * 32),
    ]


class SfpEepromOptionstruct(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("rsvd15", ctypes.c_uint8, 1),
        ("high_power2", ctypes.c_uint8, 1),
        ("high_power", ctypes.c_uint8, 1),
        ("paging", ctypes.c_uint8, 1),
        ("retimer", ctypes.c_uint8, 1),
        ("cooled_xcvr", ctypes.c_uint8, 1),
        ("pow_lvl_decl", ctypes.c_uint8, 1),
        ("lin_recv", ctypes.c_uint8, 1),
        ("rx_decision_thr", ctypes.c_uint8, 1),
        ("tunable_tx", ctypes.c_uint8, 1),
        ("rate_select", ctypes.c_uint8, 1),
        ("tx_disable", ctypes.c_uint8, 1),
        ("tx_fault", ctypes.c_uint8, 1),
        ("signal_detect", ctypes.c_uint8, 1),
        ("loss_of_signal", ctypes.c_uint8, 1),
        ("rsvd0", ctypes.c_uint8, 1),
    ]


class SfpEepromDiagTypeStruct(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("rsvd7", ctypes.c_uint8, 1),
        ("ddm_implemented", ctypes.c_uint8, 1),
        ("internal_calib", ctypes.c_uint8, 1),
        ("external_calib", ctypes.c_uint8, 1),
        ("addr_change", ctypes.c_uint8, 1),
        ("rsvd1_0", ctypes.c_uint8, 2),
    ]


class SfpMonitorStruct(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("temp_high_alarm", ctypes.c_int16),
        ("temp_low_alarm", ctypes.c_int16),
        ("temp_high_warning", ctypes.c_int16),
        ("temp_low_warning", ctypes.c_int16),
        ("vcc_high_alarm", ctypes.c_uint16),
        ("vcc_low_alarm", ctypes.c_uint16),
        ("vcc_high_warning", ctypes.c_uint16),
        ("vcc_low_warning", ctypes.c_uint16),
        ("tx_bias_high_alarm", ctypes.c_uint16),
        ("tx_bias_low_alarm", ctypes.c_uint16),
        ("tx_bias_high_warning", ctypes.c_uint16),
        ("tx_bias_low_warning", ctypes.c_uint16),
        ("tx_power_high_alarm", ctypes.c_uint16),
        ("tx_power_low_alarm", ctypes.c_uint16),
        ("tx_power_high_warning", ctypes.c_uint16),
        ("tx_power_low_warning", ctypes.c_uint16),
        ("rx_power_high_alarm", ctypes.c_uint16),
        ("rx_power_low_alarm", ctypes.c_uint16),
        ("rx_power_high_warning", ctypes.c_uint16),
        ("rx_power_low_warning", ctypes.c_uint16),
        ("rsvd40_55", ctypes.c_uint8 * 16),
        ("rx_power_4", ctypes.c_float),
        ("rx_power_3", ctypes.c_float),
        ("rx_power_2", ctypes.c_float),
        ("rx_power_1", ctypes.c_float),
        ("rx_power_0", ctypes.c_float),
        ("tx_curr_slope", ctypes.c_uint16),
        ("tx_curr_offset", ctypes.c_uint16),
        ("tx_pwr_slope", ctypes.c_uint16),
        ("tx_pwr_offset", ctypes.c_uint16),
        ("t_slope", ctypes.c_uint16),
        ("t_offset", ctypes.c_uint16),
        ("v_slope", ctypes.c_uint16),
        ("v_offset", ctypes.c_uint16),
        ("rsvd92_94", ctypes.c_uint8 * 3),
        ("checksum", ctypes.c_uint8),
        # "Table 9-16 A/D Values and Status Bits"
        ("temp", ctypes.c_int16),
        ("vcc", ctypes.c_uint16),
        ("tx_bias", ctypes.c_uint16),
        ("tx_power", ctypes.c_uint16),
        ("rx_power", ctypes.c_uint16),
        ("optional_laser_temp", ctypes.c_uint16),
        ("optional_tec_current", ctypes.c_uint16),
        ("status_control_bits", ctypes.c_uint8),
        ("rsvd111", ctypes.c_uint8),
        ("alarms", ctypes.c_uint16),
        ("tx_equalizer_ctrl", ctypes.c_uint8),
        ("rx_emphasis_ctrl", ctypes.c_uint8),
        ("warnings", ctypes.c_uint16),
        ("extended_status", ctypes.c_uint16),
    ]


class SfpMonitorStatusControlStruct(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("tx_disable", ctypes.c_uint8, 1),
        ("soft_tx_disable", ctypes.c_uint8, 1),
        ("rs1_state", ctypes.c_uint8, 1),
        ("rs0_state", ctypes.c_uint8, 1),
        ("soft_rs0", ctypes.c_uint8, 1),
        ("tx_fault", ctypes.c_uint8, 1),
        ("rx_los", ctypes.c_uint8, 1),
        ("data_not_ready", ctypes.c_uint8, 1),
    ]


def hexdump(logging_func, bs):
    BYTES_PER_LINE = 16

    logging_func("    | ", end="")
    for i in range(BYTES_PER_LINE):
        logging_func(f"{i:02x} ", end="")
    logging_func("")

    logging_func("----+-", end="")
    for i in range(BYTES_PER_LINE):
        logging_func("---", end="")
    logging_func("")

    for i in range(0, len(bs), BYTES_PER_LINE):
        logging_func(f"{i:3x} | ", end="")
        for j in range(BYTES_PER_LINE):
            if i + j < len(bs):
                logging_func(f"{bs[i+j]:02x} ", end="")
            else:
                logging_func("   ", end="")
        logging_func("")


class SfpInfo:
    def __init__(self, bus_index: int):
        self.logger = logging.getLogger("SfpInfo")
        self.bus_index = bus_index

    def _get_eeprom_data(self) -> bytes:
        bus = smbus.SMBus(self.bus_index)

        eeprom_data = b""
        for i in range(0, 256, 16):
            eeprom_data += bytes(bus.read_i2c_block_data(0x50, i, 16))

        self.logger.debug("EEPROM data:")
        if self.logger.isEnabledFor(logging.DEBUG):
            hexdump(print, eeprom_data)

        return eeprom_data

    def _get_monitor_data(self) -> bytes:
        bus = smbus.SMBus(self.bus_index)

        monitor_data = b""
        for i in range(0, 256, 16):
            monitor_data += bytes(bus.read_i2c_block_data(0x51, i, 16))

        self.logger.debug("Monitor data:")
        if self.logger.isEnabledFor(logging.DEBUG):
            hexdump(print, monitor_data)

        return monitor_data

    def _print_eeprom(self, eeprom: bytes):
        print("  Info:")
        sfp_eeprom_struct = SfpEepromStruct.from_buffer_copy(eeprom)
        print(f"    Vendor name      : {str(sfp_eeprom_struct.vendor_name, 'ascii')}")
        print(f"    Vendor PN        : {str(sfp_eeprom_struct.vendor_pn, 'ascii')}")
        print(f"    Vendor rev       : {str(sfp_eeprom_struct.vendor_rev, 'ascii')}")
        print(f"    Vendor SN        : {str(sfp_eeprom_struct.vendor_sn, 'ascii')}")
        print(f"    Vendor OUI       : {':'.join([f'{x:02x}' for x in sfp_eeprom_struct.vendor_oui])}")
        date_code_str = str(sfp_eeprom_struct.date_code, "ascii")
        print(f"    Date code        : 20{date_code_str[0:2]}-{date_code_str[2:4]}-{date_code_str[4:6]}")
        print(f"    Wavelength       : {sfp_eeprom_struct.wavelength} nm")
        print(f"    Length (OM2/50um): {sfp_eeprom_struct.length_om2_50um * 10} m")
        print(f"    Length (OM4/50um): {sfp_eeprom_struct.length_om4_50um * 10} m")
        print(f"    Encoding         : 0x{sfp_eeprom_struct.encoding:02x} (", end="")
        if sfp_eeprom_struct.encoding == 0x01:
            print("8B/10B", end="")
        elif sfp_eeprom_struct.encoding == 0x02:
            print("4B/5B", end="")
        elif sfp_eeprom_struct.encoding == 0x03:
            print("NRZ", end="")
        elif sfp_eeprom_struct.encoding == 0x04:
            print("Manchester", end="")
        elif sfp_eeprom_struct.encoding == 0x05:
            print("SONET Scrambled", end="")
        elif sfp_eeprom_struct.encoding == 0x06:
            print("64B/66B", end="")
        print(")")

        print(f"    Baud rate        : {sfp_eeprom_struct.br_nominal * 100} Mbit/s")
        print(f"    Options:         : 0x{sfp_eeprom_struct.options:04x}")
        option = SfpEepromOptionstruct.from_buffer_copy(sfp_eeprom_struct.options.to_bytes(2, byteorder="big"))
        print(f"      Retimer/CDR      : {option.retimer}")
        print(f"      Rate Select      : {option.rate_select}")
        print(f"      Tx Disable       : {option.tx_disable}")
        print(f"      Tx Fault         : {option.tx_fault}")
        print(f"      Loss of Signal   : {option.loss_of_signal}")

        print(f"    Diagnostic       : 0x{sfp_eeprom_struct.diagnostics:02x}")
        diag_type = SfpEepromDiagTypeStruct.from_buffer_copy(sfp_eeprom_struct.diagnostics.to_bytes(1, "little"))
        print(f"      Addr change      : {diag_type.addr_change}")
        print(f"      External calib   : {diag_type.external_calib}")
        print(f"      Internal calib   : {diag_type.internal_calib}")
        print(f"      DDM implemented  : {diag_type.ddm_implemented}")

        return diag_type.ddm_implemented

    def _print_monitor(self, monitor_data: bytes):
        mon = SfpMonitorStruct.from_buffer_copy(monitor_data)

        # check if the coefficients are the ones for internal calibration
        # external calibration is not implemented yet
        assert mon.rx_power_4 == 0.0, f"coef rx_power_4 is {mon.rx_power_4}, should be 0.0"
        assert mon.rx_power_3 == 0.0, f"coef rx_power_3 is {mon.rx_power_3}, should be 0.0"
        assert mon.rx_power_2 == 0.0, f"coef rx_power_2 is {mon.rx_power_2}, should be 0.0"
        assert mon.rx_power_1 == 1.0, f"coef rx_power_1 is {mon.rx_power_1}, should be 1.0"
        assert mon.rx_power_0 == 0.0, f"coef rx_power_0 is {mon.rx_power_0}, should be 0.0"
        assert mon.tx_curr_slope == 256, f"coef tx_curr_slope is {mon.tx_curr_slope}, should be 256"
        assert mon.tx_curr_offset == 0, f"coef tx_curr_offset is {mon.tx_curr_offset}, should be 0"
        assert mon.tx_pwr_slope == 256, f"coef tx_pwr_slope is {mon.tx_pwr_slope}, should be 256"
        assert mon.tx_pwr_offset == 0, f"coef tx_pwr_offset is {mon.tx_pwr_offset}, should be 0"
        assert mon.t_slope == 256, f"coef t_slope is {mon.t_slope}, should be 256"
        assert mon.t_offset == 0, f"coef t_offset is {mon.t_offset}, should be 0"
        assert mon.v_slope == 256, f"coef v_slope is {mon.v_slope}, should be 256"
        assert mon.v_offset == 0, f"coef v_offset is {mon.v_offset}, should be 0"

        print("  Monitor:")
        print(f"    Temp     : {mon.temp / 256:.02f} degC")
        print(f"    Vcc      : {mon.vcc / 10000:.03f} V")
        print(f"    Tx Bias  : {mon.tx_bias / 500:.02f} mA")
        print(f"    Tx Power : {mon.tx_power / 10000:.03f} mW")
        print(f"    Rx Power : {mon.rx_power / 10000:.03f} mW")
        print(f"    Status/Control: 0x{mon.status_control_bits:02x}")

        status_control = SfpMonitorStatusControlStruct.from_buffer_copy(
            mon.status_control_bits.to_bytes(1, byteorder="big")
        )
        print(f"      Tx Disable: {status_control.tx_disable}")
        print(f"      RS1 State : {status_control.rs1_state}")
        print(f"      RS0 State : {status_control.rs0_state}")
        print(f"      Tx Fault  : {status_control.tx_fault}")
        print(f"      Rx LOS    : {status_control.rx_los}")

    def print_sfp_info(self):
        eeprom = self._get_eeprom_data()
        ddm_implemented = self._print_eeprom(eeprom)

        if ddm_implemented:
            monitor_data = self._get_monitor_data()
            self._print_monitor(monitor_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read SFP EEPROM and monitor data")
    parser.add_argument("bus_index", type=int, help="I2C bus index")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    sfp = SfpInfo(args.bus_index)
    sfp.print_sfp_info()
