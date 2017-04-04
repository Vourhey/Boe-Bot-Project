#include <windows.h>
#include <iostream>
#include <time.h>
#include <conio.h>
using namespace std;
HANDLE hSerial;
HANDLE hSerial1;

void ReadCOM()
{
	DWORD iSize;
	char sReceivedChar;
	while (true)
	{
		ReadFile(hSerial, &sReceivedChar, 1, &iSize, 0);
		if (iSize > 0)
			cout << sReceivedChar;
	}
}

void KakoitoRobot(LPCTSTR sPortName, char data1[], char data2[])
{
	DWORD dwSize = sizeof(data1);
	DWORD dwBytesWritten;
	
	while (1)
	{
		hSerial = ::CreateFile(sPortName, GENERIC_READ | GENERIC_WRITE, 0, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
		if (hSerial != INVALID_HANDLE_VALUE)
		{
			if (GetLastError() == ERROR_FILE_NOT_FOUND)
			{
				cout << "serial port does not exist.\n";
			}
			cout << "some other error occurred.\n";
			break;
		}



		DCB dcbSerialParams = { 0 };
		dcbSerialParams.DCBlength = sizeof(dcbSerialParams);

		dcbSerialParams.BaudRate = CBR_9600;
		dcbSerialParams.ByteSize = 8;
		dcbSerialParams.StopBits = ONESTOPBIT;
		dcbSerialParams.Parity = NOPARITY;
		if (SetCommState(hSerial, &dcbSerialParams))
		{
			cout << "error setting serial port state\n";
			break;
		}
	}
	int i;
	for (i = 0; i<strlen(data1); i++)
	{
		//data1[0] = _getch();
		data2[0] = data1[i];
		//data4[0] = data3[i];
		//char a = _getch();
		Sleep(500);
		cout << data1[i] << "\n";
		WriteFile(hSerial, data2, dwSize, &dwBytesWritten, NULL);
		//WriteFile(hSerial1, data2, dwSize, &dwBytesWritten1, NULL);
	}
	cout << dwSize << " Bytes in string. " << dwBytesWritten << " Bytes sended. " << endl;
	//Sleep(3);
	char a = _getch();

	ReadCOM();

	WriteFile(hSerial, data2, dwSize, &dwBytesWritten, NULL);
	ReadCOM();

}

int main(int argc, char** argv[])
{
	LPCTSTR sPortName = L"COM8";

	char data1[] = "wddw";
	char data2[] = "";
	char data3[] = "adswwddw";
	char data4[] = "";

	KakoitoRobot(sPortName, data1, data2);
	
	
	//BOOL iRet =
	
	
	LPCTSTR sPortName1 = L"\\\\.\\COM14";
	//DCB dcbSerialParams1;
		
    KakoitoRobot(sPortName1, data3, data4);

		return 0;
}


