"""Draft translations; Roman Life and Imperial Blends remain proper names."""
from guidrange import RANGE_START

DESCRIPTION_ID = RANGE_START + 100
TITLE = "Roman Life"
IMPERIAL_MOD = "rl-shared-khayi"
IMPERIAL_MENTIONS = {
    "english": " and Imperial Blends",
    "german": " und Imperial Blends",
    "brazilian": " e Imperial Blends",
    "french": " et d’Imperial Blends",
    "italian": " e Imperial Blends",
    "spanish": " e Imperial Blends",
    "polish": " i Imperial Blends",
    "russian": " и Imperial Blends",
    "japanese": "とImperial Blends",
    "korean": "와 Imperial Blends",
    "simplified_chinese": " 和 Imperial Blends",
    "traditional_chinese": " 和 Imperial Blends",
}


def description_without_imperial(language, description):
    mention = IMPERIAL_MENTIONS[language]
    if description.count(mention) != 1:
        raise ValueError(f"Expected one Imperial Blends mention in {language}")
    return description.replace(mention, "")

# File suffix -> (modinfo language key, mod name, tab description, mod description).
TRANSLATIONS = {
    "english": (
        "English", "Roman Life - Menu Folders",
        "Everything for a good life: Find the buildings and production chains from Roman Life and Imperial Blends for this population tier, all in one place.",
        "Groups buildings from Roman Life - Latium, Albion and Imperial Blends into construction submenus for each population tier.",
    ),
    "german": (
        "German", "Roman Life - Baumenü-Ordner",
        "Alles für ein gutes Leben: Hier findest du die Gebäude und Produktionsketten aus Roman Life und Imperial Blends – passend zu dieser Bevölkerungsstufe.",
        "Bündelt Gebäude aus Roman Life - Latium, Albion und Imperial Blends in Baumenü-Unterordnern je Bevölkerungsstufe.",
    ),
    "brazilian": (
        "Brazilian", "Roman Life - Pastas do menu de construção",
        "Tudo para uma boa vida: encontre aqui os edifícios e as cadeias de produção de Roman Life e Imperial Blends para este nível populacional, reunidos em um só lugar.",
        "Agrupa edifícios de Roman Life - Latium, Albion e Imperial Blends em submenus de construção para cada nível populacional.",
    ),
    "french": (
        "French", "Roman Life - Dossiers du menu de construction",
        "Tout pour bien vivre : retrouvez ici les bâtiments et les chaînes de production de Roman Life et d’Imperial Blends adaptés à ce niveau de population.",
        "Regroupe les bâtiments de Roman Life - Latium, Albion et Imperial Blends dans des sous-menus de construction pour chaque niveau de population.",
    ),
    "italian": (
        "Italian", "Roman Life - Cartelle del menu costruzioni",
        "Tutto per vivere bene: qui trovi gli edifici e le catene di produzione di Roman Life e Imperial Blends adatti a questo livello di popolazione.",
        "Raggruppa gli edifici di Roman Life - Latium, Albion e Imperial Blends in sottomenu di costruzione per ogni livello di popolazione.",
    ),
    "spanish": (
        "Spanish", "Roman Life - Carpetas del menú de construcción",
        "Todo para vivir bien: aquí encontrarás los edificios y las cadenas de producción de Roman Life e Imperial Blends para este nivel de población, reunidos en un solo lugar.",
        "Agrupa los edificios de Roman Life - Latium, Albion e Imperial Blends en submenús de construcción para cada nivel de población.",
    ),
    "polish": (
        "Polish", "Roman Life - Foldery menu budowy",
        "Wszystko, co potrzebne do dobrego życia: tutaj znajdziesz budynki i łańcuchy produkcyjne z Roman Life i Imperial Blends dla tego poziomu ludności, zebrane w jednym miejscu.",
        "Grupuje budynki z Roman Life - Latium, Albion i Imperial Blends w podmenu budowy dla każdego poziomu ludności.",
    ),
    "russian": (
        "Russian", "Roman Life - Папки меню строительства",
        "Всё для хорошей жизни: здесь собраны здания и производственные цепочки из Roman Life и Imperial Blends для этого уровня населения.",
        "Объединяет здания из Roman Life - Latium, Albion и Imperial Blends в подменю строительства для каждого уровня населения.",
    ),
    "japanese": (
        "Japanese", "Roman Life - 建設メニューのフォルダー",
        "豊かな暮らしに必要なものを、ここに。この住民階級に合ったRoman LifeとImperial Blendsの建物や生産チェーンが、ひとつのメニューにまとまっています。",
        "Roman Life - Latium、Albion、Imperial Blendsの建物を、住民階級ごとの建設サブメニューにまとめます。",
    ),
    "korean": (
        "Korean", "Roman Life - 건설 메뉴 폴더",
        "풍요로운 삶에 필요한 모든 것을 한곳에! 이 주민 계층에 맞는 Roman Life와 Imperial Blends의 건물과 생산 체인을 여기서 찾아보세요.",
        "Roman Life - Latium, Albion 및 Imperial Blends의 건물을 주민 계층별 건설 하위 메뉴로 묶습니다.",
    ),
    "simplified_chinese": (
        "Chinese", "Roman Life - 建造菜单文件夹",
        "美好生活，尽在此处：这里汇集了 Roman Life 和 Imperial Blends 中适合当前人口阶层的建筑与生产链，方便你随时查找。",
        "将 Roman Life - Latium、Albion 和 Imperial Blends 的建筑按人口阶层归入建造子菜单。",
    ),
    "traditional_chinese": (
        "Taiwanese", "Roman Life - 建造選單資料夾",
        "美好生活，盡在此處：這裡匯集了 Roman Life 和 Imperial Blends 中適合目前人口階層的建築與生產鏈，方便你隨時尋找。",
        "將 Roman Life - Latium、Albion 和 Imperial Blends 的建築按人口階層歸入建造子選單。",
    ),
}
