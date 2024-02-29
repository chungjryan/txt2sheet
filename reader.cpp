// working on writing a reader in cpp
#include <fstream>
#include <string>
#include <iostream>

class Reader {
public:
  Reader(const std::string& filename){
    file.open(filename);
  }

  void read(){
    std::string line;
    while (std::getline(file, line)){
      std::cout << line << std::endl;
    }
  }

private:
  std::ifstream file;
};