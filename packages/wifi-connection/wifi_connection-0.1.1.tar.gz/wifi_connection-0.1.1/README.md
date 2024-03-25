# Wi-Fi Connection 

This package provides commands to interact with Wi-Fi connections on your system.

## Installation

Install the `wifi_connection` package using pip:

```bash
pip install wifi_connection
```

## Usage
```python
import wifi_connection
```

## Functions

### `settings`

Enable or disable printing of results.

- **Parameters:**
  - `set_print`: Flag to enable/disable printing. (Optional, Default: True)

### `get_interfaces`

Get the list of available network interfaces.

- **Return Value:**
  - List of available network interfaces.

### `get_network_list`

Get the list of available networks for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)

- **Return Value:**
  - List of available networks.

### `set_profile`

Set a network profile for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)
  - `band`: Wireless band. (Required)
  - `ssid`: SSID of the network. (Required)
  - `pwd`: Password of the network. (Optional, ignore if the network does not require a password)
  - `auto`: Enable or disable automatic connection to the network. (Optional, Default: True)

- **Return Value:**
  - True if the profile is set successfully, False otherwise.

### `connect`

Connect to a network with the specified SSID using the specified interface.  
**If a profile for the network does not exist, make sure to first set the profile using `set_profile`.**

- **Parameters:**
  - `iface_name`: Interface name. (Required)
  - `ssid`: SSID of the network. (Required)

- **Return Value:**
  - True if the connection is successful, False otherwise.

### `refresh`

Refresh the list of available networks for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)

- **Return Value:**
  - True if the refresh is successful, False otherwise.

### `get_ssid`

Get the SSID of the connected network for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)

- **Return Value:**
  - SSID of the connected network, or an error if the interface is not connected to any network.

### `get_profile`

Get the Profile of the SSID network for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)
  - `profile_name`: Profile name. (Required)

- **Return Value:**
  - Profile content
