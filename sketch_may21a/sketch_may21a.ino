#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <SimpleKalmanFilter.h>

Adafruit_BMP280 bmp; 

SimpleKalmanFilter bo_loc_kalman(0.2, 0.2, 0.005);

unsigned long lastTime = 0;
const int sampleInterval = 50;


void setup() {
  Serial.begin(115200);
  while (!Serial) delay(100);

  if (!bmp.begin(0x76)) {
    Serial.println("Loi: Khong tim thay GY-BMP280! Vui long kiem tra lai day I2C.");
    while (1);
  }

  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                  Adafruit_BMP280::SAMPLING_X2,
                  Adafruit_BMP280::SAMPLING_X16,
                  Adafruit_BMP280::FILTER_X16,
                  Adafruit_BMP280::STANDBY_MS_1);

}

void loop() {
  unsigned long currentTime = millis();

  // Đảm bảo thuật toán chạy đúng chu kỳ 50ms (20Hz)
  if (currentTime - lastTime >= sampleInterval) {
    lastTime = currentTime;

    // Bước 1: Đọc độ cao
    float z_raw = bmp.readAltitude(1001.0);
    //Nhiệt độ
    float temp = bmp.readTemperature();
    // Bước 2: Xử lý qua thuật toán Kalman
    float x_est = bo_loc_kalman.updateEstimate(z_raw);

    // Bước 3: Xuất kết quả
    Serial.print(z_raw);
    Serial.print(",");
    Serial.print(x_est);
    Serial.print(",");
    Serial.println(temp);
  }
}