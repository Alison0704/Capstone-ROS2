#define MOTOR_A_IN1 18
#define MOTOR_A_IN2 19
#define MOTOR_B_IN3 21
#define MOTOR_B_IN4 22

unsigned long last_cmd_time = 0;
const unsigned long TIMEOUT_MS = 1000; // Stop if no serial for 1 second

void setup() {
  // Use high baud rate to match serial_bridge.py
  Serial.begin(115200); 
  
  pinMode(MOTOR_A_IN1, OUTPUT);
  pinMode(MOTOR_A_IN2, OUTPUT);
  pinMode(MOTOR_B_IN3, OUTPUT);
  pinMode(MOTOR_B_IN4, OUTPUT);
  
  stopMotors();
  last_cmd_time = millis();
}

void loop() {
  // Check for incoming commands from Raspberry Pi
  if (Serial.available() > 0) {
    char state = Serial.read();
    last_cmd_time = millis(); // Reset safety timer
    
    executeState(state);
  }

  // Safety Watchdog: Stop motors if Pi stops talking
  if (millis() - last_cmd_time > TIMEOUT_MS) {
    stopMotors();
  }
}

void executeState(char command) {
  switch(command) {
    case 'S': // IDLE_WAIT: Rotate in place to Scan
      rotateInPlace();
      break;
      
    case 'F': // APPROACH / MOVE: Move Forward
      moveForward();
      break;
      
    case 'B': // OBSTACLE: Emergency Backup
      moveBackward(); //update on how you want to handle obstacle
      break;
      
    case 'H': // ARRIVED / HALT: Stop all motion
    default:
      stopMotors();
      break;
  }
}


void rotateInPlace() {
  // Motors turn in opposite directions to spin the robot
  digitalWrite(MOTOR_A_IN1, HIGH);
  digitalWrite(MOTOR_A_IN2, LOW);
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, HIGH);
}

void moveForward() {
  // Both motors move forward
  digitalWrite(MOTOR_A_IN1, HIGH);
  digitalWrite(MOTOR_A_IN2, LOW);
  digitalWrite(MOTOR_B_IN3, HIGH);
  digitalWrite(MOTOR_B_IN4, LOW);
}

void moveBackward() {
  // Both motors reverse
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, HIGH);
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, HIGH);
}

void stopMotors() {
  // Cut power to all motor inputs
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, LOW);
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, LOW);
}