# AL-HUDA Project Roadmap

Current completed step: 12
Next step: 13 — Email Verification + Password Reset

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

## Next
13. Email verification + password reset
14. Settings
15. UI + animations
16. GPS + Android permissions
17. Production background Azan
18. Full Quran/Hadith data verification
19. Full integration testing
20. Final APK build
21. Release preparation

## Security note
Step 12 stores only a salted PBKDF2 password hash locally; plaintext passwords are not stored. This is a local account foundation. Production authentication/email verification belongs to Step 13 and must use a secure backend/provider.

## Continuity rule
Use this file and the existing repository code as the source of truth. Do not randomly replace working modules.

## Testing rule
A green GitHub Actions workflow confirms the repository update, not complete Android feature testing. Final APK/device testing is required.
