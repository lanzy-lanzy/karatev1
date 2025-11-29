# Judge Management - Quick Start Guide

## 🎯 Quick Navigation

### Access Judge Management
**In Admin Dashboard:**
1. Look at left sidebar
2. Find "Judge Management" (between "User Management" and "Trainee Management")
3. Click → View all active judges

**Direct URLs:**
- Active judges: `http://yoursite.com/admin/judges/`
- Archived judges: `http://yoursite.com/admin/judges/archived/`

---

## ➕ How to Create a Judge

### 5 Easy Steps

```
Sidebar: Judge Management
         ↓
    [Add Judge] button (top-right)
         ↓
    Fill form:
    • First Name
    • Last Name
    • Email
    • Username
    • Certification Level
    • Certification Date
         ↓
    [Create Judge]
         ↓
    ✅ Success! Judge created
```

### Form Fields Explained

| Field | Required | Notes |
|-------|----------|-------|
| First Name | Yes | Judge's first name |
| Last Name | Yes | Judge's last name |
| Email | Yes | Must be unique |
| Phone | No | Contact number |
| Username | Yes | For login (must be unique) |
| Certification Level | Yes | Regional/National/International |
| Certification Date | Yes | When certified |

---

## ✏️ How to Edit a Judge

```
Judges List
     ↓
Click [Edit] on judge
     ↓
Update information
     ↓
[Update Judge]
     ↓
✅ Changes saved
```

**What Can Be Changed:**
- ✅ First name, last name
- ✅ Phone number
- ✅ Certification level
- ✅ Certification date
- ✅ Active/inactive status
- ❌ Email (locked)
- ❌ Username (locked)

---

## 🔴 How to Deactivate a Judge

```
Judges List
     ↓
Click [Deactivate] on judge
     ↓
Confirm "Are you sure?"
     ↓
✅ Judge deactivated
   (moves to Archived Judges)
```

**When to Deactivate:**
- Judge no longer available
- Judge on break
- Judge needs time off
- Temporary unavailability

**Effect:**
- No longer in match dropdown
- Can be restored anytime
- Won't affect past matches

---

## 🟢 How to Restore a Judge

```
Archived Judges
     ↓
Click [Restore] on judge
     ↓
Confirm "Are you sure?"
     ↓
✅ Judge restored
   (returns to active list)
```

**When to Restore:**
- Judge returns from break
- Judge available again
- Need to reactivate

---

## 🔍 Search & Filter Judges

### Search
- **By:** Name, Email, or Username
- **How:** Type in search box
- **Updates:** Real-time as you type

### Filter by Certification
- **Levels:** Regional, National, International
- **How:** Select from dropdown
- **Combine:** Use search + filter together

### Examples
- Search "Sarah" → shows all judges named Sarah
- Filter "National" → shows only National level judges
- Search "Sarah" + Filter "National" → shows Sarah who is National level

---

## 🎓 Certification Levels

### Regional
- Entry level
- Local/regional tournaments
- Most common

### National
- Intermediate level
- National tournaments
- Higher expertise

### International
- Highest level
- International tournaments
- Most experienced

---

## 📋 Judges List View

### What You See
```
Name (with username)  │  Email  │  Certification  │  Date  │  Actions
─────────────────────────────────────────────────────────────────────
Sarah Johnson         │  sarah@ │  National ●     │ Jan 15 │ Edit
(@sarah.j)            │  ...    │  (blue badge)   │  2022  │ Deactivate
```

### Color Badges
- 🔵 **Blue** = National
- 🟣 **Purple** = International
- ⚫ **Gray** = Regional

### Actions
- **Edit** - Modify judge info
- **Deactivate** - Archive judge
- **Restore** - Reactivate (archived list only)

---

## 💡 Pro Tips

### Username Ideas
```
✅ Good usernames:
   judge_sarah
   judge_ahmed_1
   judge_maria_natl
   
❌ Bad usernames:
   judge1
   j_s
   Judge (must be lowercase)
```

### Finding a Judge
1. Use **Search** for quick lookup
2. Use **Filter** for certification level
3. Combine both for specific results

### Common Passwords
- Consider giving judges temporary passwords
- Ask them to change on first login
- Or set via password reset link

---

## 📌 Important Rules

### ✅ Do
- Use unique emails per judge
- Use unique usernames per judge
- Keep certification dates current
- Archive unused judges
- Restore when needed

### ❌ Don't
- Create duplicate judge records
- Use same email for multiple judges
- Use same username for multiple judges
- Leave wrong certification dates
- Delete judges (use archive instead)

---

## 🔗 Integration with Matches

### When Creating a Match
1. Judge Management → Create judges first
2. Go to Matches → Add Match
3. Judges dropdown shows **active judges only**
4. Must select **at least 3 judges**
5. Match created with judges assigned

### When Deactivating a Judge
- Existing matches unaffected
- Won't appear in new match dropdowns
- Can be restored if needed

---

## ⚠️ Common Issues

### "Email already exists"
**Problem:** Email is already used
**Solution:** Use different email
**Check:** Try searching for existing judge with that email

### "Username already exists"
**Problem:** Username is already used
**Solution:** Add number to end (judge_sarah_1)
**Try:** judge_sarah_001, judge_sarah_02

### Judge not in match dropdown
**Problem:** Judge might be archived
**Solution:** Check Archived Judges list
**Fix:** Restore the judge if needed

### Can't edit email
**Problem:** Email field is locked
**Note:** This is for security
**Alternative:** Create new judge with different email

---

## 📞 Need Help?

### Check This Guide
- Refer to sections above for your task
- Use Ctrl+F to search this document

### Check Full Documentation
- Read: `JUDGE_MANAGEMENT_GUIDE.md`
- Detailed explanations
- Best practices

### Contact Admin
- Your system administrator
- They can help troubleshoot

---

## ✅ Checklist

Before using Judge Management, confirm:
- [ ] You're logged in as Admin
- [ ] You can see "Judge Management" in sidebar
- [ ] You can navigate to the judges list
- [ ] You can click "Add Judge" button
- [ ] You understand the form fields

---

## 🚀 You're Ready!

You now have everything needed to:
- ✅ Create new judges
- ✅ Edit judge information
- ✅ Archive/restore judges
- ✅ Search and filter
- ✅ Integrate with match creation

**Happy judging!** 🥋

---

**Quick Links:**
- Active Judges: `/admin/judges/`
- Archived Judges: `/admin/judges/archived/`
- Add Judge: `/admin/judges/add/`
- Full Guide: `JUDGE_MANAGEMENT_GUIDE.md`
