import asyncio
import websockets

async def get_sensor_value(ip, sensor_id, value_type="ActValue", index=0):
    uri = f"ws://{ip}/ghl-api/"
    command = f"Get Sensor[{sensor_id}] {value_type}[{index}]\n"

    try:
        async with websockets.connect(uri) as ws:
            await ws.recv()  # greeting
            await ws.recv()
            await ws.send(command)
            response = await ws.recv()

            if "ACK" in response:
                return float(response.split('<')[1].split('>')[0])
            return None
    except Exception:
        return None
