"""Higher-level access to Huawei Solar inverters."""

from __future__ import annotations

import asyncio
import logging
import typing as t

from . import register_names as rn, register_values as rv
from .exceptions import HuaweiSolarException, InvalidCredentials, PermissionDenied, ReadException
from .files import (
    OptimizerRealTimeData,
    OptimizerRealTimeDataFile,
    OptimizerSystemInformation,
    OptimizerSystemInformationDataFile,
)
from .huawei_solar import DEFAULT_BAUDRATE, DEFAULT_SLAVE, DEFAULT_TCP_PORT, AsyncHuaweiSolar, Result

_LOGGER = logging.getLogger(__name__)

HEARTBEAT_INTERVAL = 15


class HuaweiSolarBridge:
    """The HuaweiSolarBridge exposes a higher-level interface than AsyncHuaweiSolar,
    making it easier to interact with a Huawei Solar inverter."""

    model_name: str
    serial_number: str
    product_number: str

    pv_string_count: int = 0
    has_optimizers: bool = False

    battery_1_type: rv.StorageProductModel = rv.StorageProductModel.NONE
    battery_2_type: rv.StorageProductModel = rv.StorageProductModel.NONE
    supports_capacity_control = False
    power_meter_online = False
    power_meter_type: t.Optional[rv.MeterType] = None

    _pv_registers: list[str]

    __login_lock = asyncio.Lock()
    __heartbeat_enabled = False
    __heartbeat_task: t.Optional[asyncio.Task] = None

    __username: t.Optional[str] = None
    __password: t.Optional[str] = None

    previous_update_result: t.Optional[t.Dict[str, Result]] = None
    previous_inverter_update_result: t.Optional[t.Dict[str, Result]] = None

    def __init__(
        self,
        client: AsyncHuaweiSolar,
        update_lock: asyncio.Lock,
        primary: bool,
        slave_id: t.Optional[int] = None,
    ):
        self.client = client
        self.update_lock = update_lock

        self._primary = primary
        self.slave_id = slave_id or 0

    @classmethod
    async def create(cls, host: str, port: int = DEFAULT_TCP_PORT, slave_id: int = DEFAULT_SLAVE):
        """Creates a HuaweiSolarBridge instance for the inverter hosting the modbus interface."""
        client = await AsyncHuaweiSolar.create(host, port, slave_id)
        update_lock = asyncio.Lock()
        bridge = cls(client, update_lock, primary=True)
        await HuaweiSolarBridge.__populate_fields(bridge)

        return bridge

    @classmethod
    async def create_rtu(
        cls,
        port: str,
        baudrate: int = DEFAULT_BAUDRATE,
        slave_id: int = DEFAULT_SLAVE,
    ):
        """Creates a HuaweiSolarBridge instance for the inverter hosting the modbus interface."""
        client = await AsyncHuaweiSolar.create_rtu(port, baudrate, slave_id)
        update_lock = asyncio.Lock()
        bridge = cls(client, update_lock, primary=True)
        await HuaweiSolarBridge.__populate_fields(bridge)

        return bridge

    @classmethod
    async def create_extra_slave(cls, primary_bridge: "HuaweiSolarBridge", slave_id: int):
        """Creates a HuaweiSolarBridge instance for extra slaves accessible via the given AsyncHuaweiSolar instance."""
        assert primary_bridge.slave_id != slave_id

        await primary_bridge.client.determine_battery_type(slave_id)

        bridge = cls(
            primary_bridge.client,
            primary_bridge.update_lock,
            primary=False,
            slave_id=slave_id,
        )
        await HuaweiSolarBridge.__populate_fields(bridge)
        return bridge

    @staticmethod
    async def __populate_fields(bridge: "HuaweiSolarBridge"):
        """Computes all the fields that should be returned on each update-call."""

        (
            model_name_result,
            serial_number_result,
            pn_result,
        ) = await bridge.client.get_multiple([rn.MODEL_NAME, rn.SERIAL_NUMBER, rn.PN], bridge.slave_id)

        bridge.model_name = model_name_result.value
        bridge.serial_number = serial_number_result.value
        bridge.product_number = pn_result.value

        bridge.pv_string_count = (await bridge.client.get(rn.NB_PV_STRINGS, bridge.slave_id)).value
        bridge._compute_pv_registers()  # pylint: disable=protected-access

        try:
            bridge.has_optimizers = (await bridge.client.get(rn.NB_OPTIMIZERS, bridge.slave_id)).value
        except ReadException:  # some inverters throw an IllegalAddress exception when accessing this address
            pass

        try:
            bridge.battery_1_type = (await bridge.client.get(rn.STORAGE_UNIT_1_PRODUCT_MODEL, bridge.slave_id)).value
        except ReadException:
            pass
        try:
            bridge.battery_2_type = (await bridge.client.get(rn.STORAGE_UNIT_2_PRODUCT_MODEL, bridge.slave_id)).value
        except ReadException:
            pass

        if (
            bridge.battery_1_type != rv.StorageProductModel.NONE
            and bridge.battery_2_type != rv.StorageProductModel.NONE
            and bridge.battery_1_type != bridge.battery_2_type
        ):
            _LOGGER.warning("Detected two batteries of a different type. This can lead to unexpected behavior")

        if bridge.battery_type != rv.StorageProductModel.NONE:
            try:
                await bridge.client.get(rn.STORAGE_CAPACITY_CONTROL_MODE, bridge.slave_id)
                bridge.supports_capacity_control = True
            except ReadException:
                pass

        try:
            bridge.power_meter_online = (
                await bridge.client.get(rn.METER_STATUS, bridge.slave_id)
            ).value == rv.MeterStatus.NORMAL
        except ReadException:
            pass

        # Caveat: if the inverter is in offline mode, and the power meter is thus offline,
        # we will incorrectly detect that no power meter is present.
        if bridge.power_meter_online:
            bridge.power_meter_type = (await bridge.client.get(rn.METER_TYPE, bridge.slave_id)).value

    async def _get_multiple_to_dict(self, names: list[str]) -> dict[str, Result]:
        return dict(zip(names, await self.client.get_multiple(names, self.slave_id)))

    async def update(self) -> dict[str, Result]:
        """Receive an update for all (interesting) available registers

        WARNING: Deprecated in favor of 3 separate functions: update_inverter,
        update_power_meter, update_energy_storage that allow for finer grained management
        of what registers must be read by the client
        """

        # Only allow one update at a time
        async with self.update_lock:
            result = await self._get_multiple_to_dict(INVERTER_REGISTERS)

            # State and Alarm registers can be combined with PV registers due to close proximity
            result.update(await self._get_multiple_to_dict(STATE_AND_ALARM_REGISTERS + self._pv_registers))

            if self.has_optimizers:
                result.update(await self._get_multiple_to_dict(OPTIMIZER_REGISTERS))

            if self.power_meter_type is not None:
                # If the 'device status' has changed, force a recheck of the power meter online status
                # cfr. https://gitlab.com/Emilv2/huawei-solar/-/merge_requests/9#note_1281471842
                if self.previous_update_result:
                    if result[rn.DEVICE_STATUS].value != self.previous_update_result[rn.DEVICE_STATUS].value:
                        self.power_meter_online = False

                if not self.power_meter_online:
                    power_meter_online_register = await self.client.get(rn.METER_STATUS, self.slave_id)
                    result[rn.METER_STATUS] = power_meter_online_register
                    self.power_meter_online = power_meter_online_register.value

                if self.power_meter_online:
                    try:
                        result.update(await self._get_multiple_to_dict(POWER_METER_REGISTERS))
                    except HuaweiSolarException as exc:
                        _LOGGER.info(
                            "Fetching power meter registers failed. "
                            "We'll assume that this is due to the power meter going offline and the registers "
                            "becoming invalid as a result.",
                            exc_info=exc,
                        )
                        self.power_meter_online = False

            if self.battery_type != rv.StorageProductModel.NONE:
                result.update(await self._get_multiple_to_dict(ENERGY_STORAGE_REGISTERS))

        self.previous_update_result = result
        return result

    async def update_inverter(self) -> dict[str, Result]:
        """Receive an update for all (interesting) available registers of the inverter"""

        # Only allow one update at a time
        async with self.update_lock:
            result = await self._get_multiple_to_dict(INVERTER_REGISTERS)

            # State and Alarm registers can be combined with PV registers due to close proximity
            result.update(await self._get_multiple_to_dict(STATE_AND_ALARM_REGISTERS + self._pv_registers))

            if self.has_optimizers:
                result.update(await self._get_multiple_to_dict(OPTIMIZER_REGISTERS))

            if self.power_meter_type is not None:
                # If the 'device status' has changed, force a recheck of the power meter online status
                # cfr. https://gitlab.com/Emilv2/huawei-solar/-/merge_requests/9#note_1281471842
                if self.previous_inverter_update_result:
                    if result[rn.DEVICE_STATUS].value != self.previous_inverter_update_result[rn.DEVICE_STATUS].value:
                        self.power_meter_online = False

        self.previous_inverter_update_result = result
        return result

    async def update_power_meter(self) -> dict[str, Result]:
        """Receive an update for all (interesting) available registers of the power meter"""

        result = {}

        # Only allow one update at a time
        async with self.update_lock:
            if self.power_meter_type is not None:
                if not self.power_meter_online:
                    power_meter_online_register = await self.client.get(rn.METER_STATUS, self.slave_id)
                    result[rn.METER_STATUS] = power_meter_online_register
                    self.power_meter_online = power_meter_online_register.value

                if self.power_meter_online:
                    try:
                        result.update(await self._get_multiple_to_dict(POWER_METER_REGISTERS))
                    except HuaweiSolarException as exc:
                        _LOGGER.info(
                            "Fetching power meter registers failed. "
                            "We'll assume that this is due to the power meter going offline and the registers "
                            "becoming invalid as a result.",
                            exc_info=exc,
                        )
                        self.power_meter_online = False

        self.previous_update_result = result
        return result

    async def update_energy_storage(self) -> dict[str, Result]:
        """Receive an update for all (interesting) available energy storage registers"""

        result = {}
        # Only allow one update at a time
        async with self.update_lock:
            if self.battery_type != rv.StorageProductModel.NONE:
                result.update(await self._get_multiple_to_dict(ENERGY_STORAGE_REGISTERS))

        return result

    async def update_configuration_registers(self):
        """Receive an update for all configurable registers"""

        result = {}
        # Only allow one update at a time
        async with self.update_lock:
            if self.battery_type != rv.StorageProductModel.NONE:
                result.update(await self._get_multiple_to_dict(ENERGY_STORAGE_CONFIGURATION_PARAMETERS_1))
                result.update(await self._get_multiple_to_dict(ENERGY_STORAGE_CONFIGURATION_PARAMETERS_2))
                result.update(await self._get_multiple_to_dict(ENERGY_STORAGE_CONFIGURATION_PARAMETERS_3))

                # We have no way of knowing if a backup box is installed, so always fetch these registers
                result.update(await self._get_multiple_to_dict(BACKUP_POWER_REGISTERS))
            if self.supports_capacity_control:
                result.update(await self._get_multiple_to_dict(CAPACITY_CONTROL_REGISTERS))
        return result

    async def _read_file(self, file_type, customized_data=None) -> bytes:
        """
        Wraps `get_file` from `AsyncHuaweiSolar` in a retry-logic for when
        the login-sequence needs to be repeated.
        """
        logged_in = await self.ensure_logged_in()

        if not logged_in:
            _LOGGER.warning("Could not login, reading file %x will probably fail.", file_type)

        try:
            return await self.client.get_file(file_type, customized_data, self.slave_id)
        except PermissionDenied as err:
            if self.__username:
                logged_in = self.ensure_logged_in(force=True)

                if not logged_in:
                    _LOGGER.error("Could not login to read file %x .", file_type)
                    raise err

                return await self.client.get_file(file_type, customized_data, self.slave_id)

            # we have no login-credentials available, pass on permission error
            raise err

    async def get_latest_optimizer_history_data(
        self,
    ) -> dict[int, OptimizerRealTimeData]:
        """Reads the latest Optimizer History Data File from the inverter"""

        # emulates behavior from FusionSolar app when current status of optimizers is queried
        end_time = (await self.client.get(rn.SYSTEM_TIME_RAW, self.slave_id)).value
        start_time = end_time - 600

        file_data = await self._read_file(
            OptimizerRealTimeDataFile.FILE_TYPE,
            OptimizerRealTimeDataFile.query_within_timespan(start_time, end_time),
        )
        real_time_data = OptimizerRealTimeDataFile(file_data)

        if len(real_time_data.data_units) == 0:
            return {}

        # we only expect one element, but if more would be present,
        # then only the latest one is of interest (list is sorted time descending)
        latest_unit = real_time_data.data_units[0]

        return {opt.optimizer_address: opt for opt in latest_unit.optimizers}

    async def get_optimizer_system_information_data(
        self,
    ) -> dict[int, OptimizerSystemInformation]:
        """Reads the Optimizer System Information Data File from the inverter"""
        file_data = await self._read_file(OptimizerSystemInformationDataFile.FILE_TYPE)
        system_information_data = OptimizerSystemInformationDataFile(file_data)

        return {opt.optimizer_address: opt for opt in system_information_data.optimizers}

    def _compute_pv_registers(self):
        """Get the registers for the PV strings which were detected from the inverter"""
        assert 1 <= self.pv_string_count <= 24

        self._pv_registers = []
        for idx in range(1, self.pv_string_count + 1):
            self._pv_registers.extend(
                [
                    getattr(rn, f"PV_{idx:02}_VOLTAGE"),
                    getattr(rn, f"PV_{idx:02}_CURRENT"),
                ]
            )

    async def stop(self):
        """Stop the bridge."""
        self.stop_heartbeat()

        if self._primary:
            return await self.client.stop()

        return True

    ############################
    # Everything write-related #
    ############################

    async def has_write_permission(self) -> t.Optional[bool]:
        """Tests write permission by getting the time zone and trying to write that same value back to the inverter"""

        try:
            time_zone = await self.client.get(rn.TIME_ZONE, self.slave_id)

            await self.client.set(rn.TIME_ZONE, time_zone.value, self.slave_id)
            return True
        except ReadException:
            # A ReadException can occur when connecting via a SmartLogger 3000A.
            # In that case, we do not support writing values at all.
            return None
        except PermissionDenied:
            return False

    async def ensure_logged_in(self, *, force=False):
        """
        Checks if it is necessary to login and performs the necessary login sequence if needed.
        """
        async with self.__login_lock:
            if force:
                _LOGGER.debug("Forcefully stopping any heartbeat task (if any is still running)")
                self.stop_heartbeat()

            if self.__username and not self.__heartbeat_enabled:
                _LOGGER.debug("Currently not logged in: logging in now and starting heartbeat")
                assert self.__password
                if not await self.client.login(self.__username, self.__password):
                    raise InvalidCredentials()

                self.start_heartbeat()

        return True

    async def login(self, username: str, password: str) -> bool:
        """Performs the login-sequence with the provided username/password."""
        async with self.__login_lock:
            if not await self.client.login(username, password, self.slave_id):
                raise InvalidCredentials()

            # save the correct login credentials
            self.__username = username
            self.__password = password
            self.start_heartbeat()

        return True

    def stop_heartbeat(self):
        """Stop the running heartbeat task (if any)"""
        self.__heartbeat_enabled = False

        if self.__heartbeat_task:
            self.__heartbeat_task.cancel()

    def start_heartbeat(self):
        """Start the heartbeat thread to stay logged in."""
        assert self.__login_lock.locked(), "Should only be called from within the login_lock!"

        if self.__heartbeat_task:
            self.stop_heartbeat()

        async def heartbeat():
            while self.__heartbeat_enabled:
                try:
                    self.__heartbeat_enabled = await self.client.heartbeat(self.slave_id)
                    await asyncio.sleep(HEARTBEAT_INTERVAL)
                except HuaweiSolarException as err:
                    _LOGGER.warning("Heartbeat stopped because of, %s", err)
                    self.__heartbeat_enabled = False

        self.__heartbeat_enabled = True
        self.__heartbeat_task = asyncio.create_task(heartbeat())

    async def set(self, name: str, value):
        """Sets a register to a certain value."""

        logged_in = await self.ensure_logged_in()  # we must login again before trying to set the value

        if not logged_in:
            _LOGGER.warning("Could not login, setting, %s will probably fail.", name)

        if self.__heartbeat_enabled:
            try:
                await self.client.heartbeat(self.slave_id)
            except HuaweiSolarException:
                _LOGGER.warning("Failed to perform heartbeat before write")

        try:
            return await self.client.set(name, value, slave=self.slave_id)
        except PermissionDenied as err:
            if self.__username:
                logged_in = await self.ensure_logged_in(force=True)

                if not logged_in:
                    _LOGGER.error("Could not login to set %s .", name)
                    raise err

                # Force a heartbeat first when connected with username/password credentials
                await self.client.heartbeat(self.slave_id)

                return await self.client.set(name, value, slave=self.slave_id)

            # we have no login-credentials available, pass on permission error
            raise err

    @property
    def battery_type(self) -> rv.StorageProductModel:
        """The battery type present on this inverter"""
        if self.battery_1_type != rv.StorageProductModel.NONE:
            return self.battery_1_type
        return self.battery_2_type


# Registers which should always be read
INVERTER_REGISTERS = [
    rn.INPUT_POWER,
    rn.LINE_VOLTAGE_A_B,
    rn.LINE_VOLTAGE_B_C,
    rn.LINE_VOLTAGE_C_A,
    rn.PHASE_A_VOLTAGE,
    rn.PHASE_B_VOLTAGE,
    rn.PHASE_C_VOLTAGE,
    rn.PHASE_A_CURRENT,
    rn.PHASE_B_CURRENT,
    rn.PHASE_C_CURRENT,
    rn.DAY_ACTIVE_POWER_PEAK,
    rn.ACTIVE_POWER,
    rn.REACTIVE_POWER,
    rn.POWER_FACTOR,
    rn.GRID_FREQUENCY,
    rn.EFFICIENCY,
    rn.INTERNAL_TEMPERATURE,
    rn.INSULATION_RESISTANCE,
    rn.DEVICE_STATUS,
    rn.FAULT_CODE,
    rn.STARTUP_TIME,
    rn.SHUTDOWN_TIME,
    rn.ACTIVE_POWER_FAST,
    rn.ACCUMULATED_YIELD_ENERGY,
    rn.TOTAL_DC_INPUT_POWER,
    rn.CURRENT_ELECTRICITY_GENERATION_STATISTICS_TIME,
    rn.HOURLY_YIELD_ENERGY,
    rn.DAILY_YIELD_ENERGY,
]

# State and alarm registers can be combined with PV String readout
STATE_AND_ALARM_REGISTERS = [
    rn.STATE_1,
    rn.STATE_2,
    rn.STATE_3,
    rn.ALARM_1,
    rn.ALARM_2,
    rn.ALARM_3,
]

# Registers that should be read if optimizers are present
OPTIMIZER_REGISTERS = [rn.NB_ONLINE_OPTIMIZERS]

# Registers that should be read if a power meter is present
POWER_METER_REGISTERS = [
    rn.METER_STATUS,
    rn.GRID_A_VOLTAGE,
    rn.GRID_B_VOLTAGE,
    rn.GRID_C_VOLTAGE,
    rn.ACTIVE_GRID_A_CURRENT,
    rn.ACTIVE_GRID_B_CURRENT,
    rn.ACTIVE_GRID_C_CURRENT,
    rn.POWER_METER_ACTIVE_POWER,
    rn.POWER_METER_REACTIVE_POWER,
    rn.ACTIVE_GRID_POWER_FACTOR,
    rn.ACTIVE_GRID_FREQUENCY,
    rn.GRID_EXPORTED_ENERGY,
    rn.GRID_ACCUMULATED_ENERGY,
    rn.GRID_ACCUMULATED_REACTIVE_POWER,
    rn.METER_TYPE,
    rn.ACTIVE_GRID_A_B_VOLTAGE,
    rn.ACTIVE_GRID_B_C_VOLTAGE,
    rn.ACTIVE_GRID_C_A_VOLTAGE,
    rn.ACTIVE_GRID_A_POWER,
    rn.ACTIVE_GRID_B_POWER,
    rn.ACTIVE_GRID_C_POWER,
]

# Registers that should be read if a battery is present
ENERGY_STORAGE_REGISTERS = [
    rn.STORAGE_STATE_OF_CAPACITY,
    rn.STORAGE_RUNNING_STATUS,
    rn.STORAGE_BUS_VOLTAGE,
    rn.STORAGE_BUS_CURRENT,
    rn.STORAGE_CHARGE_DISCHARGE_POWER,
    rn.STORAGE_TOTAL_CHARGE,
    rn.STORAGE_TOTAL_DISCHARGE,
    rn.STORAGE_CURRENT_DAY_CHARGE_CAPACITY,
    rn.STORAGE_CURRENT_DAY_DISCHARGE_CAPACITY,
]

# Covers registers 47075 - 47088 (maximum would be 47139)
ENERGY_STORAGE_CONFIGURATION_PARAMETERS_1 = [
    rn.STORAGE_MAXIMUM_CHARGING_POWER,
    rn.STORAGE_MAXIMUM_DISCHARGING_POWER,
    rn.STORAGE_CHARGING_CUTOFF_CAPACITY,
    rn.STORAGE_DISCHARGING_CUTOFF_CAPACITY,
    rn.STORAGE_WORKING_MODE_SETTINGS,
    rn.STORAGE_CHARGE_FROM_GRID_FUNCTION,
    rn.STORAGE_GRID_CHARGE_CUTOFF_STATE_OF_CHARGE,
]

# Covers registers 47200 - 47244 (maximum would be 47264)
ENERGY_STORAGE_CONFIGURATION_PARAMETERS_2 = [
    rn.STORAGE_FIXED_CHARGING_AND_DISCHARGING_PERIODS,
    rn.STORAGE_POWER_OF_CHARGE_FROM_GRID,
    rn.STORAGE_MAXIMUM_POWER_OF_CHARGE_FROM_GRID,
]

# Covers register 47255 - 47299 (maximum would be 47319)
ENERGY_STORAGE_CONFIGURATION_PARAMETERS_3 = [
    rn.STORAGE_TIME_OF_USE_CHARGING_AND_DISCHARGING_PERIODS,
    rn.STORAGE_EXCESS_PV_ENERGY_USE_IN_TOU,
]

CAPACITY_CONTROL_REGISTERS = [
    rn.STORAGE_CAPACITY_CONTROL_MODE,
    rn.STORAGE_CAPACITY_CONTROL_SOC_PEAK_SHAVING,
    rn.STORAGE_CAPACITY_CONTROL_PERIODS,
]

BACKUP_POWER_REGISTERS = [
    rn.STORAGE_BACKUP_POWER_STATE_OF_CHARGE,
]
