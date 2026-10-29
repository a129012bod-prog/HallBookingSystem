function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
}

document.addEventListener("DOMContentLoaded", fetchFacilities);

async function fetchFacilities() {
    try {
        const response = await fetch('/api/facilities');
        const facilities = await response.json();
        renderFacilities(facilities);
    } catch (error) {
        console.error("خطأ في جلب البيانات:", error);
    }
}

function renderFacilities(facilities) {
    const grid = document.getElementById('facilities-grid');
    grid.innerHTML = '';

    facilities.forEach(fac => {
        const isBooked = fac.status === 'محجوز';

        const cardBg = isBooked
            ? 'border-red-500 bg-red-50/50 dark:bg-red-950/20'
            : 'border-green-500 bg-green-50/50 dark:bg-green-950/20';

        const badgeColor = isBooked
            ? 'bg-red-500 text-white'
            : 'bg-green-500 text-white';

        const cardHTML = `
            <div class="border-2 ${cardBg} rounded-2xl p-5 shadow-sm transition-all duration-300 flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-start mb-3">
                        <h3 class="font-bold text-lg">${fac.name}</h3>
                        <span class="text-xs px-3 py-1 rounded-full font-semibold ${badgeColor}">${fac.status}</span>
                    </div>
                    <p class="text-sm text-slate-500 dark:text-slate-400 mb-4">النوع: ${fac.type}</p>
                </div>

                <div>
                    ${isBooked ? `
                        <p class="text-sm text-red-600 dark:text-red-400 font-semibold mb-3">محجوز بواسطة: ${fac.booked_by}</p>
                    ` : `
                        <div class="space-y-2">
                            <input type="text" id="name-${fac.id}" placeholder="أدخل اسمك الكريم..."
                                class="w-full px-3 py-2 text-sm border rounded-lg dark:bg-slate-700 dark:border-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <button onclick="bookFacility(${fac.id})"
                                class="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold py-2 rounded-lg transition">
                                تأكيد الحجز
                            </button>
                        </div>
                    `}
                </div>
            </div>
        `;
        grid.innerHTML += cardHTML;
    });
}

async function bookFacility(id) {
    const nameInput = document.getElementById(`name-${id}`);
    const name = nameInput.value.trim();

    if (!name) {
        alert("الرجاء كتابة الاسم قبل إتمام الحجز!");
        return;
    }

    try {
        const response = await fetch('/api/book', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: id, name: name })
        });

        const result = await response.json();
        if (result.success) {
            fetchFacilities();
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error("خطأ في عملية الحجز:", error);
    }
}