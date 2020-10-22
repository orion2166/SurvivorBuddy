#include <iostream>
class VarSpeedServo_Mock {
  public:
    int write_3_input = 0;
    int pin_num = 0;
    void wait(){
      std::cout << "waiting" << std::endl;
    }
    int read(){
      return 10;
    }
    void write(int, int) {
      /* code */
    };
    void write(int){
      //code
    }
    void write(int x, int y, bool z){
      write_3_input = x;
    }
    void attach(int){
      //code
    }
    void writeMicroseconds(int x){
      std::cout << "writeMicroseconds " << x << std::endl;
    }
};

class Serial {
  public:
    void write(char*, int){
      //code
    }
    void begin(int){
      //code
    }
    bool available(){
      return true;
    }
    void setTimeout(int){
      //code
    }
    void readBytes(unsigned char*, int){
      //code
    }
};

//funcs write, wait, read, attach(int)
