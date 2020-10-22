#include <iostream>
class VarSpeedServo_Mock {
  public:
    int pin_num = 0;
    void wait(){
      //code
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
    void write(int, int, bool){
      //code
    }
    void attach(int){
      //code
    }
    void writeMicroseconds(int){
      //code
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
