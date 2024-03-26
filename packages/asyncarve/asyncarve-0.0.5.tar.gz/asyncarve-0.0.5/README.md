# Python: Arve API Client

Asynchronous Python client for the Arve API.

## About

This package allows you to acquire the latest measurement data and information about the device programmatically.
It is mainly created to allow third-party programs to get and display the measurements of the device.

An example of this might be Home Assistant.

## Installation

```bash
pip install asyncarve
```

## Usage

```python
from asyncarve import Arve
import asyncio


async def main() -> None:
    async with Arve("249e597c-e0cc-436e-abbd-867d61d6c5a9", "73bdb639-a454-4f9e-879c-793ee39bb268",
                    "A0120-0000-0000-1798") as arv_cl:
        data = await arv_cl.get_sensor_info()

        print(data)


if __name__ == "__main__":
    asyncio.run(main())

```

## Additional requirements

This package relies on `orjson`, `mashumaro`, `aiohttp` and `yarl` packages.
