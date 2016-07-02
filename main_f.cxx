#include <iostream>
#include <fstream>
#include <unistd.h>
#include <fcntl.h>

using namespace std;

int toBin (int a) {
	int b=0, k=1;
	while (a)
    {
        b+=a%2*k;
        a/=2;
        k*=10;
    }
    return b;
}

int toDec (int N) {
	int sum=0; 
	int pow2 = 1;
	int a=0;
	for (int i=7; i>-1; i--) {
		a = N%10;
		if (a==1) {
			sum+=pow2;
		} 
		pow2*=2;
		N = N/10;
	}
	return sum;
}

void pulsout (int id, int pin, int N) {
	bool flag = true;
	while (flag) {
		char oneBit = static_cast<char>(toDec(toBin(id)*10000));
		char twoBit = static_cast<char>(toDec((10000+toBin(pin))*100+toBin(N)/100000000));
		char thirdBit = static_cast<char>(toDec(toBin(N)%100000000));
      //  cout << "Starting fout\n";
		ofstream fout ("/dev/ttyUSB0");
       // cout << oneBit << twoBit << thirdBit;
		fout << oneBit << twoBit << thirdBit;
		fout.close();
     //   cout << "Finished\n";
//		ofstream resout ("/home/grandalw/boe-bot/result/res.txt", ios_base::app);
//		resout <<toBin(id)*10000 + toBin(idFrm)<<' '<<(10000+toBin(pin))*100+toBin(N)/100000000 <<' '<<toBin(N)%100000000<<'\n';
//		usleep(100000);

		char buf[1];
		usleep(20000);
		ifstream fin ("/dev/ttyUSB0", ios_base::binary);
		fin.readsome(&buf[0], 1);
		fin.close();

		if (buf[0] == oneBit) {
			cout <<"Yes"<< buf << '\n';
			flag = false;
		} else {
			cout <<"No"<< buf << '\n';
			flag = true;
//			usleep(10000);
		}
//		resout.close();
	}
	return;
}

int main(int argc,char **argv)
{
    
    // ./a.out [l, r, f]
    char cmd = argv[1][0];
    int i = 0;
    
    switch (cmd) {
    case 'l':
        cout << "Turn left\n";
        for(; i<3; i++) {
            pulsout (4, 12, 750);
            pulsout (4, 13, 500);
            usleep (1000);
        }
        break;
    case 'r':
        cout << "Turn right\n";
        for(; i<3; i++) {
            pulsout (4, 12, 1000);
            pulsout (4, 13, 750);
            usleep (1000);
        }
        break;
    case 'f':
        cout << "Go forward\n";
        for(; i<5; i++) {
            pulsout (4, 12, 1000);
            pulsout (4, 13, 500);
            usleep (1000);
        }
        break;
    default:
        cout << "Unexpected input\n";
        break;
    }
    
    /*
	for(int i=0; i<5; i++) {
		cout << i << '\t';
		pulsout (4, 12, 850);
		pulsout (4, 13, 650);
		usleep (10000);		
	} */
	return 0;
}
