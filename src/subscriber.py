import asyncio

import nats
from __init__ import db
from event_handler import check_report_files
from kyso_event_enum import KysoEventEnum


async def app():

    async def disconnected_cb():
        print('Got disconnected!')

    async def reconnected_cb():
        print(f'Got reconnected to {nc.connected_url.netloc}')

    async def error_cb(e):
        print(f'There was an error: {e}')

    async def closed_cb():
        print('Connection is closed')

    nats_kyso_settings = db["KysoSettings"].find_one({
        "key": "KYSO_NATS_URL"
    })

    if nats_kyso_settings is None:
        raise Exception("KYSO_NATS_URL not found in KysoSettings collection.")

    nc = await nats.connect(nats_kyso_settings["value"],
                            error_cb=error_cb,
                            reconnected_cb=reconnected_cb,
                            disconnected_cb=disconnected_cb,
                            closed_cb=closed_cb,
                            )

    await nc.subscribe(KysoEventEnum.REPORTS_CREATE.value, f"{KysoEventEnum.REPORTS_CREATE.value}_queue", cb=check_report_files)
    await nc.subscribe(KysoEventEnum.REPORTS_NEW_VERSION.value, f"{KysoEventEnum.REPORTS_NEW_VERSION.value}_queue", cb=check_report_files)

    print(f"Listening for requests...")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app())
    loop.run_forever()
    loop.close()
