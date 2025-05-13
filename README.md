# Darbu Pārvaldnieks ar MinHeap

## 1. Projekta apraksts
Šī projekta mērķis ir izveidot komandrindas (CLI) lietojumprogrammu personīgo vai darba uzdevumu efektīvai pārvaldībai. Galvenā funkcija ir nodrošināt lietotājam iespēju ātri pievienot jaunus darbus, norādot to aprakstu un prioritāti, kā arī ērti to pārskatīt un pārvaldīt tā esošos darbus

**Galvenā funkcionalitāte:**

* **Darbu pievienošana:** Lietotājs var pievienot jaunus darbus, ievadot aprakstu un skaitlisku prioritāti. Mazāks prioritātes skaitlis nozīmē augstāku prioritāti (piemēram, 0 ir steidzami, 2 nav tik steidzami).
* **Nākamā steidzamākā darba apskate:** Programma ļauj apskatīt darbu, kuram ir visaugstākā prioritāte.
* **Darba pabeigšana:** Lietotājs var atzīmēt nākamo steidzamāko darbu kā pabeigtu, kas to noņem no darbu saraksta.
* **Visu darbu apskate:** Ir iespējams attēlot sarakstu ar visiem aktuālajiem darbiem, sakārtotus pēc to prioritātes (tas ir, 0 būs ar augstāko prioritāti).
* **Datu pastāvība:** Visi pievienotie darbi tiek saglabāti lokālā `darbi.json` failā. Tas nodrošina, ka darbi nepazūd pēc programmas aizvēršanas.
* **Sakārtota saglabāšana:** Saglabājot datus `darbi.json` failā, tie tiek sakārtoti pēc prioritātes, nodrošinot, ka faila struktūra parāda darbu steidzamību.

Programmas pamatā ir pašimplementēta MinHeap datu struktūra, kas pārvalda darbu prioritātes un nodrošina ātru piekļuvi steidzamākajam darbam.

## 2. Izmantotās Python bibltiotēkas

Projektā tiek izmantotas šādas Python bibliotēkas:

* **`datetime`**:
    * **Pielietojums:** Šī bibliotēka tiek izmantota, lai katram pievienotajam darbam piešķirtu precīzu pievienošanas laiku `datetime.datetime.now()`. Šis laiks tiek izmantots kā otrs kārtošanas kritērijs, ja vairākiem darbiem ir vienāda prioritāte, tad agrāk pievienotais darbs tiek uzskatīts par steidzamāku.
    * **Pamatojums:** `datetime` ir Python bibliotēka darbam ar datumiem un laikiem, nodrošinot visu nepieciešamo funkcionalitāti laiku iegūšanai, glabāšanai un formatēšanai.

* **`json`**:
    * **Pielietojums:** Bibliotēka tiek izmantota darbu saraksta pārveidošanai Python objektu struktūras par JSON formāta virkni un JSON virknes pārveidošanai atpakaļ par Python objektiem. Tas ļauj saglabāt visus darbus `darbi.json` failā un vēlāk tos ielādēt.
    * **Pamatojums:** JSON ir viegls, cilvēkam lasāms un plaši izplatīts datu formāts. Python `json` modulis nodrošina vienkāršu un efektīvu veidu, kā strādāt ar šo formātu, padarot datu saglabāšanu un ielādi ļoti parocīgu.

* **`os`**:
    * **Pielietojums:** Šī bibliotēka tiek izmantota operētājsistēmas funkciju veikšanai, konkrēti, lai pārbaudītu, vai datu fails (`darbi.json`) eksistē, izmantojot `os.path.exists()`. Tas ir svarīgi, lai programma korekti apstrādātu situāciju, kad tā tiek palaista pirmo reizi un datu fails vēl nav izveidots.
    * **Pamatojums:** `os` modulis nodrošina neatkarīgu no platformas veidu, kā sadarboties ar failu sistēmu, ieskaitot failu eksistences pārbaudi.

## 3. Pašu Definētās Datu Struktūras

Projektā tiek izmantotas divas galvenās pašdefinētas datu struktūras, kas realizētas kā Python klases:

### Class Darbs

* **Apraksts:** Šī klase apraksta vienu pārvaldāmo darbu sistēmā. Katrs `Darbs` objekts satur visu nepieciešamo informāciju par konkrēto darbu.
* **Atribūti:**
    * `apraksts`: Darba tekstuālais apraksts.
    * `prioritate`: Darba skaitliskā prioritāte.
    * `pievienosanas_datums`: Precīzs laiks, kad darbs tika pievienots sistēmai.
* **Galvenās Metodes:**
    * `__init__(self, apraksts, prioritate)`: Konstruktors, kas tiek izsaukts, veidojot jaunu `Darbs` objektu. Tas pārbauda atribūtus un veic ievades datu validāciju piemēram, pārbauda, vai prioritāte ir nenegatīvs vesels skaitlis.
    * `__lt__(self, other)`: Speciālā "less than" metode, kas definē, kā divi `Darbs` objekti tiek savstarpēji salīdzināti. Tas ir ļoti svarīgi `MinHeap` datu struktūras pareizai darbībai. Darbi tiek salīdzināti primāri pēc to `prioritate` atribūta. Ja prioritātes ir vienādas, tad tiek salīdzināti `pievienosanas_datums`, agrāk pievienotais ir ar augstāku prioritāti.
    * `__str__(self)`: Speciālā metode, kas atgriež lietotājam draudzīgu, formatētu teksta virkni, kas parāda `Darbs` objektu.
    * `to_dict(self)`: Pārveido `Darbs` objekta datus par Python vārdnīcu. Tas ir nepieciešams, lai objektu varētu viegli serializēt JSON formātā saglabāšanai failā.
    * `from_dict(data_dict)` statiska metode: Izveido jaunu `Darbs` objektu no Python vārdnīcas, kas parasti tiek iegūta, nolasot datus no JSON faila, kā arī veic validāciju.

### Class MinHeap

* **Apraksts:** Šī klase ir pašimplementēta MinHeap datu struktūra. Tā tiek izmantota, lai glabātu un pārvaldītu `Darbs` objektus, nodrošinot, ka darbs ar visaugstāko prioritāti vienmēr ir viegli pieejams. MinHeap tiek realizēts, izmantojot Python sarakstu `list` kā pamatni.
* **Galvenās Metodes:**
    * `__init__(self)`: Konstruktors, kas inicializē tukšu sarakstu `_heap_list`, kurā tiks glabāti heap elementi.
    * `insert(self, item)`: Pievieno jaunu elementu `Darbs` objektu heap. Pēc pievienošanas elements tiek pacelts uz augšu `_sift_up`, lai saglabātu Min-Heap īpašību.
    * `peek(self)`: Atgriež elementu no heap saknes tas ir, darbu ar visaugstāko prioritāti, bet nenoņem to no heap.
    * `extract_min(self)`: Noņem un atgriež elementu no heap saknes. Pēc saknes noņemšanas pēdējais heap elements tiek pārvietots uz sakni, un tad tas tiek nolikts uz leju `_sift_down`, lai atjaunotu Min-Heap īpašību.
    * `is_empty(self)`: Pārbauda, vai heap ir tukšs.
    * `__len__(self)`: Atgriež heap esošo elementu skaitu.
    * `get_all_tasks_sorted(self)`: Atgriež jaunu sarakstu ar visiem heap esošajiem darbiem, sakārtotiem pēc to prioritātes no augstākās uz zemāko. Tas tiek panākts, veidojot heap kopiju un secīgi no tās izņemot minimālos elementus.

## 4. Programmatūras Izmantošanas Metodes

1.  **Darbību Izvēle:**
    * Lietotājam jāievada darbības numurs.
    * Pieejamās darbības:
        * **`1. Pievienot jaunu darbu`**:
            * Programma prasīs ievadīt darba aprakstu un tā prioritāti.
            * Apraksts var būt jebkāds teksts.
            * Prioritāte jāievada kā vesels skaitlis piemēram - 0, 1, 2. Mazāks skaitlis nozīmē augstāku prioritāti.
        * **`2. Skatīt nākamo steidzamāko darbu`**:
            * Tiks parādīts darbs ar visaugstāko prioritāti.
        * **`3. Pabeigt nākamo steidzamāko darbu`**:
            * Darbs ar visaugstāko prioritāti tiks noņemts no saraksta, un par to tiks paziņots.
        * **`4. Parādīt visus darbus`**:
            * Tiks attēloti visi darbi, sakārtoti pēc to prioritātes no augstākās uz zemāko un pievienošanas datuma.
        * **`5. Saglabāt darbus`**:
            * Ļauj saglabāt visus pašreizējos darbus `darbi.json` failā. Šī darbība notiek arī automātiski, izejot no programmas.
        * **`0. Iziet`**:
            * Pārtrauc programmas darbību. Pirms iziešanas visi darbi tiek automātiski saglabāti `darbi.json` failā.

2.  **Datu Fails:**
    * Visi pievienotie un nepabeigtie darbi tiek glabāti failā ar nosaukumu `darbi.json`.
    * Šis fails tiek automātiski izveidots tajā pašā direktorijā, kur atrodas Python skripts, ja tas iepriekš nav pastāvējis.
    * Programmai startējot, dati no šī faila tiek automātiski ielādēti.
