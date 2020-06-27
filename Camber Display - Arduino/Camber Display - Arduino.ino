#include <WiFi.h>
#include <PubSubClient.h>
#include <GD23Z.h>
#include "default_assets.h"

#define INPUTCOUNT 7 //COUNT OF SENSOR INPUTS

const char* ssid =  "Camber";
const char* password = "12345678";
const char* mqtt_server = "10.3.141.1";

char sensordata[INPUTCOUNT][10];
char* config_data[5];//display mode,displayed data
int i1, i2, i3, i4;
int display_mode;
bool configuration = 0;
char* tags[INPUTCOUNT] = {"TWS","TWA","AWS","AWA","BS","HEEL","DPTH"};

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  if (strcmp(topic, "display/01/config") == 0) {
    sep_by_comma((char*)payload, config_data);
    i1 = *config_data[1] - '0';
    i2 = *config_data[2] - '0';
    i3 = *config_data[3] - '0';
    i4 = *config_data[4] - '0';
    display_mode = (int) * config_data[0] - '0';
    configuration = 1;
  }
  if (strcmp(topic, "wind/tws") == 0) {
    configuration = 0;
    for (int i = 0; i < length; i++) {
      sensordata[0][i] = (char)payload[i];
    }
    sensordata[0][length] = '\0';
  }
  if (strcmp(topic, "wind/twa") == 0) {
    configuration = 0;
    for (int i = 0; i < length; i++) {
      sensordata[1][i] = (char)payload[i];
    }
    sensordata[1][length] = '\0';
  }
  if (strcmp(topic, "wind/aws") == 0) {
    configuration = 0;
    for (int i = 0; i < length; i++) {
      sensordata[2][i] = (char)payload[i];
    }
    sensordata[2][length] = '\0';
  }
  if (strcmp(topic, "wind/awa") == 0) {
    configuration = 0;
    for (int i = 0; i < length; i++) {
      sensordata[3][i] = (char)payload[i];
    }
    sensordata[3][length] = '\0';
  }
  if (strcmp(topic, "boat/speed") == 0) {
    configuration = 0;
    for (int i = 0; i < length; i++) {
      sensordata[4][i] = (char)payload[i];
    }
    sensordata[4][length] = '\0';
  }
  if (strcmp(topic, "boat/heel") == 0) {
    configuration = 0;
    for (int i = 0; i < length; i++) {
      sensordata[5][i] = (char)payload[i];
    }
    sensordata[5][length] = '\0';
  }
  if (strcmp(topic, "boat/depth") == 0) {
    configuration = 0;
    for (int i = 0; i < length; i++) {
      sensordata[6][i] = (char)payload[i];
    }
    sensordata[6][length] = '\0';
  }

  GD.ClearColorRGB(0x000000);
  GD.Clear();

  GD.Begin(LINES);
  GD.Vertex2f(16 * 400, 0);
  GD.Vertex2f(16 * 400, 16 * 480);
  GD.End();

  GD.Begin(LINES);
  GD.Vertex2f(0, 16 * 240);
  GD.Vertex2f(16 * 800, 16 * 240);
  GD.End();

  GD.Begin(RECTS);
  GD.ColorRGB(0xFF0000);
  GD.Vertex2f(0, 0);
  GD.Vertex2f(250, 3801);
  GD.End();

  GD.Begin(RECTS);
  GD.ColorRGB(0x0000FF);
  GD.Vertex2f(0, 3878);
  GD.Vertex2f(250, 12800);
  GD.End();

  GD.Begin(RECTS);
  GD.ColorRGB(0x00FF00);
  GD.Vertex2f(12510, 3878);
  GD.Vertex2f(12800, 12800);
  GD.End();

  GD.Begin(RECTS);
  GD.ColorRGB(0xFF00FF);
  GD.Vertex2f(12510, 0);
  GD.Vertex2f(12800, 3801);
  GD.End();

  GD.ColorRGB(0xFFFFFF);

  switch (display_mode) {
    case 1:// 1 data displayed on screen
      if (configuration == 0) {
        display_data(i1, 0);
        GD.cmd_text(380, 36, BEBAS2_HANDLE, OPT_CENTERY | OPT_RIGHTX, tags[i1]);//top left
        GD.swap();
      }
      else {
        GD.cmd_text(565, 370, BEBAS_HANDLE, OPT_CENTER | OPT_RIGHTX, "00.0");
        GD.swap();
      }
      break;

    case 2:// 2 data displayed on screen
      if (configuration == 0) {
        display_data(i1, 0);
        display_data(i2, 1);
        GD.cmd_text(380, 36, BEBAS2_HANDLE, OPT_CENTERY | OPT_RIGHTX, tags[i1]);//top left
        GD.cmd_text(770, 36, BEBAS2_HANDLE, OPT_CENTERY | OPT_RIGHTX, tags[i2]);//top right
        GD.swap();
      }
      else {
        GD.cmd_text(565, 370, BEBAS_HANDLE, OPT_CENTER | OPT_RIGHTX, "00.0");
        GD.cmd_text(194, 127, BEBAS_HANDLE, OPT_CENTER | OPT_RIGHTX, "00.0");
        GD.swap();
      }
      break;
    case 4:// 4 data displayed on screen
      if (configuration == 0) {

        display_data(i1, 0);
        display_data(i2, 1);
        display_data(i3, 2);
        display_data(i4, 3);

        GD.cmd_text(380, 36, BEBAS2_HANDLE, OPT_CENTERY | OPT_RIGHTX, tags[i1]);//top left
        GD.cmd_text(770, 36, BEBAS2_HANDLE, OPT_CENTERY | OPT_RIGHTX, tags[i2]);//top right
        GD.cmd_text(380, 270, BEBAS2_HANDLE, OPT_CENTERY | OPT_RIGHTX, tags[i3]);//bottom left
        GD.cmd_text(770, 270, BEBAS2_HANDLE, OPT_CENTERY | OPT_RIGHTX, tags[i4]);//bottom right
        GD.swap();
      }
      else {
        GD.cmd_text(565, 370, BEBAS_HANDLE, OPT_CENTER | OPT_RIGHTX, "00.0");
        GD.cmd_text(194, 127, BEBAS_HANDLE, OPT_CENTER | OPT_RIGHTX, "00.0");
        GD.cmd_text(580, 127, BEBAS_HANDLE, OPT_CENTER | OPT_RIGHTX, "00.0");
        GD.cmd_text(194, 370, BEBAS_HANDLE, OPT_CENTER | OPT_RIGHTX, "00.0");
        GD.swap();
      }
      break;
  }
}

void display_data(int id, int loc) {

  if (loc == 0) {
    GD.cmd_text(50, 140, BEBAS_HANDLE, OPT_CENTERY, sensordata[id]); //upper left
  }
  if (loc == 1) {
    GD.cmd_text(450, 140, BEBAS_HANDLE, OPT_CENTERY, sensordata[id]); // upper right
  }
  if (loc == 2) {
    GD.cmd_text(50, 380, BEBAS_HANDLE, OPT_CENTERY, sensordata[id]); //lower left
  }
  if (loc == 3) {
    GD.cmd_text(450, 380, BEBAS_HANDLE, OPT_CENTERY, sensordata[id]); //lower right
  }
  if (loc == 4) {
    GD.cmd_text(GD.w / 2, GD.h / 2, BEBAS_HANDLE, OPT_CENTERY, sensordata[id]); //center
  }
}


//c type string manipulation with fixed construct type
void sep_by_comma(char main_string[], char* array_of_pointers[7]) {
  const char seperator[] = ",";
  char* to_array = array_of_pointers[0];
  char* token = strtok(main_string, seperator);
  int i = 0;
  while (token != NULL) {
    array_of_pointers[i] = token;
    token = strtok(NULL, seperator);
    i += 1;
  }
}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    char* clientId = "ESP32";
    // Attempt to connect
    if (client.connect(clientId)) {
      Serial.println("connected");
      client.subscribe("display/01/config");
      client.subscribe("wind/twa");
      client.subscribe("wind/tws");
      client.subscribe("wind/awa");
      client.subscribe("wind/aws");
      client.subscribe("boat/speed");
      client.subscribe("boat/heel");
      client.subscribe("boat/depth");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  GD.begin();
  LOAD_ASSETS();
  Serial.begin(115200);

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
