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

int main(int argc, char **argv){
  int total_tests = 1;
  int passed_tests = 0;

  // tests
  //passed_tests += test_setYaw();
  passed_tests += test_setRoll(30);

  //report
  std::cout << "Tests sucessful " << passed_tests << "/" << total_tests << std::endl;
  if (passed_tests >= total_tests) {
    std::cout << "All Tests Passed" << std::endl;
  }
  else {
    std::cout << "Some Tests Failed" << std::endl;
  }
}
