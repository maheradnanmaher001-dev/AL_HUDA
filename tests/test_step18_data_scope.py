from app.services import quran_service, hadith_service

def test_quran_scope():
    assert quran_service.SURAH_COUNT == 114
    assert quran_service.JUZ_COUNT == 30
    assert quran_service.AYAH_COUNT == 6236
    assert quran_service.get_juz.__defaults__ == (quran_service.ARABIC,)

def test_hadith_scope():
    assert len(hadith_service.HADITH_COLLECTIONS) == 15
    assert "bukhari" in hadith_service.HADITH_COLLECTIONS
    assert "muslim" in hadith_service.HADITH_COLLECTIONS
