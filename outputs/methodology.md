# Google Trends Clinic Dashboard Methodology

- Generated: 2026-06-13T04:39:10+00:00
- Geography: TH / Thailand
- Range: 2022-01-01 to 2026-06-13
- Grain: weekly
- Source: Google Trends <https://trends.google.com/trends/>

## Methodology

- Each canonical brand is represented by an alias expression joined with '+', which Google Trends parses as multiple broad keywords within one comparison item.
- single_index is the standard Google Trends 0-100 index for each canonical alias group, normalized within that brand over the selected time range.
- comparison_index is anchored through THE KLINIQ because Google Trends direct comparison is limited to small groups; groups were rescaled using the shared THE KLINIQ series and then normalized to the cross-brand maximum.
- The data is weekly, Thailand-only, web search, all categories, from 2022-01-01 through 2026-06-13.

## Limitations

- Google Trends values are relative indices, not absolute search volumes.
- Low-volume terms can return zeros due to rounding/privacy thresholds.
- Generic names such as APEX, SLC, L Clinic, Acne Lab, Ritz, and acronym-style brands can include non-brand intent despite clinic aliases.
- Alias mapping is a query design, not a legal-brand verification table; review ambiguous names before making investment decisions.

## Alias Map

### THE KLINIQ
- Query: `THE KLINIQ + THE KLINIQUE + เดอะคลีนิกค์ + เดอะคลินิก + เดอะคลีนิค`
- Source note: Official website text uses THE KLINIQUE and เดอะคลีนิกค์; user canonical kept as THE KLINIQ.
- Source URL: https://www.theklinique.com/

### KLINIQ Surgery
- Query: `KLINIQ Surgery + THE KLINIQUE Surgery + Klinique Surgery + เดอะคลีนิกค์ ศัลยกรรม`
- Source note: Surgery wording appears on THE KLINIQUE official service navigation; long Thai surgery-center phrase omitted from the Trends query because it triggers a Google Trends bad-request response.
- Source URL: https://www.theklinique.com/

### LABX
- Query: `LABX + LABX Clinic + LAB X Clinic + แล็บเอ็กซ์ + แลบเอ็กซ์`
- Source note: Seeded from user-provided brand plus Thai/English spelling variants; official source not verified in this run.
- Caveat: Low-volume or generic lab wording can create zeros/noise.

### L clinic
- Query: `L Clinic + L clinic + แอลคลินิก + แอล คลินิก`
- Source note: Seeded from user-provided brand plus Thai/English spelling variants.
- Caveat: Very generic name; results may include unrelated clinics.

### Acne lab
- Query: `Acne Lab + Acne Lab Clinic + Acnelab + แอคเน่แลบ + แอคเน่ แล็บ`
- Source note: Seeded from user-provided brand plus Thai/English spelling variants.
- Caveat: Generic acne wording can include non-brand search intent.

### AURA Bangkok clinic
- Query: `Aura Bangkok Clinic + Aura Bangkok + ออร่า แบงคอก คลินิก + ออร่าแบงคอก + ออร่า Bangkok`
- Source note: Official website title and page text use Aura Bangkok Clinic.
- Source URL: https://aurabangkokclinic.com/

### Aura Xpress
- Query: `Aura Xpress + Aura Express + Aura Xpress Clinic + ออร่า เอ็กซ์เพรส + ออร่า เอ็กซ์เพรส คลินิก`
- Source note: Seeded from user-provided brand plus common Xpress/Express spelling variants.

### Vsquare
- Query: `V Square Clinic + VSquare Clinic + V Square + วีสแควร์คลินิก + วี สแควร์ คลินิก`
- Source note: Official website title and page text use V Square Clinic.
- Source URL: https://www.vsquareclinic.com/

### SLC
- Query: `SLC Clinic + SLC Hospital + SLC คลินิก + เอสแอลซี คลินิก + SLC Clinics Hospital`
- Source note: Official website title uses SLC(Clinics&Hospital).
- Source URL: https://www.slcclinic.com/
- Caveat: Acronym can include non-clinic meanings; clinic/hospital aliases reduce but do not remove noise.

### APEX
- Query: `APEX Clinic + APEX Medical Center + Apex Profound Beauty + เอเพ็กซ์ คลินิก + เอเพ็กซ์`
- Source note: Official website title uses APEX Hospital & Clinic and Apex Beauty.
- Source URL: https://www.apexprofoundbeauty.com/
- Caveat: APEX is generic outside beauty clinics; clinic/medical aliases are included.

### KKC clinic
- Query: `KKC Clinic + KKC คลินิก + เคเคซี คลินิก + เคเคซีคลินิก`
- Source note: Seeded from user-provided brand plus Thai/English spelling variants; official source not verified in this run.
- Caveat: Acronym can include unrelated meanings.

### พรเกษม
- Query: `พรเกษม + พรเกษมคลินิก + พรเกษม คลินิก + Pornkasem Clinic + Pornkasem`
- Source note: Official website uses พรเกษม and Pornkasem.
- Source URL: https://www.pornkasemclinic.com/

### Gangnam clinic
- Query: `Gangnam Clinic + Gangnam Consult + กังนัมคลินิก + กังนัม คลินิก`
- Source note: Official website title uses Gangnam Clinic.
- Source URL: https://www.gangnamconsult.com/

### Souel clinic
- Query: `Souel Clinic + Seoul Clinic + Seoul Clinic Thailand + โซลคลินิก + โซล คลินิก`
- Source note: User spelling retained; Seoul spelling added as likely English variant.
- Caveat: Spelling is ambiguous: user wrote Souel; Seoul is included as a likely variant and should be reviewed.

### Romrawin
- Query: `Romrawin Clinic + Romrawin + รมย์รวินท์ + รมย์รวินท์คลินิก + รมย์รวินท์ คลินิก`
- Source note: Official website title uses รมย์รวินท์คลินิก.
- Source URL: https://www.romrawin.com/

### นิติพล
- Query: `นิติพล + นิติพลคลินิก + นิติพล คลินิก + Nitipon Clinic + Nitipon`
- Source note: Seeded from user-provided Thai name plus common English spelling.

### THE RITZ clinic
- Query: `THE RITZ Clinic + The Ritz Clinic + Ritz Clinic + เดอะริทซ์คลินิก + เดอะ ริทซ์ คลินิก`
- Source note: Seeded from user-provided brand plus Thai/English spelling variants.
- Caveat: Ritz can include hotel/non-clinic intent; clinic aliases are included.
