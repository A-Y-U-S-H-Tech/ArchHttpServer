"""
Multithreading Verification Test for Custom HTTP Server
=======================================================

Purpose
-------
This program experimentally verifies whether your server:

1. Handles clients concurrently
2. Creates overlapping request execution
3. Blocks sequentially or not

How It Works
------------
Each client:
    - connects simultaneously
    - sends GET request
    - waits for response
    - measures response completion time

IMPORTANT SERVER SETUP
----------------------
Inside your server request pipeline temporarily add:

    import time
    time.sleep(5)

Example:

    def HTTPpipeline(self):
        time.sleep(5)
        ...

Expected Results
----------------

If SINGLE-THREADED:
    Total test time ≈ CLIENTS × 5 sec

If MULTITHREADED:
    Total test time ≈ 5-8 sec total

because all requests overlap.

Run
---
python3 test_threading.py
"""

import socket
import threading
import time

# ============================================================
# CONFIG
# ============================================================

HOST = "10.12.131.251"
PORT = 8080

CLIENTS = 4000

# ============================================================
# RESULTS
# ============================================================

results = []
lock = threading.Lock()

# ============================================================
# CLIENT TASK
# ============================================================

def worker(client_id: int):

    start = time.perf_counter()

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))

        request = (
            "GET /test.html HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        sock.sendall(request.encode())

        data = b""

        while True:

            chunk = sock.recv(4096)

            if not chunk:
                break

            data += chunk

        end = time.perf_counter()

        sock.close()

        with lock:
            results.append({
                "id": client_id,
                "success": True,
                "time": end - start,
                "bytes": len(data)
            })

    except Exception as e:

        end = time.perf_counter()

        with lock:
            results.append({
                "id": client_id,
                "success": False,
                "time": end - start,
                "error": str(e)
            })

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("HTTP SERVER MULTITHREADING TEST")
    print("=" * 60)

    print(f"Target : {HOST}:{PORT}")
    print(f"Clients: {CLIENTS}")
    print()

    threads = []

    total_start = time.perf_counter()

    # --------------------------------------------------------
    # CREATE THREADS
    # --------------------------------------------------------

    for i in range(CLIENTS):

        t = threading.Thread(
            target=worker,
            args=(i,)
        )

        threads.append(t)

    # --------------------------------------------------------
    # START ALL CLIENTS NEAR-SIMULTANEOUSLY
    # --------------------------------------------------------

    for t in threads:
        t.start()

    # --------------------------------------------------------
    # WAIT
    # --------------------------------------------------------

    for t in threads:
        t.join()

    total_end = time.perf_counter()

    # ========================================================
    # ANALYSIS
    # ========================================================

    success = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print("\nRESULTS")
    print("-" * 60)

    print(f"Successful : {len(success)}")
    print(f"Failed     : {len(failed)}")

    print()

    if success:

        times = [r["time"] for r in success]

        print(f"Fastest    : {min(times):.3f} sec")
        print(f"Slowest    : {max(times):.3f} sec")
        print(f"Average    : {sum(times)/len(times):.3f} sec")

    print()
    print(f"TOTAL TEST TIME: {(total_end-total_start):.3f} sec")

    # ========================================================
    # INTERPRETATION
    # ========================================================

    print("\nINTERPRETATION")
    print("-" * 60)

    total = total_end - total_start

    if total < 10:
        print("Server appears MULTITHREADED.")
        print("Requests overlapped concurrently.")

    elif total < CLIENTS * 5:
        print("Partial concurrency detected.")

    else:
        print("Server appears SEQUENTIAL / SINGLE-THREADED.")

    # ========================================================
    # FAILURES
    # ========================================================

    if failed:

        print("\nFAILURES")
        print("-" * 60)

        for r in failed:
            print(
                f"Client {r['id']} -> {r['error']}"
            )

# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    main()