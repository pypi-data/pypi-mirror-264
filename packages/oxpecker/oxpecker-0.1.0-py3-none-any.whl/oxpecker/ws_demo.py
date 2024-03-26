import io
import json
import sys
import threading
from datetime import datetime


def on_message(ws, message):
    print("### websocket on_message ###")
    thread = threading.Thread(target=handle_message, args=(ws, message))
    thread.start()


def handle_message(ws, message):
    print("Received: " + message)
    biz_message = json.loads(message)
    event = biz_message.get("event")
    print("event: " + event)
    if event == "EVENT.RUN_PYTHON":
        script = biz_message.get("data")
        print("===exec script===: " + script)
        if script:
            try:
                output = io.StringIO()
                old_stdout = sys.stdout
                sys.stdout = output
                exec(script)
                sys.stdout = old_stdout
                captured_output = output.getvalue()
                print("===exec result output===: " + captured_output)
                output.close()
                biz_message["data"] = captured_output
            except Exception as e:
                print(f"发生异常：{e}")
                biz_message["data"] = repr(e)
        else:
            biz_message["data"] = "script is empty"
        ws.send(json.dumps(biz_message))
        return
    if event == "EVENT.TASK_FINISH":
        print("TODO task finish")


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print(f"### websocket close ###, at {datetime.now()}")


def on_open(ws):
    print(f"### websocket open ###，at {datetime.now()}")


# def start_heartbeat(ws):
#     def run():
#         count = 0
#         while True:
#             time.sleep(30)
#             count += 1
#             print(f"### heartbeat {count} ###")
#             ws.send(json.dumps({"event": "EVENT.HEARTBEAT.PING"}))
#
#     thread = threading.Thread(target=run)
#     thread.start()
