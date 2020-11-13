#include <iostream>
#include <vector>
#include "motorMovement_Tester.cpp"

using namespace std;

int test_getPositionPM(int input1){
  //test
  phoneMountServo.write(input1,0);
  int actual = phoneMountServo.read();
  int return_val = 0;

  //assert
  if (actual == input1) {
    std::cout << "PASSED";
    return_val = 1;
  }
  else {
    std::cout << "FAILED";
  }
  std::cout << " - getPositionPM - Expected: " << input1 << " Actual: " << actual <<  endl;

  return return_val;
}

int test_getPositionBM(int input1){
  //test
  leftBaseServo.write(input1,0);
  int actual = leftBaseServo.read();
  int return_val = 0;

  //assert
  if (actual == input1) {
    std::cout << "PASSED";
    return_val = 1;
  }
  else {
    std::cout << "FAILED";
  }
  std::cout << " - getPositionBM - Expected: " << input1 << " Actual: " << actual <<  endl;

  return return_val;
}

int test_sendPosition(int input1, std::vector<int> vect){
  //test
  std::vector<int> actual = sendPosition(input1);
  int return_val = 0;

  //assert
  if (actual == vect) {
    std::cout << "PASSED";
    return_val = 1;
  }
  else {
    std::cout << "FAILED";
  }
  std::cout << " - sendPosition - Expected: [" << vect.at(0) << ", " << vect.at(1) << ", " << vect.at(2) << "] Actual: [" << actual.at(0) <<", "<< actual.at(1) <<", "<< actual.at(2) <<"]"<<  endl;

  return return_val;
}

int test_getPositionTabletop(int input1,int expected){
  //test
  int actual = getPositionTabletop(input1);
  int return_val = 0;

  //assert
  if (actual == expected) {
    std::cout << "PASSED";
    return_val = 1;
  }
  else {
    std::cout << "FAILED";
  }
  std::cout << " - getPositionTabletop - Expected: " << expected << " Actual: " << actual <<  endl;

  return return_val;
}

int test_setYaw(int input1,int input2,int expected){
  //test
  int actual = setYaw(input1,input2);
  int return_val = 0;
  std::string motions[3] = {"Stay","Counter-Clockwise","Clockwise"};

  //assert
  if (actual == expected) {
    std::cout << "PASSED";
    return_val = 1;
  }
  else {
    std::cout << "FAILED";
  }
  std::cout << " - setYaw - Expected: " << motions[expected] << " Actual: " << motions[actual] <<  endl;

  return return_val;
}

int test_setRoll(int input,int expected){
  //test
  setRoll(input);
  int actual = setRoll_tester();
  int return_val = 0;

  //assert
  if (actual == expected) {
    std::cout << "PASSED";
    return_val = 1;
  }
  else {
    std::cout << "FAILED";
  }
  std::cout << " - setRoll - Expected: " << expected << " Actual: " << actual <<  endl;

  return return_val;
}

int test_setPitch(int input,int expected){
  //test
  setPitch(input);
  int actual = setPitchLeft_tester();
  int return_val = 0;

  //assert
  if (actual == expected) {
    std::cout << "PASSED";
    return_val = 1;
  }
  else {
    std::cout << "FAILED";
  }
  std::cout << " - setPitch - Expected: " << expected << " Actual: " << actual <<  endl;

  return return_val;
}

int main(int argc, char **argv){
  int total_tests = 15;
  int passed_tests = 0;
  std::vector<int> vect;
  vect.push_back(41);
  vect.push_back(35);
  vect.push_back(47);

  // tests
  //IDEFO [4.2.2]
  //test_getPositionPM(inputAndExpected);
  passed_tests += test_getPositionPM(99);
  //IDEFO [4.2.6]
  //test_getPositionBM(inputAndExpected);
  passed_tests += test_getPositionBM(78);
  //IDEFO [4.3]
  //test_sendPosition(currentposition,expectedDataSent);
  passed_tests += test_sendPosition(30,vect);
  //IDEFO [4.2.4]
  //test_getPositionTabletop(input,expected);
  passed_tests += test_getPositionTabletop(245,180); //left edge
  passed_tests += test_getPositionTabletop(65,0); //right edge
  passed_tests += test_getPositionTabletop(150,0); //right over extended
  //IDEFO [4.2.3]
  //test_setPitch(newPosition,currentPosition,expectedOutcome)
  passed_tests += test_setYaw(78,78,0); //same = stay
  passed_tests += test_setYaw(90,15,1); //counter clockwise
  passed_tests += test_setYaw(45,98,2); //clockwise
  //IDEFO [4.2.1]
  //test_setRoll(input,expected)
  passed_tests += test_setRoll(0,78); //edge case
  passed_tests += test_setRoll(90,118); //edge case
  passed_tests += test_setRoll(45,98); //normal case
  //IDEFO [4.2.5]
  //test_setPitch(input,expected)
  passed_tests += test_setPitch(0,110); //edge case
  passed_tests += test_setPitch(90,40); //edge case
  passed_tests += test_setPitch(45,75); //normal case

  //report
  std::cout << "\n\nSucessful Tests: " << passed_tests << "/" << total_tests << std::endl;
  if (passed_tests >= total_tests) {
    std::cout << "All Tests Passed" << std::endl;
  }
  else {
    std::cout << "Some Tests Failed" << std::endl;
  }
}
