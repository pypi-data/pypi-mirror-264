# Ukrainian Numbers Spellout

This library allows to convert the numbers into numerals

## Supported Features

- [x] Number spellout – converting numbers into text (numerals)
- [x] Numeral inflection - modifying grammatical form of numerals to match required grammatical characteristics
- [x] Agreement - setting grammatical forms of compound numerals to produce grammatically and syntactically correct text
- [x] Stress
- [x] Cardinal numbers in range [0...1×10<sup>27</sup>)<sup>_1_, _2_</sup>
- [x] Ordinal numbers in range [0...1×10<sup>27</sup>)<sup>_1_</sup>
- [x] Fractional numbers with whole, each element in range [0...1×10<sup>27</sup>)
- [x] Decimal numbers in range (0...1×10<sup>27</sup>) with precision up to 1×10<sup>-27</sup> <sup>_3_</sup>

---

<sup>_1_</sup> Numbers outside of the range will be spelled out digit-wise and inflected only last digit

<sup>_2_</sup> 1×10<sup>27</sup> is 1 000 000 000 000 000 000 000 000 000

<sup>_3_</sup> 1×10<sup>-27</sup> is 0.000 000 000 000 000 000 000 000 001

## Future Features

- [ ] Negative numbers
- [ ] Contracted ordinal numbers (e.g. "1-й", "1000-на")
- [ ] Scientific notation of exponential numbers (e.g. "1e5")

## Supported Grammatical Attributes

- cases: nominative, genitive, dative, accusative, instrumental, locative, vocative
- gender: masculine, feminine, neuter
- number: singular, plural
- animacy: inanimate, animate
