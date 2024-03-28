import logging
from nicegui import app, ui, run
from ezlab.parameters import EZNODES, KVM, PVE
from ezinfra.vms import clone
from ezinfra import kvm, pve
from ezlab.utils import ezapp


logger = logging.getLogger("ezlab.ui.vms")

def pve_newvm_dialog():

    app.storage.user["busy"] = True

    templates = [
        x for x in pve.vms(ezapp.connection) if x["template"] and x["type"] == "qemu"
    ]
    # networks = pve.networks(ezapp.connection)
    storage = pve.storage(ezapp.connection)

    app.storage.user["busy"] = False

    # vm settings dialog
    with ui.dialog() as dialog, ui.card():
        template_selector = (
            ui.select(
                options=[x["name"] for x in templates],
                label="Template",
                # on_change=lambda e: set_template(e.value),
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[PVE], "template")
        )
        storage_selector = (
            ui.select(
                options=[
                    x["storage"]
                    for x in storage
                    # if x["node"] == app.storage.user["template"]["node"]
                ],
                label="Storage",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[PVE], "storage")
        )
        # network_selector = (
        #     ui.select(
        #         options=[
        #             x["sdn"]
        #             for x in networks
        #             # if x["node"] == app.storage.user["template"]["node"]
        #         ],
        #         label="Network",
        #     )
        #     .classes("w-full")
        #     .props("inline")
        #     .bind_value(app.storage.general[PVE], "network")
        # )

        bridge_selector = (
            ui.select(
                options=[
                    x["iface"]
                    for x in pve.bridges(ezapp.connection, app.storage.general[PVE]["template"])
                ],
                label="Bridge",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[PVE], "bridge")
        )

        eznode_selector = (
            ui.select(
                options=[x["name"] for x in EZNODES],
                label="Node Type",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[PVE], "eznode")
        )

        host_selector = (
            ui.input(label="VM Name", placeholder="ezvm")
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[PVE], "hostname")
        )

        firstip_selector = (
            ui.input(
                label="First IP",
                placeholder=app.storage.general["config"]["gateway"],
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[PVE], "firstip")
        )

        ui.button(
            "Create",
            on_click=lambda: dialog.submit(
                (
                    next(
                        (i for i in templates if i["name"] == template_selector.value),
                        None,
                    ),
                    next(
                        (i for i in storage if i["storage"] == storage_selector.value),
                        None,
                    ),
                    bridge_selector.value,
                    next(
                        (i for i in EZNODES if i["name"] == eznode_selector.value),
                        None,
                    ),
                    host_selector.value,
                    firstip_selector.value,
                )
            ),
        )

    return dialog


def kvm_newvm_dialog():
    # @ui.refreshable
    # def volume_selector():
    #     app.storage.user["busy"] = True
    #     vols = kvm.volumes(
    #         app.storage.general[KVM].get("pool", "default")
    #     )
    #     selector = (
    #         ui.select(
    #             options=vols,
    #             label="Base Image",
    #         )
    #         .classes("w-full")
    #         .props("inline")
    #         .bind_value(app.storage.general[KVM], "baseimg")
    #     )
    #     app.storage.user["busy"] = False
    #     return selector

    # select dialog
    with ui.dialog() as dialog, ui.card():

        app.storage.user["busy"] = True

        pools = kvm.pools()
        bridges = kvm.bridges()

        app.storage.user["busy"] = False

        pool = (
            ui.select(
                options=[p.name() for p in pools],
                label="Pool",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[KVM], "pool")
        )

        baseimg = (
            ui.select(
                options=kvm.volumes(app.storage.general[KVM].get("pool", "default")),
                label="Base Image",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[KVM], "baseimg")
        )
        

        bridge = (
            ui.select(
                options=bridges,
                label="Bridge",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[KVM], "bridge")
        )

        eznode_selector = (
            ui.select(
                options=[x["name"] for x in EZNODES],
                label="Node Type",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[KVM], "eznode")
        )

        host_selector = (
            ui.input(label="VM Name", placeholder="ezvm")
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[KVM], "hostname")
        )

        firstip_selector = (
            ui.input(
                label="First IP",
                placeholder="10.1.1.21",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(app.storage.general[KVM], "firstip")
        )

        ui.button(
            "Create",
            on_click=lambda: dialog.submit(
                (
                    pool.value,
                    baseimg.value,
                    bridge.value,
                    next(
                        (i for i in EZNODES if i["name"] == eznode_selector.value),
                        None,
                    ),
                    host_selector.value,
                    firstip_selector.value,
                )
            ),
        )
    return dialog


async def new_vm_ui():

    if app.storage.general["target"]["hve"] == PVE:
        dialog = pve_newvm_dialog()
    elif app.storage.general["target"]["hve"] == KVM:
        dialog = kvm_newvm_dialog()
    else:
        ui.notify("not implemented")

    resources = await dialog

    if resources and all(resources):
        vmcount = resources[3]["count"]

        app.storage.user["busy"] = True

        for count in range(vmcount):
            try:
                await run.io_bound(clone,
                    target=app.storage.general["target"]["hve"],
                    resources=resources,
                    settings=dict(app.storage.general["config"]),
                    vm_number=(
                        0 if vmcount == 1 else count + 1
                    ),  # start from 1 not 0, use 0 for single vm
                    dryrun=app.storage.general["config"].get("dryrun", True),
                )
            except Exception as error:
                ui.notify(error, type="negative")

        app.storage.user["busy"] = False

    else:
        ui.notify("VM creation cancelled", type="info")
