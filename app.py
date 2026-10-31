from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# قائمة القاعات والمعامل مع متغيرات الوقت
rooms_data = [
    {"id": 1, "name": "المؤتمرات الكبرى", "status": "متاح", "booked_by": None, "start_time": None, "end_time": None},
    {"id": 2, "name": "معمل الحاسب الآلي (1)", "status": "متاح", "booked_by": None, "start_time": None,
     "end_time": None},
    {"id": 3, "name": "قاعة الاجتماعات الرئيسية", "status": "متاح", "booked_by": None, "start_time": None,
     "end_time": None},
    {"id": 4, "name": "معمل الشبكات والاتصالات", "status": "متاح", "booked_by": None, "start_time": None,
     "end_time": None},
    {"id": 5, "name": "معمل التدريب التفاعلي", "status": "متاح", "booked_by": None, "start_time": None,
     "end_time": None},
    {"id": 6, "name": "معمل الذكاء الاصطناعي", "status": "متاح", "booked_by": None, "start_time": None,
     "end_time": None}
]


# الصفحة الرئيسية (تفحص الحجوزات وتنظف المنتهية تلقائياً)
@app.route('/')
def index():
    now = datetime.now()
    for room in rooms_data:
        if room["status"] == "محجوز" and room["end_time"]:
            if now > room["end_time"]:
                room["status"] = "متاح"
                room["booked_by"] = None
                room["start_time"] = None
                room["end_time"] = None

    return render_template('index.html')


# جلب بيانات الغرف
@app.route('/api/rooms')
def get_rooms():
    return jsonify(rooms_data)


# حجز القاعة مع حساب الوقت والمدة (من 30 دقيقة إلى 3 ساعات)
@app.route('/api/book', methods=['POST'])
def book_room():
    data = request.json
    room_id = data.get('room_id')
    user_name = data.get('user_name')
    booking_time_str = data.get('booking_time')
    duration_minutes = int(data.get('duration', 60))

    if not user_name or not booking_time_str:
        return jsonify({"success": False, "message": "الرجاء إدخال الاسم ووقت الحجز"})

    if duration_minutes < 30 or duration_minutes > 180:
        return jsonify({"success": False, "message": "المدة المسموح بها من 30 دقيقة إلى 3 ساعات فقط"})

    start_time = datetime.strptime(booking_time_str, '%Y-%m-%dT%H:%M')
    end_time = start_time + timedelta(minutes=duration_minutes)

    for room in rooms_data:
        if room['id'] == room_id:
            if room['status'] == 'محجوز':
                return jsonify({"success": False, "message": "القاعة محجوزة بالفعل"})

            room['status'] = 'محجوز'
            room['booked_by'] = user_name
            room['start_time'] = start_time
            room['end_time'] = end_time
            return jsonify({"success": True})

    return jsonify({"success": False, "message": "القاعة غير موجودة"})


# إلغاء الحجز
@app.route('/api/cancel/<int:room_id>', methods=['POST'])
def cancel_room(room_id):
    for room in rooms_data:
        if room['id'] == room_id:
            room['status'] = 'متاح'
            room['booked_by'] = None
            room['start_time'] = None
            room['end_time'] = None
            return jsonify({"success": True})
    return jsonify({"success": False, "message": "القاعة غير موجودة"})


if __name__ == '__main__':
    app.run(debug=True)