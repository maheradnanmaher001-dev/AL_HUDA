from datetime import date, timedelta

ISLAMIC_MONTHS = (
    "Muharram","Safar","Rabi al-Awwal","Rabi al-Thani",
    "Jumada al-Awwal","Jumada al-Thani","Rajab","Sha'ban",
    "Ramadan","Shawwal","Dhu al-Qi'dah","Dhu al-Hijjah"
)

def gregorian_to_hijri(d):
    # Arithmetic Islamic calendar approximation; suitable as a UI foundation.
    jd = d.toordinal() + 1721424.5
    l = int(jd) - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631*n + 354
    j = ((10985-l)//5316)*((50*l)//17719) + (l//5670)*((43*l)//15238)
    l = l - ((30-j)//15)*((17719*j)//50) - (j//16)*((15238*j)//43) + 29
    m = (24*l)//709
    day = l - (709*m)//24
    year = 30*n + j - 30
    return year, m, day

def hijri_label(d=None):
    d=d or date.today()
    y,m,day=gregorian_to_hijri(d)
    return f"{day} {ISLAMIC_MONTHS[m-1]} {y} AH"

def month_grid(year, month):
    first=date(year,month,1)
    start=first - timedelta(days=(first.weekday()+1)%7)
    grid=[]
    for i in range(42):
        grid.append(start+timedelta(days=i))
    return grid
