/* timestamp.c */

#include <stdio.h>
#include <time.h>
#include <sys/stat.h>

int main(int argc,char *argv[])
{
	int option;
	char ch;
	char fnam[256];
	struct stat s;
	struct tm* t;
	struct time_t* tlocal;

	if (argc < 2 || argc > 3) {
	    printf("Usage: timestamp [option] filename\n");
	    exit(1);
	}
	option = 0;
	while ((ch = getopt(argc, argv, "01234w")) != EOF) {
	    switch (ch) {
		case '0': option = 0;
			  break;
		case '1': option = 1;
			  break;
		case '2': option = 2;
			  break;
		case '3': option = 3;
			  break;
		case '4': option = 4;
			  break;
		case 'w': option = 255;
			  break;
		default : exit(1);
	    }
        }
	strcpy(fnam, argv[argc-1]);

        if (stat(fnam, &s) < 0) {
	    printf("%s: No such file or directory.", fnam);
	    exit(1);
	}
        t = localtime(&s.st_mtime);

        if (option == 0) {
		t->tm_year -= (t->tm_year < 100 ? 0 : 100);
                printf("%02d/%02d/%02d", t->tm_year, t->tm_mon + 1, t->tm_mday);
        }
	else if (option == 1) {
		printf("%04d/%02d/%02d %02d:%02d:%02d", t->tm_year + 1900, t->tm_mon + 1, t->tm_mday, t->tm_hour, t->tm_min, t->tm_sec);
	}
	else if (option == 2) {
		t->tm_year -= (t->tm_year < 100 ? 0 : 100);
		printf("%02d/%02d/%02d %02d:%02d:%02d", t->tm_year, t->tm_mon + 1, t->tm_mday, t->tm_hour, t->tm_min, t->tm_sec);
	}
	else if (option == 3) {
		printf("%02d:%02d:%02d", t->tm_hour, t->tm_min, t->tm_sec);
	}
	else if (option == 4) {
		printf("%02d/%02d %02d:%02d", t->tm_mon + 1, t->tm_mday, t->tm_hour, t->tm_min);
	}
	else if (option == 255) {
		printf("<META NAME=\"WWWC\" CONTENT=\"%04d/%02d/%02d %02d:%02d\">", t->tm_year + 1900, t->tm_mon + 1, t->tm_mday, t->tm_hour, t->tm_min);
	}
	exit(0);
}
