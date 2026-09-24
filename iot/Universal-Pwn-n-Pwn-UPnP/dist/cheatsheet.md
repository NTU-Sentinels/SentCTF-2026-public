# Cheatsheet for UPnP challenge

## Resources

1. **UPnP overview**: https://upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.0-20080424.pdf

2. **UPnP technical basics**: https://upnp.org/resources/documents/UPnP_UDA_tutorial_July2014.pdf

## UPnP basics

### Simple Service Discovery Protocol (SSDP)

- **Role**: discovery mechanism
- **Function**: allows a new device to announce its presence to the network or a control point to search for available devices (via requests over UDP/1900)
- **Output**: returns basic device info and a pointer (URL) to the root device description file
- this request will usually be multicast, but we will be using a unicast in this challenge (directly to the challenge server)

### Service Control Protocol Description (SCPD)

- **Role**: The service description mechanism.
- **Function**: An XML-based file fetched during a later phase of a UPnP session to inspect a specific service
- **Output**: Details the exact list of actions, arguments, and state variables available for that service, acting similarly to an API definition before commands are sent via SOAP

### 1. SSPD request

**A SSDP request will look like (UDP/1900)**:

> Due to certain limitations with the server infrastructure, it will be running on TCP/1900 instead. Don't worry about this, as the provided `m-search.py` script handles this

```http
M-SEARCH * HTTP/1.1
HOST: <TARGET-IP>:1900
MAN: "ssdp:discover"
MX: 2
ST: ssdp:all
```

- replace `<TARGET-IP>` with the target IP address

**Example response**:

```http
HTTP/1.1 200 OK
LOCATION: http://<TARGET-IP>:5000/device.xml
ST: upnp:rootdevice
USN: uuid:sentinel-gateway::upnp:rootdevice
```

- take note of the `LOCATION` field
- this value URL will be used to retrieve `device.xml` in the next step (via a GET request)

You may use the provided `m-search.py` script to send the M-SEARCH request:

> modify the `TARGET` variable in the provided script

```shell
python3 m-search.py
```

### 2. GET device.xml

Contains the following important information:

- `URLBase`
- `SCPDURL`
- `controlURL`
- `eventSubURL`

**GET /device.xml (TCP/5000 - from previous response)**:

```shell
curl http://TARGET-IP:5000/device.xml
```

- replace `TARGET-IP` with the target IP address

**Example response**:

```xml
<URLBase>http://TARGET-IP:5000/</URLBase>

<device>
    <deviceType>
            urn:schemas-upnp-org:device:InternetGatewayDevice:1
    </deviceType>

    <service>
        <serviceType>
            urn:sentinel-org:service:DeviceConfig:1
        </serviceType>

        <serviceId>
            urn:sentinel-org:serviceId:DeviceConfig
        </serviceId>

        <SCPDURL>
            /deviceconfig.xml
        </SCPDURL>

        <controlURL>
            /upnp/control/deviceconfig
        </controlURL>

        <eventSubURL>
            /upnp/event/deviceconfig
        </eventSubURL>
    </service>

    </device>
```

- `URLBase` -> **http://TARGET-IP:5000/**
- `SCPDURL` -> **/deviceconfig.xml**
- `controlURL` -> **/upnp/control/deviceconfig**
- `eventSubURL` -> **/upnp/event/deviceconfig** (NOT used)

### 3. GET deviceconfig.xml

Send a HTTP GET request to the `URLBase` + `SCDPURL` found earlier:

```shell
curl http://TARGET-IP:5000/deviceconfig.xml
```

**Example response**:

```xml
<scpd xmlns="urn:schemas-upnp-org:service-1-0">

    <actionList>
        <action>
            <name>X</name>

            <argumentList>
                <argument>
                    <name>Status</name>
                    <direction>out</direction>
                    <relatedStateVariable>Status</relatedStateVariable>
                </argument>
            </argumentList>

        </action>
        <action>
            <name>Y</name>

            <argumentList>
                <argument>
                    <name>Target</name>
                    <direction>in</direction>
                    <relatedStateVariable>Target</relatedStateVariable>
                </argument>

                <argument>
                    <name>Result</name>
                    <direction>out</direction>
                    <relatedStateVariable>Result</relatedStateVariable>
                </argument>
            </argumentList>

        </action>
    </actionList>

    <serviceStateTable>

        <stateVariable sendEvents="no">
            <name>Status</name>

            <dataType>string</dataType>

        </stateVariable>

        <stateVariable sendEvents="no">
            <name>Target</name>

            <dataType>string</dataType>

             <allowedValueList>
                <allowedValue>bits</allowedValue>
                <allowedValue>bytes</allowedValue>
            </allowedValueList>

        </stateVariable>

    </serviceStateTable>

</scpd>
```

Contains the following important information:

> An arrow (->) will be used to indicate nested levels of tags within the XML

> eg. a -> b -> c indicates that is nested within b, and b is nested within a

- `action.name` (actionList -> action -> name)
  - used in SOAP request later on
- `argument.name` (actionlist -> action -> argumentList -> name)
  - used in SOAP request later on
- `argument.direction` (actionlist -> action -> argumentList -> direction)
  - indicates if its an argument to be sent, or retrieved from the server
- `argument.relatedStateVariable` (actionlist -> action -> argumentList -> relatedStateVariable)
  - we can look for this value in the `stateVariable.name` down below

- `stateVariable.name` (serviceStateTable -> stateVariable -> name)
- `stateVariable.dataType` (serviceStateTable -> stateVariable -> dataType)
- `stateVariable.allowedValueList` (serviceStateTable -> stateVariable -> allowedValueList)

### 4. Enumerate SOAP actions

From the `deviceconfig.xml` response, we can see 2 different possible actions: **X** and **Y**

- the corresponding arguments are **Status**, **Target** + **Result** respectively
- from the nested values under `serviceStateTable`, we know:
  - **Status** -> string
  - **Target** -> string ("bits" or "bytes")

### 5. Send POST SOAP requests

We can now send a SOAP request to the path we retrieved from `controlURL` previously (**/upnp/control/deviceconfig**)

- this will be handled by the script

With the `soap.py` script:

```shell
python3 soap.py HOST --port PORT --action ACTION --arg FIELD=VALUE
# eg.
python3 soap.py TARGET-IP --port 5000 --action Y --arg Target=bytes
```

**Example response**:

```xml
Status: 200
<?xml version="1.0"?>
<s:Envelope
    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
    s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">

    <s:Body>
        <u:Y
            xmlns:u="urn:schemas-upnp-org:service:DeviceConfig:1">
            <Result>Y successfully set to bytes!</Result>
        </u:Y>
    </s:Body>

</s:Envelope
```

## Python UPnP tools

> Overview of tools usage

```shell
# M-SEARCH
python3 m-search.py


# SOAP request
python3 soap.py HOST --help
python3 soap.py HOST --port PORT --action ACTION --arg FIELD=VALUE
...

```
