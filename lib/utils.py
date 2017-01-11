def store_or_user_vm_id(vm_id):
    if not vm_id:
        with open("last_vm_id") as f:
            vm_id = int(f.read())
    else:
        vm_id = int(vm_id)
        with open("last_vm_id", 'w') as f:
            f.write(str(vm_id))
    return vm_id
