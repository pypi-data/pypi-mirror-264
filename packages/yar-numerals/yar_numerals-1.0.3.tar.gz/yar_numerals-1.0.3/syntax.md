# Syntax of Compound Numbers

When the number is expanded to lexemes the problem of agreement arises. The agreement mechanism we will be using is based on dependency parsing. The basic theory aligns with approach taken by [Universal Dependency](https://universaldependencies.org/u/dep/nummod.html), however for our purposes we will introduce additional types.

## Dependency Types

Introduce following relation types:

- `num`
- `nummod:govsg` - relation to a singular numeral (to lexeme for 1)
- `nummod:govpc` - relation to a paucal numeral (to a lexeme for 2, 3, or 4)
- `nummod:govpl` - relation to a plural numeral (to any other numeral lexeme)

Note that number 11 is expanded to a single lexeme "одина́дцять" and thus has relation `nummod:govpl`. Simlarly numbers 12, 13, and 14 will have `nummod:govpl`.

## Cardinal Numerals

### Agreement of Cardinal Numerals

All `nummod` relations agrees with the parent's gender, animacy, and case. The last depending numeral lexeme will introduce one of the following governing modifiers.
The `nummod:govsg` relation always governs singular number to the parent and does not affect infered case.
The `nummod:govpc` relation takes parent's case, gender, and animacy and governs plural number.
The `nummod:govpl` relation always governs plural number to the parent and governs genitive case only when parent is in nominative or accusative, the remaining cases take precedence.

#### Subtrees

Every 3 orders of magnitude spawns a new subtree, elements of which are agreed to the aggregate numeral: 1 000, 1 000 000, 1 000 000 000, etc.
So if the number is less than a 1000 then all numeral lexems are connected to object directly. Number with any number of 1000s in it will spawn a new aggregate lexeme for number 1000 and all numerals in positions 4, 5, 6 will connect to the aggregate instead of the object. The numbers with 1 000 000 in it will have a subtree with aggregate numeral lexeme for "1 000 000" that will collect all numerals in positions 7, 8, 9. See [Examples](#Examples of Cardinal Numerals Agreement) section for more details.
What is worth noting is that these aggregate numerals have persistent grammatical gender, which differentiates them from regular numerals. So the lexeme "ти́сяча" (1 000) has persistent feminine gender thus all its child `nummod` dependencies will use that gender as basis for agreement. Lexeme "мільйо́н" (1 000 000) has masculine gender, as all the consqutive numbers in the short scale.

### Examples of Cardinal Numerals Agreement

#### Singular `nummod:govsg`

The forms for the number `1 021 131` (оди́н мільйо́н два́дцять одна́ ти́сяча сто́ три́дцять оди́н)

| Case | Aux. Verb | 1 | 1 000 000 | 20 | 1 | 1000 | 100 | 30 | 1 | Obj. |
|---|---|---|---|---|---|---|---|---|---|---|
| nominative | є́ | оди́н{nom;m} | мільйо́н{M;nom;sg} | два́дцять{nom;f} | одна́{nom;f} | ти́сяча{F;nom;sg} | сто́{nom;n} | три́дцять{nom;n} | одне́{nom;n} | я́блуко{N;nom;sg} |
| genitive | нема́є | одного́{gen;m} | мільйо́на{M;gen;sg} | двадцяти́{gen;f} | одніє́ї{gen;f} | ти́сячі{F;gen;sg} | ста́{gen;n} | тридцяти́{gen;n} | одного́{gen;n} | я́блука{N;gen;sg} |
| dative | даю́ | одному́{dat;m} | мільйо́ну{M;dat;sg} | двадцяти́{dat;f} | одні́й{dat;f} | ти́сячі{F;dat;sg} | ста́{dat;n} | тридцяти́{dat;n} | одному́{dat;n} | я́блуку{N;dat;sg} |
| accusative | ба́чу | оди́н{acc;m} | мільйо́н{M;acc;sg} | два́дцять{acc;f} | одну́{acc;f} | ти́сячу{F;acc;sg} | сто́{acc;n} | три́дцять{acc;n} | одне́{acc;n} | я́блуко{N;acc;sg} |
| instrumental | пиша́юся | одни́м{inst;m} | мільйо́ном{M;inst;sg} | двадцятьма́{inst;f} | одніє́ю{inst;f} | ти́сячею{F;inst;sg} | ста́{inst;n} | тридцятьма́{inst;n} | одни́м{inst;n} | я́блуком{N;inst;sg} |
| locative | стою́ на́ | одному́{loc;m} | мільйо́ні{M;loc;sg} | двадцяти́{loc;f} | одні́й{loc;f} | ти́сячі{F;loc;sg} | ста́{loc;n} | тридцяти́{loc;n} | одному́{loc;n} | я́блуку{N;loc;sg} |

```mermaid
graph TD
    A("root") --> B["я́блуко{N;nom;sg}"]
    B --> |nummod| C["мільйо́н{M;nom;sg}"]
    C --> |nummod:govsg| D["оди́н{nom;m}"]
    B --> |nummod| E["ти́сяча{F;nom;sg}"]
    E --> |nummod| F["два́дцять{nom;f}"]
    E --> |nummod:govsg| G["одна́{nom;f}"]
    B --> |nummod| B1["сто́{nom;n}"]
    B --> |nummod| B2["три́дцять{nom;n}"]
    B --> |nummod:govsg| B3["одне́{nom;n}"]
```

#### Paucal `nummod:govpc`

The forms for the number `2 034 643` (два́ мільйо́ни три́дцять чоти́ри ти́сячі шістсо́т со́рок три́)

| Case | Aux. Verb | 2 | 1 000 000 | 30 | 4 | 1000 | 600 | 40 | 3 | Obj. |
|---|---|---|---|---|---|---|---|---|---|---|
| nominative | є́ | два́{nom;m} | мільйо́ни{M;nom;pl} | три́дцять{nom;f} | чоти́ри{nom;f} | ти́сячі{F;nom;pl} | шістсо́т{nom;n} | со́рок{nom;n} | три́{nom;n} | я́блука{N;gen;sg} |
| genitive | нема́є | дво́х{gen;m} | мільйо́нів{M;gen;pl} | тридцяти́{gen;f} | чотирьо́х{gen;f} | ти́сяч{F;gen;pl} | шестисо́т{gen;n} | сорока́{gen;n} | трьо́х{gen;n} | я́блук{N;gen;pl} |
| dative | даю́ | дво́м{dat;m} | мільйо́нам{M;dat;pl} | тридцяти́{dat;f} | чотирьо́м{dat;f} | ти́сячам{F;dat;pl} | шестиста́м{dat;n} | сорока́{dat;n} | трьо́м{dat;n} | я́блукам{N;dat;pl} |
| accusative | ба́чу | два́{acc;m;inan} | мільйо́ни{M;INAN;acc;pl} | три́дцять{acc;f;inan} | чоти́ри{acc;f;inan} | ти́сячі{F;INAN;acc;pl} | шістсо́т{acc;n;inan} | со́рок{acc;n;inan} | три́{acc;n;inan} | я́блука{N;gen;pl} |
| instrumental | пиша́юся | двома́{inst;m} | мільйо́нами{M;inst;pl} | тридцятьма́{inst;f} | чотирма́{inst;f} | ти́сячами{F;inst;pl} | шістьмаста́ми{inst;n} | сорока́{inst;n} | трьома́{inst;n} | я́блуками{N;acc;pl} |
| locative | стою́ на́ | дво́х{loc;m} | мільйо́нах{M;loc;pl} | тридцяти́{loc;f} | чотирьо́х{loc;f} | ти́сячах{F;loc;pl} | шестиста́х{loc;n} | сорока́{loc;n} | трьо́х{loc;n} | я́блуках{N;loc;pl} |

```mermaid
graph TD
    A("root") --> B["я́блука{N;gen;sg}"]
    B --> |nummod| C["мільйо́ни{M;nom;pl}"]
    C --> |nummod:govpc| D["два́{nom;m}"]
    B --> |nummod| E["ти́сячі{F;nom;pl}"]
    E --> |nummod| F["три́дцять{nom;f}"]
    E --> |nummod:govpc| G["чоти́ри{nom;f}"]
    B --> |nummod| B1["шістсо́т{nom;n}"]
    B --> |nummod| B2["со́рок{nom;n}"]
    B --> |nummod:govpc| B3["три́{nom;n}"]
```

#### Plural `nummod:govpl`

The forms for the number `6 013 845` (ші́сть мільйо́нів трина́дцять ти́сяч вісімсо́т со́рок пʼя́ть)

| Case | Aux. verb | 6 | 1 000 000 | 13 | 1000 | 800 | 40 | 5 | Obj. |
|---|---|---|---|---|---|---|---|---|---|
| nominative | є́ | ші́сть{nom;m} | мільйо́нів{M;gen;pl} | трина́дцять{nom;f} | ти́сяч{F;gen;pl} | вісімсо́т{nomn;n} | со́рок{nom;n} | пʼя́ть{nom;n} | я́блук{N;gen;pl} |
| genitive | нема́є | шести́{gen;m} | мільйо́нів{M;gen;pl} | тринадцяти́{gen;f} | ти́сяч{F;gen;pl} | восьмисо́т{gen;n} | сорока́{gen;n} | пʼяти́{gen;n} | я́блук{N;gen;pl} |
| dative | даю́ | шести́{dat;m} | мільйо́нам{M;dat;pl} | тринадцяти́{dat;f} | ти́сячам{F;dat;pl} | восьмиста́м{dat;n} | сорока́{dat;n} | пʼяти́{dat;n} | я́блукам{N;dat;pl} |
| accusative | ба́чу | ші́сть{acc;m} | мільйо́нів{M;gen;pl} | трина́дцять{acc;f} | ти́сяч{F;gen;pl} | вісімсо́т{acc;n} | со́рок{acc;n} | пʼя́ть{acc;n} | я́блук{N;gen;pl} |
| instrumental | пиша́юся | шістьма́{inst;m} | мільйо́нами{M;inst;pl} | тринадцятьма́{inst;f} | ти́сячами{F;inst;pl} | вісьмаста́ми{inst;n} | сорока́{inst;n} | пʼятьма́{inst;n} | я́блуками{N;inst;pl} |
| locative | стою́ на́ | шести́{loc;m} | мільйо́нах{M;loc;pl} | тринадцяти́{loc;f} | ти́сячах{F;loc;pl} | восьмиста́х{loc;n} | сорока́{loc;n} | пʼяти́{loc;n} | я́блуках{N;loc;pl} |

```mermaid
graph TD
    A("root") --> B["я́блук{N;gen;pl}"]
    B --> |nummod| C["мільйо́нів{M;gen;pl}"]
    C --> |nummod:govpl| D["ші́сть{nom;m}"]
    B --> |nummod| E["ти́сяч{F;gen;pl}"]
    E --> |nummod:govpl| G["трина́дцять{nom;f}"]
    B --> |nummod| B1["вісімсо́т{nom;n}"]
    B --> |nummod| B2["со́рок{nom;n}"]
    B --> |nummod:govpl| B3["пʼя́ть{nom;n}"]
```

## Ordinal Numerals

### Agreement of Ordinal Numerals

Regular ordinal numerals connect to the object with the [`amod`](https://universaldependencies.org/u/dep/amod.html) relation. And accordingly takes on the parent's case, gender, number, and animacy. This relation is not governing. Only the last numeral is inflected as an ordinal, all remamining are inflected as cardinal and are connected directly with the object with the `num` relation.

`[пиша́юсь] 46 013 845-м я́блуком`

```mermaid
graph TD
    A("root") --> B["я́блуком{N;inst;sg}"]
    B --> |num| H["мільйо́нів{M;gen;pl}"]
    H --> |nummod| J["со́рок{nom;m}"]
    H --> |nummod:govpl| I["ші́сть{nom;m}"]
    B --> |num| F["ти́сяч{F;gen;pl}"]
    F --> |nummod:govpl| G["трина́дцять{nom;f}"]
    B --> |num| E["вісімсо́т{nom;n}"]
    B --> |num| D["со́рок{nom;n}"]
    B --> |amod| C["пʼя́тим{inst;n}"]
```

If the numeral ends with noun numeral (1000, 1 000 000, etc.) then it combines its three ranks into one compound numeral. The remaining numerals are inflected normally.

`[немає] 692 525 000-го я́блука`
`[немає] чоти́ри мілья́рда девʼяно́сто два́ мільйо́на пʼятисотдвадцятипʼятити́сячного я́блука`

```mermaid
graph TD
    A("root") --> B["я́блука{N;gen;sg}"]
    subgraph C ["compound"]
        direction RL
        D["ти́сячного{gen;n;sg}"] -.- E["пʼяти{gen;n}"]
        E -.- F["двадцяти{gen;n}"]
        F -.- G["пʼятисот{gen;n}"]
    end
    B --> |num| K["мілья́рдів{M;gen;pl}"]
    K --> |nummod:govpl| L["ші́сть{nom;m}"]
    B --> |num| H["мільйо́на{M;gen;sg}"]
    H --> |nummod| I["девʼяно́сто{nom;m}"]
    H --> |nummod:govpc| J["два́{nom;m}"]
    B ---> |amod| C
```

## Fractional Numerals

### Agreement of Fractional Numerals

`[ба́чу] пʼя́ть мільйо́нів со́рок одну́ два́ мільйо́ни сімдеся́т пе́ршу [части́ну] я́блука`
`[ба́чу] пʼя́ть мільйо́нів со́рок дві́ два́ мільйо́ни сімдеся́т пе́рших [части́ни] я́блука`

пишаюсь пʼятьма другими яблука
пишаюсь однією другою яблука
пишаюсь двома другими яблука
