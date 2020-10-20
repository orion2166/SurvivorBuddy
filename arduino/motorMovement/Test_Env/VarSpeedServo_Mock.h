
class VarSpeedServo_Mock {
  public:
    int pin_num = 0;
    void wait();
    int read();
    void write(int, int) {
      /* code */
    };
    void write(int);
    void write(int, int, bool);
    void attach(int);
    void writeMicroseconds(int);
};

//funcs write, wait, read, attach(int)
