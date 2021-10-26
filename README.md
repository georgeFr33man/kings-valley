# King's Valley the board game

1. <a href="#1">Złożoność.</a>
2. <a href=#2>Algorytm MinMax.</a>


<div id="1"></div>

## Złożoność:

### Metoda pierwsza:
obliczenia na podstawie 10 000 rozegranych, losowych gier, wyniki uśrednione ze statystyk dla obydwu graczy.

##### Branching factor, `b = 14`  
W czasie gry każdy z graczy może ruszać swoimi pionkami w każdym możliwym kierunku, ale zawsze jak najdalej (pionek musi zatrzymać się na polu sąsiadującym z innym pionkiem lub na brzegu planszy).

##### Depth, `d = 19`  
Średnia liczba wykonanych ruchów w czasie gry, sumarycznie przez obu graczy wyniosła 19. Ze względu na całkowicie losowy charakter wyboru ruchów wynik z dużym prawdopodobiestwem został zawyżony (stany planszy były wielokrotnie powtarzane). Minimalna liczba sumy wykonanch ruchów obu graczy, która wystąpiła w 10 000 zagranych grach wyniosła 4, a maksymalna zaobserwowana - 91.

Złożoność gry wyniosła: `14^19`, czyli `5.976303958948914397184 * 10^21`


### Metoda druga:
wygenerowano 10 000 losowych stanów gry, z czego 70% stanów było poprawnych. Poprawny stan w przypadku King’s Valley to stan, w którym żaden z pionków nie znajduje się na środku planszy, tylko król może zajmować tę pozycję.

Plansza składa się z 25 pól, korzystając ze wzoru na permutację z powtórzeniami obliczyłem, że liczba wszystkich możliwych permutacji zbioru elementów na planszy wynosi:

`25!/(4! * 4! * 15!) = 20 593 188 000`  
Z czego 70% stanów jest możliwych, czyli. <b>14 415 231 600</b> stanów.

<div id="2"></div>

## Algorytm MinMax

Implementacja algorytmu MinMax została zaimplementowana tak by kierować ruchami jednego z graczy. Celem algorytmu jest doprowadzić do przegranej swojego przeciwnika (losowego lub drugiego algorytmu).
W grze King's Valley nie jest możliwy remis.

<b>Funkcja kosztu</b> algorytmu sprowadza się do sprawdzania najważniejszych elementów rozgrywki, w kolejności:
- ruch wygrywa:
  - poprzez ruch przyjaznego króla na środek planszy lub zablokowanie króla przeciwnika,
  - wartość: <b>1 000 000</b>
- ruch przegrywa:
  - poprzez zablokowanie przyjaznego króla,
  - wartość: <b>-1 000 000</b>
- ruch spowoduje przegraną algorytmu w turze przeciwnika:
  - sprawdzane jest czy pionek na nowej pozycji umożliwia przeciwnikowi ruch królem na środek planszy,
  - wartość: <b>-900 000</b>
- ruch umożliwia wygraną w następne turze:
  - sprawdzane jest czy pionek na nowej pozycji daje możliwość ruchu królem na środek planszy,
  - wartość: <b>900 000</b>
- ruch odbiera możliwość wygranej przeciwnikowi:
  - postawienie piona na nowej pozycji powoduje, że król przeciwnika nie może już poruszyć się na środek planszy, jeśli wcześniej miał taką możliwość,
  - wartość: <b>250 000</b>
- ruch powoduje zwiększenie liczby możliwych ruchów przyjaznego króla:
  - jeżeli pion stoi obok przyjaznego króla a po wykonaniu ruchu nie będzie znajdować się w pozycji sąsiadującej z przyjaznym królem to ruch "uwalnia" króla,
  - wartość: <b>250 000</b>
- ruch powoduje zmniejszenie liczby ruchów przyjaznego króla:
  - jeżeli ruch piona to ruch na pozycję sąsiadującą z pozycją przyjaznego króla, to ruch zmniejsza liczbę ruchów przyjaznego króla,
  - wartość: <b>-500 000</b>
- ruch powoduje zmniejszenie liczby ruchów króla przeciwnika:
  - jeżeli ruch piona to ruch na pozycję sąsiadującą z pozycją króla przeciwnika, to ruch zmniejsza liczbę ruchów króla przeciwnika,
  - wartość: <b>500 000</b>






