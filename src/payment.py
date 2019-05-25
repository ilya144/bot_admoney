# hi, gonna use Flask, to make payment server to Free Kassa
# I'm sure that will be great


from flask import Flask, request
from threading import Thread


class ThreadPaymentServer(Thread):          #поток сервера обработки платежей
    def __init__(self):
        Thread.__init__(self)
        self.app = Flask(__name__)

    def run(self):
        @self.app.route('/', methods=["POST"])
        def write_post_body():
            print(request.body.read())
            post_str = request.body.read().decode()
            user_id = int(re.search('MERCHANT_ORDER_ID=\d+', post_str).group().split('=')[1])
            money = int(re.search(r'AMOUNT=\d+', post_str).group().split('=')[1])
            USERS[user_id].activedays += int(money / 5)
            paynumber = int(re.search(r'intid=\d+', post_str).group().split('=')[1])
            bot.send_message(user_id,'Оплата успешна\nНомер вашего платежа: %d'%paynumber)
            #with open('payment%s.txt' % user_id, 'wb') as f:
            #    f.write(request.body.read())
            #    f.close()
            return "Принял POST запрос"

        @self.app.route('/test')
        def hello_world():
            return 'Проверка сервера\nМожно принимать деньги)'
        while True:
            try:self.app.run(host='0.0.0.0', port=12377)
            except Exception:continue