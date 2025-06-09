 # control_motors_1.py
import RPI.GPIO as GPIO
from time import sleep

class MotorController:
    def __init__(self,forward_pin: int, backward_pin: int, enable_pin: int):
        # Инмциализация пинов
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self.enable_pin = enable_pin 

        # Настройка GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarning(false)
        GPIO.setup(self.forward_pin, GPIO.OUT)
        GPIO.setup(self.backward_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)

        # Инициализация PWM для управления скоростью
        self.pwm = GPIO.PWM(self.enable_pin, 1000)  # частота 1 кГц
        self.pwm.start(0)  # начальная скорость 0%

    def set_speed(self, speed: int):
       """Установка скорости двигателя (0-100%)"""
        self.pwm.ChangeDutyCycle(speed)

    def smooth_speed(self, target_speed: int, step: int = 5, delay: float = 0.1):
        """Плавное измененме скорости"""    
        current_speed = 0
        while current_speed != target_speed:
             if target_speed > current_speed:
                current_speed = min(current_speed + step, target_speed)
             else:
                current_speed = max(current_speed - step, target_speed)
             self.set_speed(current_speed)
             sleep(delay)

     def move_forward(self):
        """Движение вперёд"""
         GPIO.output(self.forward_pin, GPIO.HIGH)
         GPIO.output(self.backward_pin, GPIO.LOW)

     def move_backward(self):
        """Движение назад"""
         GPIO.output(self.forward_pin, GPIO.LOW)
         GPIO.output(self.backward_pin, GPIO.HIGH)

     def move_backward(self):
        """Остановка двигателя """
         GPIO.output(self.forward_pin, GPIO.LOW)
         GPIO.output(self.backward_pin, GPIO.LOW)
         self.set_speed(0)
       
      def cleanup(self):
         """Освобождение ресурсов"""
          self.pwm.stop()
          GPIO.clean()

# Пример Использования
 if __name__ == "__main__":
     try:
         # конфигурация пинов (ВСМ нумерация)
         motor = M0torController(
              forward_pin=16,    # GPIO 23
              backward_pin=18,   # GPIO 24
              enable_pin=22,     # GPIO 25
            )

         print("плавный старт двигателя")
         motor.move_forward()
         motor.smooth_speed(80,step=5)   # Плавный разгон до 80%
         sleep(2)

         print("плавная остановка")         
         motor.smooth_speed(0,step=5)   # Плавное торможение  
         sleep(1)

         print("Реверс с плавным ускорением...")
         motor.move_backward()
         motor.smooth_speed(60,step=3)   # Медленный разгон
         sleep(1.5)

      except KeyboardInterrupt:
         print("\Прервано пользователем")
      finally:
         motor.stop()
         motor.cleanup()
         print("Ресурсы освобождены")

   
