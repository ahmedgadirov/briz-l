# 👑 Vera for Seljan - Admin Guide

Welcome Seljan! This guide explains your special admin features with Vera.

---

## 🎯 What's Special About Your Access

When you message Vera on WhatsApp (+994502115120), you get **unlimited AI access** with no restrictions! Vera becomes your personal assistant for:

1. **Clinic Management** - Daily reports, analytics, lead insights
2. **Content Creation** - Write anything you need
3. **General Assistance** - Answer questions, research, analysis
4. **Unlimited Conversations** - No message limits!

---

## 📊 Daily Reports (Automated)

Every morning at **9:00 AM**, Vera automatically sends you a clinic report including:

- **Yesterday's Performance**
  - New leads
  - Hot leads
  - Booking intents
  - Follow-ups sent

- **This Week So Far**
  - Total leads
  - Hot leads
  - Conversion metrics

- **Conversion Funnel**
  - Lead progression rates
  - Conversion percentages

- **Top Procedures**
  - Most inquired surgeries

- **Hot Leads to Follow**
  - High-priority patients
  - Lead scores
  - Interests

---

## 📱 Manual Reports (On-Demand)

You can send reports to yourself anytime using the command line:

### Daily Report
```bash
python send_report.py
```
or
```bash
python send_report.py --type daily
```

### Weekly Report
```bash
python send_report.py --type weekly
```

### Monthly Report
```bash
python send_report.py --type monthly
```

### Custom Message
```bash
python send_report.py --type custom --message "Your custom text here"
```

---

## 💬 Chat with Vera on WhatsApp

Simply message Vera on WhatsApp from your number: **+994502115120**

### What You Can Ask:

**Clinic Questions:**
- "How many leads did we get today?"
- "Show me our hot leads"
- "What's our conversion rate?"
- "Which surgeries are most popular?"

**Content Creation:**
- "Write a blog post about rhinoplasty recovery"
- "Create an Instagram caption for before/after photos"
- "Draft an email to a potential patient"
- "Write a social media post about Briz-L"

**General Help:**
- "Research the latest trends in aesthetic surgery"
- "Summarize this article for me"
- "Help me brainstorm marketing ideas"
- "Answer this question about..."

**Unlimited!**
- No message limits
- No AI restrictions
- Vera is your personal assistant!

---

## 🔍 How It Works

### For You (Admin):
- **Phone Number:** 994502115120 (Your number)
- **Unlimited AI Access:** ✅
- **Personalized Responses:** ✅
- **Clinic-Focused:** ✅
- **Can Write Anything:** ✅

### For Regular Users (Patients):
- **Limited AI Access:** They have message limits
- **Medical Focus:** Only medical consultations
- **Standard Vera:** Professional medical assistant

---

## 📝 Example Conversations

### Quick Update
**You:** "Hi Vera"

**Vera:** "Hello Seljan! 👋 Vera here.

📊 Quick Update:
• Total Leads: 45
• Hot Leads: 12
• New Today: 3

How can I help you today? I'm ready to assist with clinic reports, writing, or anything else you need! ✨"

### Content Request
**You:** "Write me a 200-word Instagram caption about summer body preparations"

**Vera:** [Generates custom content for you]

### Clinic Analysis
**You:** "What are our top 3 most inquired procedures this month?"

**Vera:** [Provides detailed breakdown with numbers]

---

## 🚀 System Architecture

Your admin features include:

1. **Admin Detection**
   - Vera recognizes your phone number
   - Automatically switches to "Seljan mode"
   - No setup needed!

2. **Daily Report Scheduler**
   - Runs 24/7 in background
   - Sends reports at 9:00 AM
   - Never forgets!

3. **Manual CLI Tools**
   - `send_report.py` - Send reports on demand
   - `admin_handler.py` - Core admin functions
   - `daily_report_scheduler.py` - Automated system

4. **Unlimited AI**
   - Direct OpenAI access
   - No rate limiting
   - Full capabilities

---

## 📞 Quick Reference

### Your WhatsApp Number (Admin)
```
+994502115120
```

### CLI Commands
```bash
# Daily report
python send_report.py

# Weekly report
python send_report.py --type weekly

# Monthly report
python send_report.py --type monthly

# Custom message
python send_report.py --type custom --message "Hello Seljan!"
```

### When You Get Reports
- **Automated:** Every day at 9:00 AM
- **Manual:** Anytime you run the command
- **On Request:** Just ask Vera via WhatsApp

---

## 🎨 Personality

Vera speaks to you differently than regular users:

- Addresses you as "Seljan"
- Warm and supportive tone
- Proactive with clinic insights
- Ready for ANY task (not just medical)
- Professional but friendly

---

## ❓ FAQ

**Q: Can I change the report time?**
A: Yes! Edit `daily_report_scheduler.py` and change the schedule time.

**Q: What if I don't want daily reports?**
A: You can disable the scheduler in `start.sh` by commenting out the scheduler lines.

**Q: Can other people get admin access?**
A: Currently only your number (994502115120) has admin access. This can be expanded if needed.

**Q: Does this affect regular patients?**
A: No! Regular users still get standard Vera (medical assistant) with normal limits.

**Q: Can I send reports to someone else?**
A: Yes! Modify the `ADMIN_NUMBER` in `admin_handler.py` or create a new function.

---

## 🛠️ Technical Details

### Files Created for You:
- `admin_handler.py` - Admin detection & report generation
- `send_report.py` - Manual CLI tool for reports
- `daily_report_scheduler.py` - Automated 9 AM reports
- `SELJAN_ADMIN_GUIDE.md` - This guide!

### Modified Files:
- `social_media_webhook.py` - Detects your number
- `start.sh` - Starts scheduler automatically
- `requirements.txt` - Added `schedule` library
- `.env` - Your credentials configured

### Database Tables Used:
- `marketing_leads` - Patient leads
- `marketing_analytics` - Daily stats
- `conversion_events` - Conversion tracking

---

## 🎉 Summary

**You're all set Seljan!**

- ✅ Auto daily reports at 9 AM
- ✅ Manual reports anytime
- ✅ Unlimited AI chat on WhatsApp
- ✅ Personalized Vera just for you
- ✅ Clinic-focused insights
- ✅ Content creation on demand

**Just message Vera on WhatsApp and she's ready to help! 💪**

---

## 💡 Tips

1. **Morning Routine:** Check your 9 AM report to start the day
2. **Quick Commands:** Ask "give me today's summary" for instant stats
3. **Content Batch:** Ask Vera to write multiple things at once
4. **Analytics Deep Dive:** Request specific metrics anytime
5. **Save Time:** Let Vera draft your content, then refine it

---

**Need Help?** Just message Vera - she's your unlimited assistant! 🚀

*Last Updated: February 11, 2026*
