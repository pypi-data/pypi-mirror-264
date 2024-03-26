# USBL Republisher TCP

This is a simple Python script to publish USBL data through LCM subscribing to a TCP connection.

Author: Sebastián Rodríguez, [srodriguez@mbari.org](mailto:srodriguez@mbari.org)

## Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
cd lcm-tools/build/bin
./lcm_tools_tcp_usbl --ip <ip-addresse> --port <port> --channel <channel>  --timeout<timeout>
```

### Example

```bash
cd lcm-tools/build/bin
./lcm_tools_tcp_usbl --ip 192.168.1.90 --port 22 --channel WINFROG_USBL --timeout 60
```
