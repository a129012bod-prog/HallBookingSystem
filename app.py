from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# قائمة مبدئية للقاعات والمعامل وحالتها
rooms_data = [
    {"id": 1, "name": "قاعة المؤتمرات الكبرى", "type": "قاعة", "status": "متاح", "booked_by": ""},
    {"id": 2, "name": "معمل الحاسب الآلي (1)", "type": "معمل", "status": "متاح", "booked_by": ""},
    {"id": 3, "name": "قاعة الاجتماعات الرئيسية", "type": "قاعة", "status": "محجوز", "booked_by": "أحمد محمد"},
    {"id": 4, "name": "معمل الشبكات والاتصالات", "type": "معمل", "status": "متاح", "booked_by": ""},
    {"id": 5, "name": "قاعة التدريب التفاعلي", "type": "قاعة", "status": "محجوز", "booked_by": "سارة خالد"},
    {"id": 6, "name": "معمل الذكاء الاصطناعي", "type": "معمل", "status": "متاح", "booked_by": ""},
]


@app.route('/')
def index():
    return render_template('index.html', rooms=rooms_data)


@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    return jsonify(rooms_data)


@app.route('/api/book', methods=['POST'])
def book_room():
    data = request.json
    room_id = data.get('room_id')
    user_name = data.get('user_name')

    if not user_name:
        return jsonify({"success": False, "message": "الرجاء إدخال اسم الحاجز!"}), 400

    for room in rooms_data:
        if room['id'] == room_id:
            if room['status'] == 'محجوز':
                return jsonify({"success": False, "message": "هذه القاعة/المعمل محجوزة مسبقاً!"}), 400
            room['status'] = 'محجوز'
            room['booked_by'] = user_name
            return jsonify({"success": True, "message": "تم الحجز بنجاح!"})

    return jsonify({"success": False, "message": "القاعة غير موجودة!"}), 404


if __name__ == '__main__':
    app.run(debug=True)