import oca
import time

from exceptions import LCMStateWaitingTimedOut, StateWaitingTimedOut


def boot(vm, do_not_wait_for_running_lsm_state=False):
    vm.client.call("vm.action", "boot", vm.id)
    if do_not_wait_for_running_lsm_state:
        # wait till lcm_state = Running
        wait_for_lcm_state(vm, 3)


def reboot(vm):
    vm.client.call("vm.action", "reboot", vm.id)


def get_vm(client, id):
    vm_pool = oca.VirtualMachinePool(client)
    vm_pool.info()
    for vm in vm_pool:
        if vm.id == id:
            return vm


def get_lcm_state(vm):
    vm = get_vm(vm.client, vm.id)
    return vm.lcm_state


def get_state(vm):
    vm = get_vm(vm.client, vm.id)
    return vm.state


def wait_for_lcm_state(vm, desired_state_id, time_out=60, period=5):
    """
    Wait till VM gets lcm_state with specified id
    """
    _wait_for_state(vm, desired_state_id, 'lcm_state', time_out,
                    period)


def wait_for_state(vm, desired_state_id, time_out=60, period=5):
    """
    Wait till VM gets state with specified id
    """
    _wait_for_state(vm, desired_state_id, 'state', time_out, period)


def _wait_for_state(vm, desired_state_id, state_type, time_out=60,
                    period=5):
    class _IncorrerectStateType(Exception):
        def __str__(self):
            return "state_type must equal 'lcm_state' or 'state'. However {}" \
                   "was specified".format(state_type)
    lcm_state, state = False, False
    if state_type == 'lcm_state':
        lcm_state = True
    elif state_type == 'state':
        state = True
    else:
        raise _IncorrerectStateType()
    end = time.time() + time_out
    current_state_id = "wasn't get"
    while time.time() < end:
        if lcm_state:
            current_state_id = get_lcm_state(vm)
        if state:
            current_state_id = get_state(vm)
        if current_state_id == desired_state_id:
            return
        time.sleep(period)
    if lcm_state:
        raise LCMStateWaitingTimedOut(desired_state_id, current_state_id)
    if state:
        raise StateWaitingTimedOut(desired_state_id, current_state_id)


def revert_disk_snapshot(vm, disk_id, snapshot_id):
    # If vm state != "Power off"
    if get_state(vm) != 8:
        vm.poweroff()
        wait_for_state(vm, 8, time_out=600)
    vm.client.call("vm.disksnapshotrevert", vm.id, disk_id, snapshot_id)
    wait_for_state(vm, 8, time_out=600)
    vm.resume()
    wait_for_state(vm, 3)


def client_from_file(path="/home/denis/credentials/nebula_credentials"):
    with open(path, "r") as f:
        secret, address = (st for st in f)
        return oca.Client(secret, address)