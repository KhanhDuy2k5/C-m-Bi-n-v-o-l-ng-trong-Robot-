#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

// Kalman filter tự viết

float kf_q = 0.1;
float kf_r = 0.5;
float kf_x = 0.0;
float kf_p = 1.0;

float kalman_update(float z) {
  kf_p = kf_p + kf_q;
  float k = kf_p / (kf_p + kf_r);
  kf_x = kf_x + k * (z - kf_x);
  kf_p = (1.0 - k) * kf_p;
  return kf_x;
}

const int N_SAMPLES = 20;       // lay 20 mau theo yeu cau bai
const float P0      = 1013.25;  // ICAO

float calcAltitude(float p_hpa) {
  return 44330.0 * (1.0 - pow(p_hpa / P0, 0.1903));
}

// Nhập h_ref qua Serial Monitor
float h_ref = 0.0;

void doMeasurement() {
  float p_buf[N_SAMPLES];
  float p_sum  = 0;
  float p_sum2 = 0;

  Serial.println(">> Dang lay 20 mau...");

  for (int i = 0; i < N_SAMPLES; i++) {
    delay(500);
    p_buf[i] = bmp.readPressure() / 100.0;  // hPa
    p_sum   += p_buf[i];

    // Reset Kalman sau mỗi vị trí đo mới
    float alt = calcAltitude(p_buf[i]);
    kalman_update(alt);
  }

  // Tính P trung bình
  float p_mean = p_sum / N_SAMPLES;

  // Tính sigma_P (độ lệch chuẩn áp suất)
  for (int i = 0; i < N_SAMPLES; i++) {
    float diff = p_buf[i] - p_mean;
    p_sum2 += diff * diff;
  }
  float sigma_p = sqrt(p_sum2 / N_SAMPLES);

  // Tính h_meas từ P trung bình
  float h_meas = calcAltitude(p_mean);

  // Nhiệt độ
  float temp = bmp.readTemperature();

  // Sai số tuyệt đối và tương đối
  float e_h_m   = h_meas - h_ref;              // m
  float e_h_pct = (h_ref != 0)
                  ? (abs(e_h_m) / abs(h_ref)) * 100.0
                  : 0.0;                        // %

  Serial.println("--------------------------------------------");
  Serial.print  ("h_ref    : "); Serial.print(h_ref,    2); Serial.println(" m");
  Serial.print  ("P trung binh: "); Serial.print(p_mean,  2); Serial.println(" hPa");
  Serial.print  ("sigma_P  : "); Serial.print(sigma_p,  4); Serial.println(" hPa");
  Serial.print  ("T        : "); Serial.print(temp,     2); Serial.println(" C");
  Serial.print  ("h_meas   : "); Serial.print(h_meas,   2); Serial.println(" m");
  Serial.print  ("e_h      : "); Serial.print(e_h_m,    3); Serial.println(" m");
  Serial.print  ("e_h (%%) : "); Serial.print(e_h_pct,  2); Serial.println(" %");
  Serial.println("--------------------------------------------");
  Serial.println(">> Nhap h_ref tang tiep theo (m) roi nhan Enter:");
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

  // Warm-up + seed Kalman tại tầng 1 (GND)
  Serial.println("================================");
  Serial.println("    DO CAO DA TANG - BMP280     ");
  Serial.println("================================");
  Serial.println("Warm-up cam bien...");

  double altSum = 0;
  for (int i = 0; i < 30; i++) {
    delay(100);
    altSum += calcAltitude(bmp.readPressure() / 100.0);
  }
  float altMean = altSum / 30;
  kf_x = altMean;
  for (int i = 0; i < 200; i++) kalman_update(altMean);

  Serial.println(">> Nhap h_ref Tang 1/GND (m) roi nhan Enter:");
}

void loop() {
  // Chờ người dùng nhập h_ref qua Serial Monitor
  if (Serial.available() > 0) {
    h_ref = Serial.parseFloat();
    while (Serial.available()) Serial.read();  // flush buffer

    // Reset Kalman cho vị trí đo mới
    float p_now = bmp.readPressure() / 100.0;
    kf_x = calcAltitude(p_now);
    kf_p = 1.0;

    doMeasurement();
  }
}