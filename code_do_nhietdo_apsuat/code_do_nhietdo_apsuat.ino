#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

// -------------------------------------------------------
// Kalman filter tự viết
// -------------------------------------------------------
float kf_q = 0.1;   // process noise — càng nhỏ filter càng mượt nhưng lag hơn
float kf_r = 0.5;   // measurement noise — càng lớn tin filter hơn tin cảm biến
float kf_x = 0.0;   // ước lượng hiện tại
float kf_p = 1.0;   // error covariance

float kalman_update(float z) {
  kf_p = kf_p + kf_q;                    // Predict
  float k = kf_p / (kf_p + kf_r);        // Kalman gain
  kf_x = kf_x + k * (z - kf_x);         // Estimate
  kf_p = (1.0 - k) * kf_p;              // Update covariance
  return kf_x;
}
// -------------------------------------------------------

unsigned long lastTime   = 0;
const int sampleInterval = 500;
const int WARMUP_SAMPLES = 30;

// ICAO: h = 44330 * (1 - (P/1013.25)^0.1903)
float calcAltitude(float p_hpa) {
  return 44330.0 * (1.0 - pow(p_hpa / 1013.25, 0.1903));
}

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  if (!bmp.begin(0x76)) {
    if (!bmp.begin(0x77)) {
      Serial.println("Khong tim thay BMP280!");
      while (1) delay(1000);
    }
  }

  delay(500);

  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                  Adafruit_BMP280::SAMPLING_X2,
                  Adafruit_BMP280::SAMPLING_X16,
                  Adafruit_BMP280::FILTER_X16,
                  Adafruit_BMP280::STANDBY_MS_500);

  delay(500);

  // Tính altitude mean
  Serial.println("Dang khoi dong...");
  double altSum = 0;
  for (int i = 0; i < WARMUP_SAMPLES; i++) {
    delay(100);
    altSum += calcAltitude(bmp.readPressure() / 100.0);
  }
  float altMean = altSum / WARMUP_SAMPLES;

  // Seed Kalman = hard-set về đúng giá trị thực
  kf_x = altMean;
  kf_p = 1.0;
  // Hội tụ 200 vòng
  for (int i = 0; i < 200; i++) {
    kalman_update(altMean);
  }

  Serial.println("================================");
  Serial.print  ("Do cao khoi diem: "); Serial.print(kf_x, 2); Serial.println(" m");
  Serial.println("================================");
  Serial.println("Nhiet do (C) | Do cao (m) | Ap suat (hPa)");
  Serial.println("--------------------------------------------");
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastTime >= sampleInterval) {
    lastTime = currentTime;

    float temp     = bmp.readTemperature();
    float pressure = bmp.readPressure() / 100.0;
    float z_raw    = calcAltitude(pressure);
    float z_kal    = kalman_update(z_raw);

    if (temp < -40 || temp > 85) return;

    Serial.print(temp,    2); Serial.print(" C        | ");
    Serial.print(z_kal,   2); Serial.print(" m        | ");
    Serial.print(pressure, 2); Serial.println(" hPa");
  }
}