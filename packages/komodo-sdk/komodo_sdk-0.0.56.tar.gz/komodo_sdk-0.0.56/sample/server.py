from komodo.server.fast import prepare_fastapi_app
from sample.appliance import SampleAppliance

SERVER = prepare_fastapi_app(SampleAppliance())


def run_server():
    import uvicorn
    uvicorn.run(SERVER, host="127.0.0.1", port=8000)  # noinspection PyTypeChecker


if __name__ == '__main__':
    run_server()
