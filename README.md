# IC1-projekt
## Obsah repozitara
V repozitary su 3 zlozky :
### build
Tu sa nachadza iba subor `build.bat` ktory zkompiluje vsetky zdrojaky do 4 exe suborov :
1. **client_side** - cast virtualneho terminalu ktora sa spusta na klientovy (utocnik) ked uz boli otvorene porty pomocou exploitu.
2. **server_side** - cast virtualneho terminalu ktora sa spusta na servery ma 2 argumenty *[ip_addr_ca, ip_addr_client]*. 
3. **exploit** - subor ktory utoci na tika server, spusta sa na klientovy.
4. **CertificateAuthority** - Certifikacna autorita ktora sluzy ako tretia strana pri sifrovanej komunikacii medzi sererom a klientom.
### exploit 
V tejto zlozke sa nachadza subor `commands_list.txt` v ktorom su napisane 2 prikazy na otvorenie portov na serveri pre komunikaciu z CA (4444) a klientom (3333).
V subore `exploit.py` su zdrojove kody pre exploit.exe
### virtual_cmd
V tejto zlozke su zdrojove kody pre sifrovanu komunikaciu v zlozke `communication` a subory su zdrojove kody pre client_side.exe a server_side.exe respektivne.
