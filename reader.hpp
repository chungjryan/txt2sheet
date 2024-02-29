// working on writing a reader in cpp
#include <fstream>
#include <string>

class Reader {
public:
    Reader(const std::string& filename);
    void read();
    
private:
    std::ifstream file;
};