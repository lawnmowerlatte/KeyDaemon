#include <Keyboard.h>
#include <Mouse.h>
#include <SoftwareSerial.h>

const byte rxPin = 10;
const byte txPin = 11;

int state = 0;
String readLine;
String nextLine;
int char_delay = 50;

SoftwareSerial softSerial (rxPin, txPin);

void(* reset) (void) = 0;

void setup() {
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  
  Keyboard.begin();
  Mouse.begin();
  Serial.begin(115200);

  delay(2000);
  Serial.println("Ready, waiting for Wifi");
  
  softSerial.begin(9600);
  
  Serial.println(readLine);
  while (readLine != "OK") {
    receiveCommand();
  }

  readLine = "";

  while (readLine == "") {
    receiveCommand();
  }
  
  readLine = "";
}

void receiveCommand() {
  while (softSerial.available()) {
    char c = (char)softSerial.read();
    
    if (c == 10) {
      readLine = nextLine;
      Serial.println(readLine);
      nextLine = "";
      if (readLine == F("RESTART")) {
        Serial.println(F("Resetting..."));
        delay(1000); 
        reset();
      }
    } else if (c == 13) {
      ;
    } else {
      nextLine += c;
    }
  }
}

void set_state(String parameters) {
  Serial.println("Changing state");
  
  if (parameters == "on") {
    state = 1;
    Serial.println("Starting chaos");
  } else if (parameters == "off") {
    state = 0;
    Serial.println("Offering a reprive");
  }
}

void set_delay(String parameters) {
  Serial.println("Changing cooldown");

  char_delay = parameters.toInt();
}

void send_characters(String parameters) {
  Serial.print("Sending keys: ");
  Serial.println(parameters);

  for (int i = 0; i < parameters.length(); i++) {
    Keyboard.write(parameters[i]);
    
    if (parameters.length() > 1) {
      delay(char_delay);
    }
  }
}

void send_special(String parameters) {
  Serial.print("Sending special key: ");
  Serial.println(parameters);

  int special = parameters.toInt();

  Keyboard.write(special);
}

void press_special(String parameters) {
  Serial.print("Pressing special key: ");
  Serial.println(parameters);

  int special = parameters.toInt();

  Keyboard.press(special);
}

void release_special(String parameters) {
  Serial.print("Releasing special key: ");
  Serial.println(parameters);

  int special = parameters.toInt();

  Keyboard.release(special);
}


void press_key(String parameters) {
  Serial.print("Pressing key: ");
  Serial.println(parameters);

  char c = parameters[0];

  Keyboard.press(c);
}

void release_key(String parameters) {
  Serial.print("Releasing key: ");
  Serial.println(parameters);

  char c = parameters[0];

  Keyboard.release(c);
}

void mouse_click(String parameters) {
  Serial.print("Clicking button: ");
  Serial.println(parameters);

  if (parameters == "left") {
    Mouse.click(MOUSE_LEFT);
  } else if (parameters == "right") {
    Mouse.click(MOUSE_RIGHT);
  } else if (parameters == "left") {
    Mouse.click(MOUSE_MIDDLE);
  } 
}

void mouse_press(String parameters) {
  Serial.print("Pressing button: ");
  Serial.println(parameters);

  if (parameters == "left") {
    Mouse.press(MOUSE_LEFT);
  } else if (parameters == "right") {
    Mouse.press(MOUSE_RIGHT);
  } else if (parameters == "left") {
    Mouse.press(MOUSE_MIDDLE);
  } 
}

void mouse_release(String parameters) {
  Serial.print("Releasing button: ");
  Serial.println(parameters);

  if (parameters == "left") {
    Mouse.release(MOUSE_LEFT);
  } else if (parameters == "right") {
    Mouse.release(MOUSE_RIGHT);
  } else if (parameters == "left") {
    Mouse.release(MOUSE_MIDDLE);
  } 
}

void mouse_move(String parameters) {
  Serial.print("Moving mouse: ");
  Serial.println(parameters);

  String x = "";
  String y = "";
  String w = "";
  String tmp = "";

  int separator = parameters.indexOf(",");

  for (int i=0; i < parameters.length(); i++) {
    if (i < separator) {
      x += parameters[i];
    } else if (i > separator) {
      tmp += parameters[i];
    }
  }

  parameters = tmp;
  separator = parameters.indexOf(",");

  for (int i=0; i < parameters.length(); i++) {
    if (i < separator) {
      y += parameters[i];
    } else if (i > separator) {
      w += parameters[i];
    }
  }

  int X = x.toInt();
  int Y = y.toInt();
  int W = w.toInt();
  
  Mouse.move(X, Y, W);
}

void actOnCommand() {
  if (readLine == "") {
    return;
  }

  String command = "";
  String parameters = "";
  int separator = readLine.indexOf(" ");

  if (separator == 0) {
    separator = readLine.length();
  }

  for (int i=0; i < readLine.length() - 1; i++) {
    if (i < separator) {
      command += readLine[i];
    } else if (i > separator + 2) {
      parameters += readLine[i];
    }
  }
  
  // Switch based on command
  if (command == "set_state") {
    set_state(parameters);
  } else if (command == "send_special") {
    send_special(parameters);
  } else if (command == "press_special") {
    press_special(parameters);
  } else if (command == "release_special") {
    release_special(parameters);
  } else if (command == "press_key") {
    press_key(parameters);
  } else if (command == "release_key") {
    release_key(parameters);
  } else if (command == "set_delay") {
    set_delay(parameters);
  } else if (command == "send_characters") {
    send_characters(parameters);
  } else if (command == "mouse_click") {
    mouse_click(parameters);
  } else if (command == "mouse_press") {
    mouse_press(parameters);
  } else if (command == "mouse_release") {
    mouse_release(parameters);
  } else if (command == "mouse_move") {
    mouse_move(parameters);
  } else {
    Serial.println("Unknown command: " + command);
  }  
 
  readLine = "";
}

void loop() {
  receiveCommand();
  actOnCommand();
} 
