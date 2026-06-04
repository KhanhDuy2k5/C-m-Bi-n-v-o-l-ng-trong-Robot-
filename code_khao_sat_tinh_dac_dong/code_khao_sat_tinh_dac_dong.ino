#include <Wire.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

const float alpha = 0.3; 
const unsigned long SAMPLE_INTERVAL_US = 20000; 

float raw_altitude = 0;
float ema_altitude = 0;
bool first_run = true;

unsigned long startTimeUs;
unsigned long previousMicros = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10); 

  if (!bmp.begin(0x76)) {  
    Serial.println(F("Loi: Khong tim thay BMP280!"));
    while (1) delay(10);
  }

  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                  Adafruit_BMP280::SAMPLING_X2,     
                  Adafruit_BMP280::SAMPLING_X16,    
                  Adafruit_BMP280::FILTER_OFF,      
                  Adafruit_BMP280::STANDBY_MS_1);   

  Serial.println("Time_ms,Raw_Altitude,EMA_Altitude");

  startTimeUs = micros();
  previousMicros = startTimeUs;
}

void loop() {
  unsigned long currentMicros = micros();

  if (currentMicros - previousMicros >= SAMPLE_INTERVAL_US) {
    previousMicros += SAMPLE_INTERVAL_US; 

    // 1. Đọc dữ liệu
    raw_altitude = bmp.readAltitude(1002.00);

    // 2. Lọc EMA
    if (first_run) {
      ema_altitude = raw_altitude;
      first_run = false;
    } else {
      ema_altitude = (alpha * raw_altitude) + ((1.0 - alpha) * ema_altitude);
    }

    // 3. Tính toán thời gian thực (ms) với độ phân giải cao 
    float time_ms = (currentMicros - startTimeUs) / 1000.0;

    // 4. In dữ liệu ra Serial
    Serial.print(time_ms, 2); // In thời gian với 2 chữ số thập phân (VD: 20.00, 40.00)
    Serial.print(",");
    Serial.print(raw_altitude, 3); // Tăng độ phân giải hiển thị độ cao lên 3 chữ số
    Serial.print(",");
    Serial.println(ema_altitude, 3);
  }

}
