from dataclasses import dataclass

@dataclass(frozen=True)
class Dua:
    title: str
    arabic: str
    urdu: str
    english: str
    reference: str
    category: str

DUAS = [
    Dua("Before Sleeping","بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
        "اے اللہ! تیرے ہی نام کے ساتھ مرتا اور جیتا ہوں۔",
        "O Allah, in Your name I die and live.","Sahih al-Bukhari","Before Sleeping"),
    Dua("On Waking","الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا",
        "تمام تعریفیں اللہ کے لیے ہیں جس نے ہمیں موت کے بعد زندگی دی۔",
        "Praise is for Allah who gave us life after causing us to die.","Sahih al-Bukhari","Waking Up"),
    Dua("Before Eating","بِسْمِ اللَّهِ",
        "اللہ کے نام سے۔","In the name of Allah.","Sunan Abi Dawud","Before Eating"),
    Dua("After Eating","الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا",
        "تمام تعریفیں اللہ کے لیے جس نے مجھے یہ کھانا کھلایا۔",
        "Praise is for Allah who fed me this.","Jami` at-Tirmidhi","After Eating"),
    Dua("Leaving Home","بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ",
        "اللہ کے نام سے، میں نے اللہ پر بھروسہ کیا۔",
        "In the name of Allah, I put my trust in Allah.","Sunan Abi Dawud","Leaving Home"),
    Dua("Entering Home","اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ الْمَوْلَجِ",
        "اے اللہ! میں تجھ سے بہترین داخلے کا سوال کرتا ہوں۔",
        "O Allah, I ask You for the best entrance.","Sunan Abi Dawud","Entering Home"),
]

CATEGORIES = [
    "Morning","Evening","After Salah","Before Sleeping","Waking Up",
    "Before Eating","After Eating","Entering Home","Leaving Home",
    "Travel","General","Protection","Quranic Duas"
]

def all_duas():
    return list(DUAS)

def by_category(category):
    return [d for d in DUAS if d.category == category]

def search(query):
    q=(query or "").strip().lower()
    if not q: return all_duas()
    return [d for d in DUAS if q in " ".join(
        (d.title,d.arabic,d.urdu,d.english,d.reference,d.category)
    ).lower()]
