# FromTo Translator

FromTo Translator is a Python library that provides the ability to perform translation operations between the Karakalpak language and 204 other languages using the APIs of the from-to.uz site.

## Usage

```python
from fromto import Translator

translator = Translator()

# Example usage: Translate from Uzbek to Karakalpak
translation = translator.translate(text="salom")

print(translation.text())               # Salom
print(translation.result())             # Sálem
print(translation.from_lang())          # uzn_Latn
print(translation.to_lang())            # kaa
```

## Translator Class

#### `Translator()`

Initialize a `Translator` object with the base URL of the translation API.

#### `translate(text: str, from_lang: str = "uzn_Latn", to_lang: str = "kaa") -> TranslateResult`

Translate text from one language to another using the translation API.

- `text` (str): The text to be translated.
- `from_lang` (str, optional): The code representing the original language of the text. Defaults to "uzn_Latn".
- `to_lang` (str, optional): The code representing the target language for translation. Defaults to "kaa".

Returns:
`TranslateResult`: An object representing the translation result.

Raises:
`TranslateFail`: If there is an issue with the translation request.

## Example

```python
from fromto import Translator, TranslateFail

translator = Translator()

try:
    translation = translator.translate("Hello", from_lang="no_lang", to_lang="no_lang")
    print(translation.result)
except TranslateFail as e:
    print(f"Translation failed: {e}")
```

## Languages
| Language       | Code     |
|----------------|----------|
| English        | eng_Latn |
| Russian        | rus_Cyrl |
| Uzbek          | uzn_Latn |
| Karakalpak     | kaa      |
| Acehnese       | ace_Latn |
| Mesopotamian Arabic | acm_Arab |
| Ta’izzi-Adeni Arabic | acq_Arab |
| Tunisian Arabic | aeb_Arab |
| Afrikaans      | afr_Latn |
| South Levantine Arabic | ajp_Arab |
| Akan           | aka_Latn |
| Amharic        | amh_Ethi |
| North Levantine Arabic | apc_Arab |
| Modern Standard Arabic | arb_Arab |
| Modern Standard Arabic (Romanized) | arb_Latn |
| Najdi Arabic   | ars_Arab |
| Moroccan Arabic | ary_Arab |
| Egyptian Arabic | arz_Arab |
| Assamese       | asm_Beng |
| Asturian       | ast_Latn |
| Awadhi         | awa_Deva |
| Central Aymara | ayr_Latn |
| South Azerbaijani | azb_Arab |
| North Azerbaijani | azj_Latn |
| Bashkir        | bak_Cyrl |
| Bambara        | bam_Latn |
| Balinese       | ban_Latn |
| Belarusian     | bel_Cyrl |
| Bemba          | bem_Latn |
| Bengali        | ben_Beng |
| Bhojpuri       | bho_Deva |
| Banjar         | bjn_Latn |
| Standard Tibetan | bod_Tibt |
| Bosnian        | bos_Latn |
| Buginese       | bug_Latn |
| Bulgarian      | bul_Cyrl |
| Catalan        | cat_Latn |
| Cebuano        | ceb_Latn |
| Czech          | ces_Latn |
| Chokwe         | cjk_Latn |
| Central Kurdish | ckb_Arab |
| Crimean Tatar  | crh_Latn |
| Welsh          | cym_Latn |
| Danish         | dan_Latn |
| German         | deu_Latn |
| Southwestern Dinka | dik_Latn |
| Dyula          | dyu_Latn |
| Dzongkha       | dzo_Tibt |
| Greek          | ell_Grek |
| Esperanto      | epo_Latn |
| Estonian       | est_Latn |
| Basque         | eus_Latn |
| Ewe            | ewe_Latn |
| Faroese        | fao_Latn |
| Fijian         | fij_Latn |
| Finnish        | fin_Latn |
| Fon            | fon_Latn |
| French         | fra_Latn |
| Friulian       | fur_Latn |
| Nigerian Fulfulde | fuv_Latn |
| Scottish Gaelic | gla_Latn |
| Irish          | gle_Latn |
| Galician       | glg_Latn |
| Guarani        | grn_Latn |
| Gujarati       | guj_Gujr |
| Haitian Creole | hat_Latn |
| Hausa          | hau_Latn |
| Hebrew         | heb_Hebr |
| Hindi          | hin_Deva |
| Chhattisgarhi  | hne_Deva |
| Croatian       | hrv_Latn |
| Hungarian      | hun_Latn |
| Armenian       | hye_Armn |
| Igbo           | ibo_Latn |
| Ilocano        | ilo_Latn |
| Indonesian     | ind_Latn |
| Icelandic      | isl_Latn |
| Italian        | ita_Latn |
| Javanese       | jav_Latn |
| Japanese       | jpn_Jpan |
| Kabyle         | kab_Latn |
| Jingpho        | kac_Latn |
| Kamba          | kam_Latn |
| Kannada        | kan_Knda |
| Georgian       | kat_Geor |
| Central Kanuri | knc_Latn |
| Kazakh         | kaz_Cyrl |
| Kabiyè         | kbp_Latn |
| Kabuverdianu   | kea_Latn |
| Khmer          | khm_Khmr |
| Kikuyu         | kik_Latn |
| Kinyarwanda    | kin_Latn |
| Kyrgyz         | kir_Cyrl |
| Kimbundu       | kmb_Latn |
| Northern Kurdish | kmr_Latn |
| Kikongo        | kon_Latn |
| Korean         | kor_Hang |
| Lao            | lao_Laoo |
| Ligurian       | lij_Latn |
| Limburgish     | lim_Latn |
| Lingala        | lin_Latn |
| Lithuanian     | lit_Latn |
| Lombard        | lmo_Latn |
| Latgalian      | ltg_Latn |
| Luxembourgish  | ltz_Latn |
| Luba-Kasai     | lua_Latn |
| Ganda          | lug_Latn |
| Luo            | luo_Latn |
| Mizo           | lus_Latn |
| Standard Latvian | lvs_Latn |
| Magahi         | mag_Deva |
| Maithili       | mai_Deva |
| Malayalam      | mal_Mlym |
| Marathi        | mar_Deva |
| Minangkabau    | min_Latn |
| Macedonian     | mkd_Cyrl |
| Plateau Malagasy | plt_Latn |
| Maltese        | mlt_Latn |
| Meitei         | mni_Beng |
| Halh Mongolian | khk_Cyrl |
| Mossi          | mos_Latn |
| Maori          | mri_Latn |
| Burmese        | mya_Mymr |
| Dutch          | nld_Latn |
| Norwegian Nynorsk | nno_Latn |
| Norwegian Bokmål | nob_Latn |
| Nepali         | npi_Deva |
| Northern Sotho | nso_Latn |
| Nuer           | nus_Latn |
| Nyanja         | nya_Latn |
| Occitan        | oci_Latn |
| West Central Oromo | gaz_Latn |
| Odia           | ory_Orya |
| Pangasinan     | pag_Latn |
| Eastern Panjabi | pan_Guru |
| Papiamento     | pap_Latn |
| Western Persian | pes_Arab |
| Polish         | pol_Latn |
| Portuguese     | por_Latn |
| Dari           | prs_Arab |
| Southern Pashto | pbt_Arab |
| Ayacucho Quechua | quy_Latn |
| Romanian       | ron_Lat

## License

This library is licensed under the MIT License.