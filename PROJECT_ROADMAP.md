# AL-HUDA Project Roadmap

Current completed step: 13
Next step: 14 — Settings

## Completed
1. Foundation + structure
2. Quran foundation
3. Hadith
4. Prayer Times
5. Live Qibla
6. Azan/notification foundation
7. Islamic + Gregorian calendar
8. Duas & Azkar
9. Tasbeeh Counter
10. Universal Search
11. Bookmarks + History
12. Login/Register foundation
13. Email verification + password reset foundation

## Next
14. Settings
15. UI + animations
16. GPS + Android permissions
17. Production background Azan
18. Full Quran/Hadith data verification
19. Full integration testing
20. Final APK build
21. Release preparation

## Security note
The mobile project contains no SMTP credentials. Verification/reset codes are stored only as salted hashes and expire after 10 minutes with a five-attempt limit. Actual email delivery requires a secure HTTPS backend with provider secrets stored server-side.

## Continuity rule
Use this file and the existing repository code as the source of truth. Do not randomly replace working modules.

## Testing rule
A green GitHub Actions workflow confirms the repository update, not complete Android feature testing. Final APK/device testing is required.
