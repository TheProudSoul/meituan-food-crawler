//foo.c
void foo(void){
    int a, *p;
    p = (int*)((char *)&a + 12);  //让p指向main函数调用foo时入栈的返回地址，等效于p = (int*)(&a + 3);
    *p += 12;    //修改该地址的值，使其指向一条指令的起始地址
}
int __main(void){
    foo();
    printf("First printf call\n");
    printf("Second printf call\n");
    return 0;
}
