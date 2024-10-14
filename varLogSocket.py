#!/usr/bin/env python3

import asyncio
import websockets

async def connect():
    uri = "ws://turret.local:82"

    while True:
        try:
            print("Trying to connect to the WebSocket server...")
            async with websockets.connect(uri, timeout=10) as websocket:
                print("Connected to the WebSocket server")

                # Keep the connection alive and handle communication
                while True:
                    try:
                        # Example of sending a message periodically
                        #await websocket.send("Hello, Turret!")
                        #print("Message sent")

                        # Receiving a message (expecting a byte message)
                        response = await websocket.recv()
                        print(f"{response}")

#                        await asyncio.sleep(1)  # Delay between messages

                    except websockets.ConnectionClosedError as e:
                        print(f"Connection closed unexpectedly: {e}. Reconnecting...")
                        break  # Break the inner loop and reconnect

        except (websockets.InvalidURI, websockets.InvalidHandshake) as e:
            print(f"WebSocket error: {e}. Check the WebSocket URI or handshake.")
            return  # Exit if there's an unrecoverable issue

        except asyncio.TimeoutError:
            print("Connection timed out. Retrying in 5 seconds...")
            await asyncio.sleep(5)  # Wait before retrying

        except Exception as e:
            print(f"An unexpected error occurred: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)  # Wait before retrying

async def main():
    await connect()

# Run the main function
asyncio.get_event_loop().run_until_complete(main())

