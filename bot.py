from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = "8620454775:AAFbvtocUZPOOgtHcO6I4_FqzD4QyvKHYmg"

POINTS = {1:0, 2:2, 3:4, 4:6, 5:8, 6:12, 7:16, 8:20, 9:30, 10:40, 11:80, 12:100, 13:125, 14:150}
POWER = {1:4, 2:6, 3:8, 4:12, 5:15, 6:20, 7:25, 8:33, 9:45, 10:60, 11:80, 12:100, 13:125, 14:150}
STAGES = {1:300, 2:600, 3:1500, 4:2000, 5:3000, 6:4000, 7:5000, 8:6000, 9:7000, 10:8000, 11:9000, 12:10000}

user_data = {}

def get_stage(points):
    stage = 0
    for s, t in STAGES.items():
        if points >= t:
            stage = s
        else:
            return stage, t
    return stage, STAGES[12]

async def start(update, context):
    uid = update.effective_user.id
    user_data[uid] = {i: 0 for i in range(1, 15)}
    await menu(update, uid)

async def menu(update, uid):
    cnt = user_data.get(uid, {i: 0 for i in range(1, 15)})
    text = "📊 **Калькулятор войны**\n\n"
    for i in range(1, 15):
        text += f"T{i}: {cnt[i]}\n"
    kb = []
    for i in range(1, 15):
        kb.append([InlineKeyboardButton(f"T{i} -1", callback_data=f"d{i}"),
                   InlineKeyboardButton(f"T{i} +1", callback_data=f"a{i}")])
    kb.append([InlineKeyboardButton("✅ Рассчитать", callback_data="calc")])
    kb.append([InlineKeyboardButton("🗑 Очистить", callback_data="clear")])
    try:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    except:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def add(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    lvl = int(q.data[1:])
    user_data.setdefault(uid, {i: 0 for i in range(1, 15)})[lvl] += 1
    await menu(update, uid)

async def dec(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    lvl = int(q.data[1:])
    if user_data.get(uid, {}).get(lvl, 0) > 0:
        user_data[uid][lvl] -= 1
    await menu(update, uid)

async def clear(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    user_data[uid] = {i: 0 for i in range(1, 15)}
    await menu(update, uid)

async def calc(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    cnt = user_data.get(uid, {i: 0 for i in range(1, 15)})
    points = sum(POINTS[l] * cnt[l] for l in range(1, 15))
    power = sum(POWER[l] * cnt[l] for l in range(1, 15))
    stage, nxt = get_stage(points)
    res = f"🎯 **Очки:** {points}\n🏆 **Стадий:** {stage}\n"
    if stage < 12:
        res += f"📈 **До {stage+1}:** {points} / {nxt}\n"
    res += f"⚡ **Бонус восстановления:** +300% (мощь: {power} → {power*4})"
    kb = [[InlineKeyboardButton("🔙 Назад", callback_data="back")]]
    await q.edit_message_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def back(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    await menu(update, uid)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(add, pattern="^a"))
    app.add_handler(CallbackQueryHandler(dec, pattern="^d"))
    app.add_handler(CallbackQueryHandler(clear, pattern="^clear$"))
    app.add_handler(CallbackQueryHandler(calc, pattern="^calc$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    print("✅ Калькулятор войны запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
