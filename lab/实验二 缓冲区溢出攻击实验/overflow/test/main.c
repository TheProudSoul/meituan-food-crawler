#include <stdio.h>
#include<string.h>

void overflow(const char* input)
{
       char buf[8];
       printf("Virtual address of 'buf' = Ox%p\n", buf);
       strcpy(buf,input);
}

void fun()
{
    printf("Function 'fun' has been called without an explicitly invocation.\n");
    printf("Buffer Overflow attack succeeded!\n");
    // your other codes, e.g. deleting files
    // what happens when return?
}

int _main(int argc, char* argv[])
{
        printf("Virtual address of 'overflow' = Ox%p\n",overflow);
        printf("Virtual address of 'fun' = Ox%p\n",fun);
        //char input[]="AAAAAAAA";//good input, ASCII code of 'A' is 41
        char input[]="AAAAAAAAAAAAAAAAAAAA\x77\x14\x40\x00";//bad input
        overflow(input);
        return 0;
}
