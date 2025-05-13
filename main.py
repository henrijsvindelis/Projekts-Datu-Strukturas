import datetime
import json
import os


class Darbs:
    ##Klase, kas reprezentē vienu darbu. Prioritāte tiek glabāta kā skaitlis (mazāks skaitlis = augstāka prioritāte) .Salīdzināšana notiek pēc šī skaitļa un tad pēc pievienošanas datuma.
    
    def __init__(self, apraksts, prioritate): # Atgriežamies pie skaitliskas prioritātes
        if not isinstance(apraksts, str) or not apraksts.strip():
            raise ValueError("Aprakstam jābūt nepārprotamai tekstvirknei.")
        if not isinstance(prioritate, int) or prioritate < 0:
            # Atļaujam jebkuru veselu skaitli kā prioritāti
            raise ValueError("Prioritātei jābūt veselam skaitlim.")
            
        self.apraksts = apraksts
        self.prioritate = prioritate 
        self.pievienosanas_datums = datetime.datetime.now()

    def __lt__(self, other):
        ## Salīdzina divus darbus (less than - priekš MinHeap).
        if not isinstance(other, Darbs):
            return NotImplemented # Svarīgi pareizai salīdzināšanai
        if self.prioritate == other.prioritate:
            return self.pievienosanas_datums < other.pievienosanas_datums
        return self.prioritate < other.prioritate

    def __str__(self):
        ## Atgriež lietotājam darbu attēlojumu.
        datums_formatets = self.pievienosanas_datums.strftime("%Y-%m-%d %H:%M:%S")
        return f"[Prioritāte: {self.prioritate}] {self.apraksts} (Pievienots: {datums_formatets})"

    def to_dict(self):
        ## Pārveido darba objektu par vārdnīcu JSON serializācijai.
        return {
            'apraksts': self.apraksts,
            'prioritate': self.prioritate,
            'pievienosanas_datums': self.pievienosanas_datums.isoformat()
        }

    @staticmethod
    def from_dict(data_dict):
        ## Izveido darbs objektu no vārdnīcas (no JSON).
        if not all(key in data_dict for key in ['apraksts', 'prioritate', 'pievienosanas_datums']):
            raise ValueError("JSON objektam trūkst nepieciešamo atslēgu (apraksts, prioritate, pievienosanas_datums).")
        
        drb = Darbs(data_dict['apraksts'], data_dict['prioritate'])
        # Pārbauda datuma formātu
        try:
            drb.pievienosanas_datums = datetime.datetime.fromisoformat(data_dict['pievienosanas_datums'])
        except ValueError:
            raise ValueError(f"Nekorekts datuma formāts JSON objektā: {data_dict['pievienosanas_datums']}")
        return drb

# MinHeap Klase
class MinHeap:
    def __init__(self):
        self._heap_list = []
    def _parent(self, index): return (index - 1) // 2
    def _left_child(self, index): return 2 * index + 1
    def _right_child(self, index): return 2 * index + 2
    def _swap(self, i, j): self._heap_list[i], self._heap_list[j] = self._heap_list[j], self._heap_list[i]
    def _sift_up(self, index):
        parent_index = self._parent(index)
        while index > 0 and self._heap_list[index] < self._heap_list[parent_index]:
            self._swap(index, parent_index); index = parent_index; parent_index = self._parent(index)
    def _sift_down(self, index):
        max_index = len(self._heap_list) - 1
        while True:
            left_child_index = self._left_child(index)
            right_child_index = self._right_child(index)
            smallest = index
            if left_child_index <= max_index and self._heap_list[left_child_index] < self._heap_list[smallest]:
                smallest = left_child_index
            if right_child_index <= max_index and self._heap_list[right_child_index] < self._heap_list[smallest]:
                smallest = right_child_index
            if smallest != index: self._swap(index, smallest); index = smallest
            else: break
    def insert(self, item): self._heap_list.append(item); self._sift_up(len(self._heap_list) - 1)
    def peek(self): return self._heap_list[0] if not self.is_empty() else None
    def extract_min(self):
        if self.is_empty(): return None
        min_item = self._heap_list[0]
        if len(self._heap_list) == 1: self._heap_list.pop(); return min_item
        last_item = self._heap_list.pop()
        self._heap_list[0] = last_item
        self._sift_down(0)
        return min_item
    def is_empty(self): return len(self._heap_list) == 0
    def __len__(self): return len(self._heap_list)
    def get_all_tasks_sorted(self):
        sorted_tasks = []; temp_heap = MinHeap(); temp_heap._heap_list = list(self._heap_list)
        while not temp_heap.is_empty(): sorted_tasks.append(temp_heap.extract_min())
        return sorted_tasks

## CLI prompti 
DARBA_FAILS = "darbi.json" 

def pievienot_darbu(heap_obj):
    print("\n--- Pievienot jaunu darbu ---")
    while True:
        apraksts = input("Ievadiet darba aprakstu: ").strip()
        if apraksts: break
        else: print("Apraksts nevar būt tukšs.")
    
    while True:
        try:
            prioritate_str = input("Ievadiet prioritāti (vesels skaitlis, piem., 0, 1, 2; mazāks = svarīgāks): ").strip()
            prioritate = int(prioritate_str)
            if prioritate < 0:
                print("Prioritātei jābūt nenegatīvam skaitlim.")
                continue
            break
        except ValueError:
            print("Nederīga ievade. Lūdzu, ievadiet veselu skaitli prioritātei.")
    try:
        darbs = Darbs(apraksts, prioritate)
        heap_obj.insert(darbs)
        print(f"darbs '{darbs.apraksts}' pievienots ar prioritāti {darbs.prioritate}.")
    except ValueError as e:
        print(f"Kļūda pievienojot darbu: {e}")

def skatit_nakamo_darbu(heap_obj):
    print("\n--- Nākamais steidzamākais darbu ---")
    nakamais = heap_obj.peek()
    if nakamais: print(nakamais)
    else: print("darbu saraksts ir tukšs.")

def pabeigt_nakamo_darbu(heap_obj):
    print("\n--- Pabeigt nākamo darbu ---")
    pabeigtais = heap_obj.extract_min()
    if pabeigtais: print(f"Pabeigts darbs: {pabeigtais}")
    else: print("Darbu saraksts ir tukšs, nav ko pabeigt.")

def paradit_visus_darbus(heap_obj):
    print("\n--- Visi darbi (sakārtoti pēc prioritātes) ---")
    if heap_obj.is_empty(): print("Darbu saraksts ir tukšs."); return
    visi_darbi = heap_obj.get_all_tasks_sorted()
    if not visi_darbi: print("Darbu saraksts ir tukšs.")
    else:
        for idx, drb in enumerate(visi_darbi): print(f"{idx + 1}. {drb}")

def saglabat_darbus(heap_obj, faila_nosaukums=DARBA_FAILS):
    ## Saglabā visus darbus no heap JSON failā, sakārtotus pēc prioritātes.
    # Iegūstam darbus sakārtotā secībā no heap
    darbi_sarakstam = heap_obj.get_all_tasks_sorted() 

    darbi_vardnicu_saraksts = [drb.to_dict() for drb in darbi_sarakstam]

    try:
        with open(faila_nosaukums, 'w', encoding='utf-8') as f:
            # Saglabājam sarakstu ar vārdnīcām JSON failā
            json.dump(darbi_vardnicu_saraksts, f, ensure_ascii=False, indent=4)
        print(f"darbi saglabāti failā '{faila_nosaukums}' sakārtotā secībā.")
    except IOError:
        print(f"Kļūda, saglabājot darbu failā '{faila_nosaukums}'.")
    except Exception as e:
        print(f"Nezināma kļūda saglabājot: {e}")


def ieladet_darbs(faila_nosaukums=DARBA_FAILS):
    ## Ielādē darbus no JSON faila un izveido jaunu MinHeap objektu.
    heap_obj = MinHeap()
    if not os.path.exists(faila_nosaukums):
        print(f"Fails '{faila_nosaukums}' nav atrasts. Tiek sākts ar tukšu darbu sarakstu.")
        return heap_obj
    try:
        with open(faila_nosaukums, 'r', encoding='utf-8') as f:
            dati_saraksta_veida = json.load(f) # Nolasām visu JSON failu kā sarakstu ar vārdnīcām
        
        # Katru vārdnīcu pārvēršam par darba objektu un ievietojam heapā
        # `insert` metode nodrošina heap struktūru atmiņā.
        for dati_drb_vardnica in dati_saraksta_veida:
            try:
                darbs = Darbs.from_dict(dati_drb_vardnica)
                heap_obj.insert(darbs)
            except ValueError as e_val:
                print(f"Kļūda ielādējot darbu no JSON datu: {dati_drb_vardnica}. Kļūda: {e_val}")
            except Exception as e_gen:
                 print(f"Nezināma kļūda apstrādājot darbu datus: {dati_drb_vardnica}. Kļūda: {e_gen}")

        print(f"darbi ielādēti no faila '{faila_nosaukums}'.")
    except (IOError, json.JSONDecodeError) as e: # dekodēšanas kļūdas
        print(f"Kļūda, ielādējot darbus no '{faila_nosaukums}': {e}. Tiek sākts ar tukšu sarakstu.")
        return MinHeap() # Atgriežam tukšu heap ja ir kļūda
    except Exception as e_outer:
        print(f"Negaidīta kļūda ielādējot darbus: {e_outer}. Tiek sākts ar tukšu sarakstu.")
        return MinHeap()
    return heap_obj

# Main cikls
def main():
    darbu_kaudze = ieladet_darbs()
    while True:
        print("\n--- Darbu Pārvaldnieks ---")
        print("Izvēlieties darbību:")
        print("1. Pievienot jaunu darbu")
        print("2. Skatīt nākamo steidzamāko darbu")
        print("3. Pabeigt nākamo steidzamāko darbu")
        print("4. Parādīt visus darbus")
        print("5. Saglabāt darbus")
        print("0. Iziet")
        izvele = input("Jūsu izvēle: ")
        if izvele == '1': pievienot_darbu(darbu_kaudze)
        elif izvele == '2': skatit_nakamo_darbu(darbu_kaudze)
        elif izvele == '3': pabeigt_nakamo_darbu(darbu_kaudze)
        elif izvele == '4': paradit_visus_darbus(darbu_kaudze)
        elif izvele == '5': saglabat_darbus(darbu_kaudze)
        elif izvele == '0':
            saglabat_darbus(darbu_kaudze)
            print("Darbs pabeigts. darbi saglabāti."); break
        else: print("Nederīga izvēle. Lūdzu, mēģiniet vēlreiz.")

if __name__ == "__main__":
    main()


