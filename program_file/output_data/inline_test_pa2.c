int f(m,n){
    ;
}
int main ()
{
    int (*ff)(int); 
    int a=1;
    int b=2;
    ff=f;
    ff(a,b);
    return 0;
}