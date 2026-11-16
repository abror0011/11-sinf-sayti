# 11-A sinf sayti

Bu sayt Git va GitHub darsida sinf jamoa bo'lib yaratadi.

## Jamoa qoidalari

1. `main` ga to'g'ridan-to'g'ri yozilmaydi. Har bir ish alohida branchda qilinadi.
2. Branch nomi: `feature/sahifa-nomi`, masalan `feature/dars-jadvali`.
3. Commit xabari: `tur(soha): nima qilindi`, masalan `feat(jadval): dushanba darslari qo'shildi`.
4. Ish tayyor bo'lgach, Pull Request ochiladi va shablon to'ldiriladi.
5. PR boshqa guruh va o'qituvchi tasdiqlagandan, tekshiruv (CI) yashil bo'lgandan keyin qo'shiladi.

## Sahifani lokal tekshirish

```bash
python scripts/check_html.py
```

## Guruhlar

| Guruh | Sahifa | Branch |
|---|---|---|
| 1 | Bizning sinf | `feature/bizning-sinf` |
| 2 | Dars jadvali | `feature/dars-jadvali` |
| 3 | Yutuqlarimiz | `feature/yutuqlar` |
| 4 | Fotogalereya | `feature/galereya` |
