//RunAway.c
int gPrevRet = 0; //���溯���ķ��ص�ַ
void Detour(void){
    int *p = (int*)&p + 2;  //pָ�����ķ��ص�ַ
    *p = gPrevRet;
    printf("Run Away!\n"); //��Ҫ�س������ӡ��fflush(stdout);ˢ�»���������������ڶδ���ʱ�޷����
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
