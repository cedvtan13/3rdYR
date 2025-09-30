#include <stdio.h>
#include <unistd.h>

int main(){
  fork();
  fork();
  printf("hey\n");

  // if (getpid() == 0){printf("I am the child, my id is %d\n", getpid());}

  // else {printf("I am the parent, my id is %d\n", getpid());}
}