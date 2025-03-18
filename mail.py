from dotenv import load_dotenv
load_dotenv()
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from functools import wraps

# Outlook Configuration
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("OUTLOOK_MAIL")
EMAIL_PASSWORD = os.getenv("OUTLOOK_PASSWORD")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Get group ID from environment
ALLOWED_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
def restricted_to_group(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_chat or str(update.effective_chat.id) != ALLOWED_GROUP_ID:
            if update.message:
                await update.message.reply_text("⚠️ Unauthorized access!")
            return
        return await func(update, context)
    return wrapped

@restricted_to_group
async def send_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Đang xử lý...")

    try:
        args = context.args
        
        # Split arguments into product name and emails
        product_parts = []
        emails = []
        email_found = False
        
        for arg in args:
            if not email_found and '@' in arg:
                email_found = True
                
            if email_found:
                emails.append(arg)
            else:
                product_parts.append(arg)

        # Validate input
        if not product_parts:
            await update.message.reply_text("❌ Vui lòng nhập tên sản phẩm!\nVí dụ: /send \"Tai nghe M9\" customer1@mail.com customer2@mail.com")
            return
            
        if not emails:
            await update.message.reply_text("❌ Vui lòng nhập ít nhất một địa chỉ email!\nVí dụ: /send \"Tai nghe M9\" customer1@mail.com customer2@mail.com")
            return

        product_name = ' '.join(product_parts)
        body = f"""Kính chào quý khách hàng, sản phẩm bạn Order : "{product_name}" Hiện tại đã hạ cánh tại kho HN. Nếu chưa thanh toán nốt số tiền còn lại, bạn vui lòng liên hệ và thanh toán qua kênh Discord hoặc Facebook của shop nhé.

Sau khi xác nhận thanh toán hoàn tất, bên mình sẽ làm việc và đóng gói hàng trong 1-2 ngày liền kề, bạn vui lòng kiểm tra thông tin trên app ViettelPost nếu có nhu cầu nhận Mã Vận Đơn.

T-Order xin trân trọng cảm ơn.

Thông tin liên lạc:
- Discord: https://discord.gg/torder
- Facebook: https://www.facebook.com/torder19

Vui lòng không trả lời email này"""

        # Send to each recipient individually
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            success_count = 0
            for email in emails:
                try:
                    msg = MIMEMultipart()
                    msg['From'] = f"T-Order <{EMAIL_ADDRESS}>"
                    msg['To'] = email
                    msg['Subject'] = "🚀 [QUAN TRỌNG] THÔNG BÁO VỀ TÌNH TRẠNG ĐƠN HÀNG"
                    msg.attach(MIMEText(body, 'plain', 'utf-8'))
                    server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
                    success_count += 1
                except Exception as e:
                    print(f"Failed to send to {email}: {str(e)}")

            await update.message.reply_text(
                f"✅ Đã gửi thông báo cho {product_name}\n"
                f"Thành công: {success_count}/{len(emails)}\n"
                f"Email nhận: {', '.join(emails)}"
            )

    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi hệ thống: {str(e)}")
        

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("send", send_command))
    app.run_polling()

if __name__ == "__main__":
    main()