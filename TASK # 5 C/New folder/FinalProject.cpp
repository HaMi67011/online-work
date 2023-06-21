#include <iostream>                     // for input output
#include <fstream>			            // for file opening and closing
#include <iomanip>			            //for setw function
#include <stdio.h>			            // for flush all that is to clear the buffer memmory
#include <conio.h>			            //for getch function
#include <stdlib.h>			            //for use system function for clearing the screen
#include<string>

using namespace std;
//#######################################################################################
class phonebook		                    // Phonebook class
{
    private:
        string code;
        string fname;
        string lname;
        string phone_no;
    public:
        void get_person(void);
        void put_person(void);
        string get_fname(){
            return this->fname;
        }

        string get_lname(){
            return this->lname;
        }
        
        string get_code(void)
        {
            return this->code;
        }
        
        string get_phone(){
            return this->phone_no;
        }
};
//#################################################################
void phonebook :: get_person(void)		          // function for collecting data from user
{
    cout << "Enter Unique Code: ";
    cin >> this->code;
    cout << "Enter First Name: ";
    cin >> this->fname;
    cout << "Enter Last Name: ";
    cin >> this->lname;
    cout << "Enter Phone Number: ";
    cin >>this->phone_no;
}
//#################################################################
void phonebook :: put_person(void)				// funtion for Display data
{
    cout <<code <<"               "<<fname<<" "<<lname <<"                       "<<phone_no << endl;
}
//#################################################################
//1st function  
phonebook va;                                   // class Variable
fstream file;
ofstream w;
//#################################################################
void add_record(phonebook x)			        // function for saving contact record
{
	ofstream f;
    char ch = 'y';
    f.open("record.txt", fstream::app);
    while(ch =='y' || ch == 'Y')				// loop is used for store 2 or more record
    {
        x.get_person(); 
		string code = x.get_code();
		string phone = x.get_phone();
		string fname = x.get_fname();
		string lname = x.get_lname();
        f<<code<<"              "<<fname<<" "<<lname<<"           "<<phone<<endl;  
        cout << "Add more Contact....(y 'or' n)?";
		cin >>ch;
    }
    f.close();
}
//#################################################################
void show_All(void)				                // for Display all contact list
{	
	char content;
    fstream file;
	file.open("record.txt", fstream::in);
    if(!file)
    {
        cout << "File not found: ";
        exit(0);
    }
    else
    {	
    	while(!file.eof())
		{
		    file.get(content);
		    cout<<content;
		}
    }
    file.close();
}
//##################################################################
void search_record(void)
{
	string code, line;
	int found = 0;
	cout << "Enter Person's Unique code to Search Contact: ";
	cin>>code;
	ifstream fin;
    fin.open("record.txt");
    if(!fin)
    {
        cout << "File not Found";
        exit(0);
    }
    while (getline(fin, line))
	{
		std::string id(line.begin(), line.begin() + line.find(" "));
		if(id == code)
		{
			found = 1;
			cout<<line<<endl;	
		}
	}
	if(found == 0)
	{
		cout<<"No Record Found!"<<endl;
	}
	fin.close();
	
}
//#################################################################
void delete_record(void)			                //For delete any contact
{
    string deleteline;
    string line;

    ifstream fin;
    fin.open("record.txt");
    if(!fin)
    {
        cout << "File not Found";
        exit(0);
    }
    else
	{
	    ofstream temp;
	    temp.open("temp.txt");
	    cout << "Enter Person's Unique code to Delete Contact: ";
	    cin >> deleteline;
	
	    while (getline(fin, line))
	    {
	        std::string id(line.begin(), line.begin() + line.find(" "));
			if (id != deleteline)
			    temp << line << endl;
	    }
	
	    temp.close();
	    fin.close();
	    remove("record.txt");
	    rename("temp.txt", "record.txt");
	}
}
//#################################################################

//#################################################################
int main()			                                    //Main Function
{
	phonebook object;
    int option;
    while(1)
    {
        system("cls");
cout <<"\n\t################ (   Welcome to Contact Management System   ) ################# " << endl;
cout << endl;
cout << "\n\n\tPhone Book\n\t\t*\n\t\t[1] Add a new Contact\n\t\t[2] show All contact\n\t\t[3] Search contact\n\t\t[4] delete_record\n\t\t[5]Exit\n\t\t" << endl;

        cout << endl;
        cout << "Enter: "<<endl;
        cout << endl;
cin >> option;

    switch(option)
    {
        case 1:
        {
            add_record(object);
            cout << "Press any key for Main Menu .. ";
            getch();
            break;
        }
        case 2:
        {
            cout << setw(1) << "Code |"<<setw(18)<< "Name |"<<setw(28)<<"phone_no|" << endl;
            cout <<"-------------------------------------------------------------------------"<< endl;
            show_All();
            cout << "-------------------------------------------------------------------------"<< endl;

            cout << "Press any key for Main Menu...";
            getch();
            break;
        }
        case 3:
        {
            search_record();                               //line 109
            cout << "press any key for Main Menu...";
            getch();
            break;
        }
        case 4:
            {
                delete_record();
                cout << "press any key for Main Menu...";
                getch();
                break;
            }

        case 5:
            {
                cout << "Thank you so much: ";
                cout << endl;
                exit(0);
            }
        default:
            {
                cout << "Incorrect Option: ";
                getch();
                break;
            }
    }
    }
    return 0;

}

//##################################################################
