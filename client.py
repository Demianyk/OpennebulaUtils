import click
from utils.opennebula_utils import get_vm, revert_disk_snapshot, \
    client_from_file

CLIENT = client_from_file()


@click.group()
def client():
    pass


@client.command()
@click.option('--vm-id', default=40997, help='ID of VM you want ro revert')
@click.option('--sn-id', default=0,
              help='ID of snapshot you want to revert to')
def revert(vm_id, sn_id):
    vm = get_vm(CLIENT, vm_id)
    click.echo("You are about to revert VM {} to state {}".format(vm_id,
                                                                  sn_id))
    revert_disk_snapshot(vm, 0, sn_id)


def recreate():
    pass


def main():
    client()


if __name__ == '__main__':
    main()
