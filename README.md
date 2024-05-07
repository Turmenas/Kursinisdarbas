# Kursinisdarbas
# Įvadas

Kursiinio darbo tikslas buvo kurti žaidimą, laikantis objektinio programavimo reikalavimų. Programa yra požemių nagrinėjimo žaidimas su viršaus perspektyva.

Norint paleisti programą, reikia įdiegti `pygame-ce` ir `pytmx` bibliotekas. Norint paleisti programą, reikia atidaryti terminalą ten, kur yra programos failai, ir įrašyti komandą `python main.py`.

## Pagrindiniai valdymo klavišai

- **wasd**: veikėjo valdymo klavišai
- **dešinysis pelės klavišas**: priešų išvengimas, kurio metu veikėjas negali mirti

## Analizė

**Polimorfizmas** yra pagrindinė objektinio programavimo koncepcija, leidžianti traktuoti skirtingų klasių objektus kaip bendros superklasės objektus.

```python
class Scene(State):
    def __init__(self, game, current_scene, entry_point):
        State.__init__(self, game)

    def update(self, dt):
        self.update_sprites.update(dt)
        self.camera.update(dt, self.target)
        if self.player.check_chest_collision():
            EndScreen(self.game).enter_state()
```
Apibrėžiant konkretų „update()“ įgyvendinimą „Scene“, polimorfizmas leidžia „Scene“ pritaikyti elgseną (atnaujinti vaizdus, kamerą, susidūrimų aptikimą), laikantis bendros „Update()“ metodo sutarties, apibrėžtos "State”.

**Abstrakcija** yra sąvoka, apimanti pagrindines savybes ir neesminių detalių ignoravimą. Tai būdas supaprastinti sudėtingas sistemas ar problemas, pabrėžiant tai, kas svarbu, ir nuslopinant nereikalingas detales.

**Abstrakcijos pavyzdys kode**:
```python
class State(ABC):  
  
@abstractmethod  
def update(self, dt):  
pass  
  
@abstractmethod  
def draw(self, screen):  
pass
```
- Būsenos klasė apibrėžia abstrakčius metodus update() ir draw() naudojant @abstractmethod dekoratorių.

- Šie abstraktūs metodai tarnauja kaip sutartis, reikalaujanti, kad poklasiai (TitleScreen, EndScreen, Scene) įgyvendintų savo specifinę atnaujinimo ir piešimo logiką, tačiau tiksli įgyvendinimo detalė paliekama poklasiams.

- Abstrakcija leidžia valstijai apibrėžti sąsają skirtingoms žaidimo būsenoms, nenurodant, kaip kiekviena būsena turi būti įgyvendinta.

Objektiniame programavime **paveldėjimas** yra pagrindinė sąvoka, leidžianti naujai klasei paveldėti savybes ir elgesį (metodus) iš esamos klasės. Ši koncepcija skatina kodo pakartotinį naudojimą ir nustato hierarchinį ryšį tarp klasių.

**Paveldėjimo naudojimas kode:**

```python
class TitleScreen(State): 
    def __init__(self, game): 
        State.__init__(self, game) 

    def update(self, dt): 
        if INPUTS['space']: 
            Scene(self.game, '0', '0').enter_state() 
            self.game.reset_inputs() 

    def draw(self, screen): 
        screen.fill(COLORS['black']) 
        self.game.render_text('Press space to play', COLORS['white'], self.game.font, (WIDTH/2, HEIGHT/2), centered=True)
  ```
- TitleScreen klasė paveldi iš „State“ klasės, paveldi jos atributus ir metodus.  
- TitleScreen metodas __init__() iškviečia savo superklasės (State) metodą __init__(), inicijuodamas paveldėtus atributus (game).
- Paveldėdamas metodus update() ir draw() iš State, „TitleScreen“ gali apibrėžti konkretų jo įgyvendinimą, pakartotinai naudodamas apibendrintą būsenoje apibrėžtą elgesį.

**Inkapsuliacija** yra pagrindinė objektinio programavimo koncepcija, apibūdinanti idėją sujungti duomenis ir metodus, kurie veikia su duomenimis į vieną vienetą arba klasę. Inkapsuliavimo tikslas yra paslėpti vidinę objekto būseną ir tik atskleisti kontroliuojamą sąsają sąveikai su tuo objektu.

**Inkapsuliacijos naudojimas kode:**

```python
class State(ABC): 
    def __init__(self, game): 
        self.game = game 
        self.prev_state = None 

    def enter_state(self): 
        if len(self.game.states) < 1: 
            self.prev_state = self.game.states[-1] 
        self.game.states.append(self) 

    def exit_state(self): 
        self.game.states.pop() 

    @abstractmethod 
    def update(self, dt): 
        pass 

    @abstractmethod 
    def draw(self, screen): 
        pass 
```
- State“ klasė apima žaidimo būsenos sąvoką, sujungdama tokius atributus kaip žaidimas ir prev_state.
- Tokie metodai kaip enter_state() ir exit_state() apima elgesį, susijusį su perėjimu į žaidimo būsenas ir iš jos.
- Prieiga prie žaidimo atributo yra kontroliuojama State klasėje, išlaikant inkapsuliavimą ir užkertant kelią tiesioginiam manipuliavimui iš išorės.

**Abstract Factory** modelis naudojamas sąsajai sukurti susijusių arba priklausomų objektų šeimoms, nenurodant konkrečių jų klasių. Kodo pavyzdyje „Scene“ klasė dinamiškai kuria skirtingų tipų žaidimo objektus (Wall, Background, Barrier, Player, Enemy, Chest), remdamasi įkeltuose TMX duomenyse esančiais sluoksniais.

**Kodo fragmentas, kuriame naudojamas Abstract Factory modelis:**

```python
def create_scene(self): 
    layers = [] 
    for layer in self.tmx_data.layers: 
        layers.append(layer.name) 

    if 'blocks' in layers: 
        for x, y, surf in self.tmx_data.get_layer_by_name('blocks').tiles(): 
            Wall([self.block_sprites, self.drawn_sprites], (x * TILE_SIZE, y * TILE_SIZE), 'blocks', surf) 

    if 'background' in layers: 
        for x, y, surf in self.tmx_data.get_layer_by_name('background').tiles(): 
            Background([self.block_sprites, self.drawn_sprites], (x * TILE_SIZE, y * TILE_SIZE), 'background', surf) 

    if 'semiblocks' in layers: 
        for x, y, surf in self.tmx_data.get_layer_by_name('semiblocks').tiles(): 
            Barrier([self.block_sprites, self.drawn_sprites], (x * TILE_SIZE, y * TILE_SIZE), 'semiblocks', surf) 

    if 'entities' in layers: 
        for obj in self.tmx_data.get_layer_by_name('entities'): 
            if obj.name == 'enemy': 
                self.enemy = Enemy(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'blocks', 'enemy') 
            if obj.name == 'chest': 
                self.chest = Chest(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'characters', 'chest') 
```
**Singleton** modelis užtikrina, kad klasė turi tik vieną egzempliorių ir suteikia visuotinį prieigos prie jos tašką. Kode „Game“ klasė gali būti laikoma viena, nes paprastai žaidimo programoje yra vienas pagrindinės žaidimo kilpos ir tvarkyklės pavyzdys.

**Kodo fragmentas:**

```python
if __name__ == "__main__": 
    game = Game() 
    game.loop()
```
Čia  Game() klasė  yra  instantiuojama  vieną  kartą (game = Game()) ir  tuo  atveju  iškviečiamas  loop() metodas. Tai atitinka Singleton modelį, užtikrinant, kad  būtų  vykdomas  vienas  žaidimo  egzempliorius.

Programoje skaitomi duomenys iš TMX ir CSV tipo failų. Iš TMX failų perskaitomas žaidimo lygio vaizdas ir tekstūrų sluoksniai, kurie nustato, kuri tekstūra bus rodoma virš kitos. Duomenys iš CSV failų naudojami nustatyti lygio ribas, kad žaidimo kamera neišeitų už jų.

```python
import csv

def get_scene_size(self, scene): 
    with open(f'scenes/{scene.current_scene}/{scene.current_scene}_blocks.csv', newline='') as csvfile: 
        reader = csv.reader(csvfile, delimiter=',') 
        rows = sum(1 for row in reader) + 1  # Skaičiuojame eilučių skaičių
        csvfile.seek(0)  # Grąžiname CSV failą į pradinę poziciją
        cols = len(next(reader))  # Skaičiuojame stulpelių skaičių
    return (cols * TILE_SIZE, rows * TILE_SIZE)
```
## Rezultatai ir išvados

### Rezultatai

- Žaidimo kūrimas buvo sunkesnis nei kitų programų kūrimas, nes reikėjo ne tik programavimo žinių, bet ir meninių įgūdžių.
  
- Sukurti NPC priešą, kuris atsitiktinai pasirenka judėjimo kryptį, buvo daug sunkiau nei tikėtasi.

### Išvados

Šis projektas leido įtvirtinti ir pagilinti objektinio programavimo žinias. Tai veikiantis žaidimas, kuriame žaidėjas turi pasiekti "lobį", kad jį laimėtų. Žaidimas kol kas yra labai trumpas ir net neturi būdo žaidėjui pulti priešus. Programa būtų galima plėsti, sukurdami daugiau NPC tipų, plėtojant žaidėjo veiksmus ir NPC galimybes arba tiesiog sukurdami daugiau lygių.

