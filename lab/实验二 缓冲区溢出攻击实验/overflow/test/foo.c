//foo.c
void foo(void){
    int a, *p;
    p = (int*)((char *)&a + 12);  //��pָ��main��������fooʱ��ջ�ķ��ص�ַ����Ч��p = (int*)(&a + 3);
    *p += 12;    //�޸ĸõ�ַ��ֵ��ʹ��ָ��һ��ָ�����ʼ��ַ
}
int __main(void){
    foo();
    printf("First printf call\n");
    printf("Second printf call\n");
    return 0;
}
