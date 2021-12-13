# King's Valley the board game

1. <a href="#1">Złożoność.</a>
2. <a href="#2">Algorytm MinMax.</a>
3. <a href="#3">Porównanie MinMax z AlphaBeta</a>
4. <a href="#4">Porównanie AlphaBeta z AlphaBeta + sortowanie</a>
5. <a href="#5">Proof Number Search</a>
6. <a href="#6">Monte-Carlo Search</a>


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

<b>Tabela wyników dla 100 rozegranych gier:</b>

| Liczba wygranych gier algorytmu | Głębokość |
| ------------------------------- | --------- |
| 91                              | 0         |
| 96                              | 1         |
| 99                              | 2         |
| 100                             | 3         |
| 100                             | 4         |
| 100                             | 5         |
| 100                             | 6         |

Zaimplementowana funkcja kosztu jest na tyle skuteczna, że przy głębokości 0, czyli sytuacji, gdy algorytm ocenia swoje dostępne ruchy w danej turze,
jest w stanie w ok. 90% przypadków wygrać grę z losowym przeciwnikiem.

<div id="3"></div>

## Porównanie czasowe MinMax z AlphaBeta
Oba algorytmy rozegrały po 100 gier z losowym przeciwnikiem na głębokościach od 0 do 4.

| Depth | AlphaBeta avg. time for 1 game (s) | MinMax avg. time for 1 game (s) | AlphaBeta Wins | MinMax Wins |
|-------|---------------------------------|------------------------------------|--------------|-----------------|
| 0     | 0.0241                          | 0.0221                             | 93           | 91              |
| 1     | 0.1345                          | 0.1347                             | 97           | 96              |
| 2     | 0.7976                          | 1.7386                             | 100          | 99              |
| 3     | 3.7204                          | 20.2165                            | 100          | 100             |
| 4     | 41.1839                         | 613.1320                           | 100          | 100             |


<div id="4"></div>

## Porównanie czasowe AlphaBeta z AlphaBeta + sortowanie ruchów.
Oba algorytmy rozegrały po 100 gier z losowym przeciwnikiem na głębokościach od 0 do 4.

| Depth | AlphaBeta avg. time for 1 game (s) | AlphaBeta + sort avg. time for 1 game (s) | AlphaBeta Wins | AlphaBeta + sort Wins |
|-------|---------------------------------|----------------------------------------------|--------------|-------------------------|
| 0     | 0.0241                          | 0.0198                                       | 93           | 92                      |
| 1     | 0.1345                          | 0.1931                                       | 97           | 96                      |
| 2     | 0.7976                          | 0.5818                                       | 100          | 100                     |
| 3     | 3.7204                          | 2.7929                                       | 100          | 100                     |
| 4     | 41.1839                         | 26.7838                                      | 100          | 100                     |

<div id="5"></div>

## Proof Number Search
Algorytm PNS przeprowadził sprawdzenie dla różnych ograniczeń czasowych, w każdym przypadku zostało sprawdzonych końcówek 100 końcówek gier.
Początkowe ruchy zostały wykonane przez losowe algorytmy dla obydwu graczy.
PNS był ograniczany czasowo dla pojedynczej gry.


| # | Time limit (ms) | Sure win (%) | Sure lose (%) | Unsure (%) |
|---|-----------------|--------------|---------------|------------|
| 1 | 10              | 3            | 1             | 96         |
| 2 | 100             | 9            | 1             | 90         |
| 3 | 1000            | 11           | 12            | 77         |
| 4 | 10000           | 52           | 48            | 0          |
| 5 | 100000          | 56           | 44            | 0          |

<div id="6"></div>

## Monte-Carlo Search

Algorytm rozgrywał 100 gier z losowym przeciwnikiem dla różych wartości 

| # | NoF simulations | Win rate (%) | Avg. time for 1 game (s) |
|---|-----------------|--------------|--------------------------|
| 1 | 5               | 98           | 2.8699                   |
| 2 | 10              | 98           | 3.8032                   |
| 3 | 20              | 100          | 7.4858                   |
| 4 | 40              | 100          | 13.4806                  |
| 5 | 60              | 100          | 21.2179                  |
| 6 | 80              | 100          | 30.4860                  |
| 7 | 100             | 100          | 36.4503                  |

