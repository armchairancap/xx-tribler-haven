from tribler_core.components.restapi import RestfulComponent
from tribler_core.components.upgrade import UpgradeComponent
from tribler_core.modules.resource_monitor.core import CoreResourceMonitor


class ResourceMonitorComponent(RestfulComponent):
    resource_monitor: CoreResourceMonitor = None

    async def run(self):
        await super().run()
        await self.get_component(UpgradeComponent)

        config = self.session.config
        notifier = self.session.notifier

        log_dir = config.general.get_path_as_absolute('log_dir', config.state_dir)
        resource_monitor = CoreResourceMonitor(state_dir=config.state_dir,
                                               log_dir=log_dir,
                                               config=config.resource_monitor,
                                               notifier=notifier)
        resource_monitor.start()
        self.resource_monitor = resource_monitor

        await self.init_endpoints(endpoints=['debug'], values={'resource_monitor': resource_monitor})

    async def shutdown(self):
        await super().shutdown()
        if self.resource_monitor:
            await self.resource_monitor.stop()