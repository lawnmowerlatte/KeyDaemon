#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid     = "ssid-goes-here";
const char* password = "password-goes-here";

ESP8266WebServer server(80);

String parse_restful() {
  String command = "";

  for (int i=1; i< server.uri().length(); i++) {
    command += server.uri()[i];
  }

  command += " ";

  for (uint8_t i=0; i<server.args(); i++){
    command += server.argName(i);

    if (server.arg(i).length() > 0) {
      command += "=" + server.arg(i);
    }

    command += " ";
  }

  Serial.println(command);
  return command;
}

void handle_root() {
  server.send(418, "text/plain", "I am an Arduino");
  delay(100);
}

void handle_all(){
  String message = "Command Sent\n\n";
  message = parse_restful();
  server.send(200, "text/plain", message);
}

void setup() {
  Serial.begin(9600);
  delay(3000);
 
  Serial.println();
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  
  Serial.println("OK");
  Serial.println(WiFi.localIP());

  server.on("/", handle_root);
  server.onNotFound(handle_all);
  server.begin();
}
 
void loop() {
  server.handleClient();
}
