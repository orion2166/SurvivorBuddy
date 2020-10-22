#include <iostream>
#include "motorMovement_Tester.cpp"

using namespace std;

int test_setYaw(){
  setYaw(359);
  std::cout << "setYaw unsure how to test" << endl;
  return 0;
}

int test_setRoll(int x){
  //test
  int expected = map(x, 0, 90, 115, 7);
  setRoll(x);
  int actual = setRoll_tester();

  //assert
  if (actual == expected) {
    std::cout << "setRoll Passed" << endl;
    return 1;
  }
  else {
    std::cout << "setRoll Failed - Expected: " << expected << " Actual: " << actual <<  endl;
    return 0;
  }
}

int test_setPitch(int x){
  //test
  int expected1 = map(x, 0, 90, 150, 65);
  int expected2 = map(x, 0, 90, 55, 138);
  setPitch(x);
  int actual1 = setPitchLeft_tester();
  int actual2 = setPitchRight_tester();

  //assert
  if ((actual1 == expected1) and (actual2 == expected2)) {
    std::cout << "setPitch Passed" << endl;
    return 1;
  }
  else {
    std::cout << "setPitch Failed - Expected: " << expected1 << " Actual: " << actual1 <<  endl;
    return 0;
  }
}

int main(int argc, char **argv){
  int total_tests = 2;
  int passed_tests = 0;

  // tests
  //passed_tests += test_setYaw();
  passed_tests += test_setRoll(30);
  passed_tests += test_setPitch(30);

  //report
  std::cout << "Tests sucessful " << passed_tests << "/" << total_tests << std::endl;
  if (passed_tests >= total_tests) {
    std::cout << "All Tests Passed" << std::endl;
  }
  else {
    std::cout << "Some Tests Failed" << std::endl;
  }
}
