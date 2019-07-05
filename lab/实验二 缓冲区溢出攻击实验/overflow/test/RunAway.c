//RunAway.c
int gPrevRet = 0; //保存函数的返回地址
void Detour(void){
    int *p = (int*)&p + 2;  //p指向函数的返回地址
    *p = gPrevRet;
    printf("Run Away!\n"); //需要回车，或打印后fflush(stdout);刷新缓冲区，否则可能在段错误时无法输出
}
int RunAway(void){
    int *p = (int*)&p + 2;
    gPrevRet = *p;
    *p = (int)Detour;
    return 0;
}
int main(void){
    RunAway();
    printf("Come Home!\n");
    return 0;
}
