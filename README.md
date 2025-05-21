# Python-Project-
Šis projekts izstrādāts ar mērķi automatizēt mācību procesu. Galvenais uzdevums — izveidot rīku, kas automātiski iegūst informāciju par uzdevumiem no sistēmas e-studijas.rtu.lv, analizē datus, nosaka tuvākos termiņus un nosūta atgādinājumus.
Projekta izstrādes laikā tiek izmantotas tādas bibliotēkas kā: Selenium, BeautifulSoup, Plyer, python-dotenv, datetime.
Selenium tiek izmantots pārlūkprogrammas vadībai – lai atvērtu Google Chrome, ievadītu lietotājvārdu un paroli, piespiestu pogu datu apstiprināšanai un iegūtu informāciju no kalendāra ar uzdevumiem.
BeautifulSoup kalpo lapas koda parsēšanai un vajadzīgās informācijas meklēšanai. Šī bibliotēka projektā apstrādā HTML kodu, ko iegūst Selenium, atrod kalendāra tabulu, izvelk datumus un uzdevumu nosaukumus, kā arī sašķiro šo informāciju.
Plyer tiek izmantots, lai rādītu paziņojumus galvenajā ekrānā – tas saņem tuvāko termiņu sarakstu un izveido paziņojumu.
python-dotenv ļauj glabāt lietotājvārdu un paroli atsevišķā failā, neiekļaujot tos galvenajā kodā. Tas nolasa īpašu .env failu programmas mapē un nodod piekļuves datus Selenium tālākai autorizācijai.
datetime tiek izmantots darbam ar datumiem un laiku – tas pārveido datumus no teksta formāta uz formātu “diena-mēnesis-gads” un aprēķina, cik dienas palikušas līdz termiņam.
