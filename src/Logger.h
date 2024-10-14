#include <LittleFS.h>
#include <WebSocketsServer.h>

#pragma once

// Initialize the WebSocket server on port 82
WebSocketsServer webSocketVarLog = WebSocketsServer(82);

void logData(String data)
{
  File logFile = LittleFS.open("/log.txt", "a");
  if (!logFile)
  {
    Serial.println("Failed to open log file");
    return;
  }
  logFile.println(data);
  logFile.close();
}

void clearLogs()
{
  LittleFS.remove("/log.txt"); // Delete the log file to start fresh
}

void sendRealTimeData(String data)
{
  logData(data);                      // Log data to LittleFS
  webSocketVarLog.broadcastTXT(data); // Send real-time data to all connected clients
}

void sendLogsToClient(uint8_t clientID)
{
  File logFile = LittleFS.open("/log.txt", "r");
  if (!logFile)
  {
    Serial.println("Failed to open log file");
    return;
  }

  while (logFile.available())
  {
    String logEntry = logFile.readStringUntil('\n');
    webSocketVarLog.sendTXT(clientID, logEntry); // Send each line to the client
  }
  logFile.close();
}

void onWebSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length)
{
  if (type == WStype_CONNECTED)
  {
    // When a client connects, send historical log
    sendLogsToClient(num);

    // Clear the log after sending
    clearLogs();
  }
}
