#include <stdio.h>
void main ()
{
   int x =1;
   char a[4]="";
   char b[4]="123";
   int B=sizeof(int);
   int C=strlen(a);
   memcpy(a,b,C/1);
}