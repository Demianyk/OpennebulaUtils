import click
from copy import deepcopy

from lib.opennebula_utils import get_vm, revert_disk_snapshot, \
    client_from_file
from lib.utils import store_or_user_vm_id


class _Snapshot:
    def __init__(self, node):
        self.name = node.find("NAME").text
        self.id = node.find("ID").text
        self.parent = node.find("PARENT").text
        self.children = []
        self.level = 0

    def __repr__(self):
        info = "{}{}, id: {}".format("\t" * self.level, self.name, self.id)
        for child in self.children:
            info += "\n" + child.__repr__()
        return info

    def increase_level(self, parent_level):
        self.level = parent_level + 1
        for child in self.children:
            child.increse_level()

    def find_children(self, possible_children):
        for child in possible_children:
            if child.parent == self.id:
                child.increase_level(self.level)
                self.children.append(child)
                possible_children.remove(child)
                child.find_children(possible_children)

CLIENT = client_from_file()


@click.group()
def client():
    pass


@client.command()
@click.option('--vm-id', default=None, help='ID of VM you want ro revert')
@click.option('--sn-id', default=0,
              help='ID of snapshot you want to revert to')
def revert(vm_id, sn_id):
    vm_id = store_or_user_vm_id(vm_id)
    vm = get_vm(CLIENT, vm_id)
    click.echo("You are about to revert VM {} to state {}".format(vm_id,
                                                                  sn_id))
    revert_disk_snapshot(vm, 0, sn_id)


@client.command()
@click.option('--vm-id', default=None, help='ID of VM you want ro view')
def snapshots(vm_id):
    vm_id = store_or_user_vm_id(vm_id)
    vm = get_vm(CLIENT, vm_id)

    snapshots_node = vm.xml.find("SNAPSHOTS")
    snaps = []
    for snapshot_node in snapshots_node:
        if snapshot_node.tag == "SNAPSHOT":
            snaps.append(_Snapshot(snapshot_node))
    snapshots_without_parents = deepcopy(snaps)
    for snapshot in snaps:
        snapshot.find_children(snapshots_without_parents)
    for snapshot in snaps:
        if len(snapshot.children) > 0:
            print snapshot
    print(len(snapshots_without_parents))


def recreate():
    pass


if __name__ == '__main__':
    client()

