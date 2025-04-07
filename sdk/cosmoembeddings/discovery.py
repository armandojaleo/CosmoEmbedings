"""
Node discovery implementation using UDP broadcast.
"""

import socket
import json
import threading
import time
from typing import Callable, Optional
from .node import NodeIdentity

class DiscoveryService:
    """
    Service for discovering other nodes in the network using UDP broadcast.
    """
    
    def __init__(self, port: int = 8091, broadcast_interval: float = 5.0):
        """Initialize the discovery service."""
        self.port = port
        self.broadcast_interval = broadcast_interval
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(('', port))
        self.running = False
        self.discovery_thread: Optional[threading.Thread] = None
        self.on_node_discovered: Optional[Callable[[NodeIdentity], None]] = None
        
    def start(self, identity: NodeIdentity, on_node_discovered: Callable[[NodeIdentity], None]) -> None:
        """Start the discovery service."""
        self.on_node_discovered = on_node_discovered
        self.running = True
        self.discovery_thread = threading.Thread(
            target=self._discovery_loop,
            args=(identity,),
            daemon=True
        )
        self.discovery_thread.start()
        
    def stop(self) -> None:
        """Stop the discovery service."""
        self.running = False
        if self.discovery_thread:
            self.discovery_thread.join()
        self.socket.close()
        
    def _discovery_loop(self, identity: NodeIdentity) -> None:
        """Main discovery loop that broadcasts identity and listens for other nodes."""
        while self.running:
            # Broadcast identity
            self._broadcast_identity(identity)
            
            # Listen for other nodes
            try:
                self.socket.settimeout(1.0)
                data, addr = self.socket.recvfrom(1024)
                if data:
                    try:
                        node_data = json.loads(data.decode('utf-8'))
                        if node_data.get('node_id') != identity.node_id:
                            discovered_node = NodeIdentity(**node_data)
                            if self.on_node_discovered:
                                self.on_node_discovered(discovered_node)
                    except json.JSONDecodeError:
                        continue
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error in discovery loop: {e}")
                continue
                
            time.sleep(self.broadcast_interval)
            
    def _broadcast_identity(self, identity: NodeIdentity) -> None:
        """Broadcast the node's identity to the network."""
        try:
            data = json.dumps(identity.__dict__).encode('utf-8')
            self.socket.sendto(data, ('<broadcast>', self.port))
        except Exception as e:
            print(f"Error broadcasting identity: {e}")
            
    def send_direct_message(self, identity: NodeIdentity, target_address: str, target_port: int) -> None:
        """Send a direct message to a specific node."""
        try:
            data = json.dumps(identity.__dict__).encode('utf-8')
            self.socket.sendto(data, (target_address, target_port))
        except Exception as e:
            print(f"Error sending direct message: {e}") 