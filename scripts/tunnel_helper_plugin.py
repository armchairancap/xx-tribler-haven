"""
This script enables you to start a tunnel helper headless.
"""
from __future__ import absolute_import

import argparse
import logging
import os
import re
import signal
import sys
import time
from socket import inet_aton
from asyncio import get_event_loop, ensure_future, sleep

from Tribler.Core.Config.tribler_config import TriblerConfig
from Tribler.Core.Session import Session
from Tribler.Core.simpledefs import NTFY_REMOVE, NTFY_TUNNEL
from Tribler.pyipv8.ipv8.taskmanager import TaskManager

logger = logging.getLogger(__name__)


class PortAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 0 < values < 2**16:
            raise argparse.ArgumentError(self, "Invalid port number")
        setattr(namespace, self.dest, values)


class IPAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            inet_aton(val)
        except:
            raise argparse.ArgumentError(self, "Invalid IPv4 address")
        setattr(namespace, self.dest, values)


class IPPortAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parsed = re.match(r"^([\d\.]+)\:(\d+)$", val)
        if not parsed:
            raise argparse.ArgumentError("Invalid address:port")

        ip, port = parsed.group(1), int(parsed.group(2))
        try:
            inet_aton(ip)
        except:
            raise argparse.ArgumentError("Invalid server address")

        if not (0 < port < 65535):
            raise argparse.ArgumentError("Invalid server port")
        setattr(namespace, self.dest, values)


class TunnelHelperService(TaskManager):

    def __init__(self):
        super(TunnelHelperService, self).__init__()
        self._stopping = False
        self.log_circuits = False
        self.session = None
        self.community = None

    def on_circuit_reject(self, reject_time, balance):
        with open(os.path.join(self.session.config.get_state_dir(), "circuit_rejects.log"), 'a') as out_file:
            time_millis = int(round(reject_time * 1000))
            out_file.write("%d,%d\n" % (time_millis, balance))

    def tribler_started(self):
        async def signal_handler(sig):
            print("Received shut down signal %s" % sig)
            if not self._stopping:
                self._stopping = True
                await self.session.shutdown()
                get_event_loop().stop()

        signal.signal(signal.SIGINT, lambda sig, _: ensure_future(signal_handler(sig)))
        signal.signal(signal.SIGTERM, lambda sig, _: ensure_future(signal_handler(sig)))

        self.register_task("bootstrap",  self.session.lm.tunnel_community.bootstrap, interval=30)

        # Remove all logging handlers
        root_logger = logging.getLogger()
        handlers = root_logger.handlers
        for handler in handlers:
            root_logger.removeHandler(handler)
        logging.getLogger().setLevel(logging.ERROR)

        new_strategies = []
        with self.session.lm.ipv8.overlay_lock:
            for strategy, target_peers in self.session.lm.ipv8.strategies:
                if strategy.overlay == self.session.lm.tunnel_community:
                    new_strategies.append((strategy, -1))
                else:
                    new_strategies.append((strategy, target_peers))
            self.session.lm.ipv8.strategies = new_strategies

    def circuit_removed(self, _, __, circuit, additional_info):
        self.session.lm.ipv8.network.remove_by_address(circuit.peer.address)
        if self.log_circuits:
            with open(os.path.join(self.session.config.get_state_dir(), "circuits.log"), 'a') as out_file:
                duration = time.time() - circuit.creation_time
                out_file.write("%d,%f,%d,%d,%s\n" % (circuit.circuit_id, duration, circuit.bytes_up, circuit.bytes_down,
                                                     additional_info))

    async def start(self, options):
        # Determine ipv8 port
        ipv8_port = options.ipv8_port
        if ipv8_port == -1 and "HELPER_INDEX" in os.environ and "HELPER_BASE" in os.environ:
            base_port = int(os.environ["HELPER_BASE"])
            ipv8_port = base_port + int(os.environ["HELPER_INDEX"]) * 5

        config = TriblerConfig()
        config.set_state_dir(os.path.join(config.get_state_dir(), "tunnel-%d") % ipv8_port)
        config.set_tunnel_community_socks5_listen_ports([])
        config.set_tunnel_community_random_slots(options.random_slots)
        config.set_tunnel_community_competing_slots(options.competing_slots)
        config.set_torrent_checking_enabled(False)
        config.set_ipv8_enabled(True)
        config.set_libtorrent_enabled(False)
        config.set_video_server_enabled(False)
        config.set_ipv8_port(ipv8_port)
        config.set_ipv8_address(options.ipv8_address)
        config.set_trustchain_enabled(True)
        config.set_credit_mining_enabled(False)
        config.set_market_community_enabled(False)
        config.set_dht_enabled(True)
        config.set_tunnel_community_exitnode_enabled(bool(options.exit))
        config.set_popularity_community_enabled(False)
        config.set_testnet(bool(options.testnet))
        config.set_chant_enabled(False)
        config.set_bootstrap_enabled(False)

        if not options.no_rest_api:
            config.set_http_api_enabled(True)
            api_port = options.restapi
            if "HELPER_INDEX" in os.environ and "HELPER_BASE" in os.environ:
                api_port = int(os.environ["HELPER_BASE"]) + 10000 + int(os.environ["HELPER_INDEX"])
            config.set_http_api_port(api_port)

        if options.ipv8_bootstrap_override is not None:
            config.set_ipv8_bootstrap_override(options.ipv8_bootstrap_override)

        self.session = Session(config)

        self.log_circuits = options.log_circuits
        # Register reject event handler if set
        if options.log_rejects:
            self.session.lm.tunnel_community.reject_callback = self.on_circuit_reject
        self.session.notifier.add_observer(self.circuit_removed, NTFY_TUNNEL, [NTFY_REMOVE])

        await self.session.start()
        self.tribler_started()
        
    async def stop(self):
        await self.shutdown_task_manager()
        if self.session:
            return self.session.shutdown()


def main(argv):
    parser = argparse.ArgumentParser(add_help=False, description=('Tunnel helper script, starts a (hidden) tunnel as a service'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    parser.add_argument('--ipv8_port', '-d', default=-1, type=int, help='IPv8 port', action=PortAction, metavar='{0..65535}')
    parser.add_argument('--ipv8_address', '-i', default='0.0.0.0', type=str, help='IPv8 listening address', action=IPAction)
    parser.add_argument('--ipv8_bootstrap_override', '-b', default=None, type=str, help='Force the usage of specific IPv8 bootstrap server (ip:port)', action=IPPortAction)
    parser.add_argument('--restapi', '-p', default=8085, type=str, help='Use an alternate port for the REST API', action=PortAction, metavar='{0..65535}')
    parser.add_argument('--random_slots', '-r', default=10, type=int, help='Specifies the number of random slots')
    parser.add_argument('--competing_slots', '-c', default=20, type=int, help='Specifies the number of competing slots')
    
    parser.add_argument('--exit', '-x', action='store_const', default=False, const=True, help='Allow being an exit-node')
    parser.add_argument('--testnet', '-t', action='store_const', default=False, const=True, help='Join the testnet')
    parser.add_argument('--no-rest-api', '-a', action='store_const', default=False, const=True, help='Disable the REST api')
    parser.add_argument('--log-rejects', action='store_const', default=False, const=True, help='Log rejects')
    parser.add_argument('--log-circuits', action='store_const', default=False, const=True, help='Log information about circuits')

    args = parser.parse_args(sys.argv[1:])    
    service = TunnelHelperService()
    
    loop = get_event_loop()
    coro = service.start(args)
    ensure_future(coro)
    
    if sys.platform == 'win32':
        # Unfortunately, this is needed on Windows for Ctrl+C to work consistently.
        # Should no longer be needed in Python 3.8.
        async def wakeup():
            while True:
                await sleep(1)
        ensure_future(wakeup())
    
    loop.run_forever()


if __name__ == "__main__":
    main(sys.argv[1:])
